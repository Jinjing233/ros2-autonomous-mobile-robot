# Gazebo ros2_control Parser Failure — 2026-07-24

## 1. Context

- ROS2 Humble, Gazebo Classic, `gazebo_ros2_control` (installed `0.4.10-1jammy.20260505.183241`).
- Workspace migrated from VMware Shared Folder (`/mnt/hgfs/ros2_autonomous_mobile_robot`) to Ubuntu native filesystem (`/home/jinjing/robot_project`, `ext2/ext3`).
- `colcon build --symlink-install` succeeded after migration.
- Gazebo, robot model, and sensor nodes (`/camera_plugin`, `/gazebo_ros_imu_sensor`, `/gazebo_ros_ray_sensor`) started normally.
- Teleop regression test failed: no robot motion.

## 2. Observed Symptoms

- `ros2 control list_controllers` could not connect to `/controller_manager/list_controllers`.
- `ros2 service call /controller_manager/list_controllers controller_manager_msgs/srv/ListControllers "{}"` hung indefinitely.
- `spawner_joint_state_broadcaster` looped on "waiting for service /controller_manager/list_controllers to become available".
- `/controller_manager/list_controllers` appeared in `ros2 service list`, but no server ever answered it.
- `gazebo_ros2_control` node was present in `ros2 node list`, but `controller_manager` never finished initializing.

## 3. Evidence

```
ros2 node list
/camera_plugin
/gazebo
/gazebo_ros2_control
/gazebo_ros_imu_sensor
/gazebo_ros_ray_sensor
/robot_state_publisher
/spawner_joint_state_broadcaster

ros2 service list | grep controller_manager
/controller_manager/list_controllers

ros2 control list_controllers
waiting for service /controller_manager/list_controllers to become available
Could not contact service /controller_manager/list_controllers
```

`/tmp/amr_gazebo_debug.log` (representative excerpt):

```
[gazebo_ros2_control]: Loading gazebo_ros2_control plugin
[gazebo_ros2_control]: Starting gazebo_ros2_control plugin in namespace: /
[gazebo_ros2_control]: Starting gazebo_ros2_control plugin in ros 2 node: gazebo_ros2_control
[gazebo_ros2_control]: connected to service!! robot_state_publisher
[gazebo_ros2_control]: Received urdf from param server, parsing...
[gazebo_ros2_control]: Loading parameter files /home/jinjing/robot_project/install/amr_control/share/amr_control/config/ros2_control.yaml
[rcutils|error_handling.c:65] an error string ... will be truncated
[ERROR] [gazebo_ros2_control]: parser error Couldn't parse parameter override rule: '--param robot_description:=<?xml version="1.0" ?> ...
```

## 4. Initial Hypotheses

All treated as **unverified** until proven or disproven by direct inspection/execution:

- robot_description 参数传递问题
- 最终 URDF/XML 内容问题（非法 XML、未闭合标签等）
- Xacro include 或重复 XML 声明问题
- 换行、BOM 或不可见字符问题
- launch 中重复注入 robot_description
- ros2_control 参数配置或安装路径问题

## 5. Investigation

1. **Launch/param passing review** (`gazebo.launch.py`, `spawn_amr.launch.py`, `gazebo_rviz.launch.py`): confirmed `robot_description` is built exactly once via `ParameterValue(Command(["xacro ", xacro_file, " ros2_control_config:=", ros2_control_config]), value_type=str)`, matching the official ROS2 Humble `ros2_control` demo pattern. No manual `--ros-args`/`--param` string construction, no duplicate injection across nodes. → Ruled out launch-level duplication.
2. **Xacro composition review** (`amr.gazebo.xacro` and all 12 included files): each macro instantiated exactly once; `gazebo_ros2_control` plugin macro appears once; `<ros2_control>` block appears once; XML declaration only in top-level source files.
3. **Generated final URDF**: ran
   `xacro <install>/amr_gazebo/share/amr_gazebo/urdf/amr.gazebo.xacro ros2_control_config:=<install>/amr_control/.../ros2_control.yaml > /tmp/amr_final.urdf`
   → exit code 0, no stderr.
4. **check_urdf /tmp/amr_final.urdf** → `Successfully Parsed XML`, full link tree valid (9 links). **Ruled out broken/invalid URDF structure.**
5. **xmllint --noout /tmp/amr_final.urdf** → passes, no XML syntax errors. **Ruled out illegal XML.**
6. **Encoding/line-ending check**: `file`, `grep -rIl $'\r'`, `xxd` on all xacro/yaml files in `amr_description/urdf` and `amr_gazebo/urdf` and `amr_control/config` → pure ASCII, no CRLF, no BOM, no control characters. **Ruled out encoding/line-ending causes for this specific bug.**
7. **ros2_control.yaml review**: `controller_manager`, `joint_state_broadcaster`, `diff_drive_controller` keys/types match ROS2 Humble official naming; joint names (`left_wheel_joint`, `right_wheel_joint`) match the final URDF exactly; `diff /src/.../ros2_control.yaml /install/.../ros2_control.yaml` → byte-identical (symlink-install is consistent). **Ruled out YAML parsing/config/install-path staleness.**
8. **Targeted content scan**: `grep -n ': ' /tmp/amr_final.urdf` (colon immediately followed by whitespace — a pattern documented in upstream issues `ros-controls/gazebo_ros2_control#295` and `ros-controls/gz_ros2_control#503` as breaking the `rcl` parameter-override-rule parser) → exactly **one** match:
   `<!-- REP-103 optical frame: z forward, x right, y down -->` (from `amr_description/urdf/amr_sensors.xacro:114`).
   Other colon+space occurrences found in source files (`amr_ros2_control.gazebo.xacro`, `amr_caster.gazebo.xacro`, `amr_properties.xacro`) sit outside macro bodies / on property declarations and do **not** appear in the expanded URDF — confirmed by diffing source comments against the generated file.
9. **Direct reproduction (not inferred from logs)**: using the exact mechanism `gazebo_ros2_control` uses internally to hand `robot_description` to `controller_manager` (a raw `--param robot_description:=<urdf>` override rule parsed by `rcl`):
   ```python
   import rclpy
   rclpy.init(args=['--ros-args', '--param', 'robot_description:=' + urdf_string])
   ```
   With the original `/tmp/amr_final.urdf` → **fails** with the byte-for-byte identical error signature as the reported log (`Couldn't parse parameter override rule: '--param robot_description:=<?xml version="1.0" ?>...`, `at ./src/rcl/arguments.c:343`).
   Removing only line 236 (the colon+space comment) from the generated URDF and re-running the identical test → **succeeds**.

   This isolates the failure to that single comment, independent of any other file or configuration.

## 6. Root Cause

- **File**: `src/amr_description/urdf/amr_sensors.xacro`, line 114.
- **Content**: `<!-- REP-103 optical frame: z forward, x right, y down -->` — a colon immediately followed by a space inside an XML comment that is included, unmodified, in the final `robot_description` URDF (via the shared `amr_sensors` macro, included by `amr.gazebo.xacro`).
- **Failure mechanism**: `gazebo_ros2_control` passes the entire `robot_description` string to its internal `controller_manager` Node via a command-line-style parameter override (`--param robot_description:=<urdf>`), which is parsed by `rcl`'s argument parser (`rcl/arguments.c`, `parse_param_rule`). This parser has a known upstream limitation (`ros-controls/gazebo_ros2_control#295`, `ros-controls/gz_ros2_control#503`): a colon followed directly by whitespace inside the parameter value is misinterpreted as a new argument/rule boundary, causing the whole override rule to fail to parse.
- **Why controller_manager never became available**: the parse failure occurs during `rcl` initialization of the `controller_manager` node that `gazebo_ros2_control` spins up internally. The node (and therefore the `/controller_manager` service server, including `/controller_manager/list_controllers`) never comes up, even though the service *name* is advertised in the ROS graph via `gazebo_ros2_control`'s own node. Downstream, `spawner` processes and `ros2 control list_controllers` wait forever for a server that never starts. Teleop non-responsiveness is a further downstream symptom of the same root cause, not an independent issue.
- The URDF is otherwise valid XML/URDF (`check_urdf`, `xmllint` both pass); the file encoding is plain ASCII with Unix line endings; the Xacro composition, launch parameter passing, and `ros2_control.yaml` configuration are all correct per ROS2 Humble official patterns. None of these were the cause.

## 7. Resolution

- **File modified**: `src/amr_description/urdf/amr_sensors.xacro` (1 line).
- **Change**:
  ```diff
  -    <!-- REP-103 optical frame: z forward, x right, y down -->
  +    <!-- REP-103 optical frame - z forward, x right, y down -->
  ```
  Colon replaced with a hyphen; comment text/meaning otherwise unchanged.
- **Why this matches ROS2 Humble official architecture**: no change to launch structure, `ParameterValue`/`Command` usage, `ros2_control.yaml`, or plugin configuration — all of which already matched the official Humble `ros2_control` demo pattern. The fix addresses the exact upstream-documented trigger condition (colon+space in `robot_description`) without working around or masking the failure (no added delays, no removed checks, no disabled logging).
- **Scope**: no geometry, joint, link, sensor, or controller parameter was changed. No package renamed, no directory moved, no launch architecture rewritten, no spawner removed.
- **Impact on frozen Sprint modules**: `amr_sensors.xacro` is shared between `amr.urdf.xacro` (non-Gazebo) and `amr.gazebo.xacro` (Gazebo). The comment-only change affects both consumers identically; no link, joint, or frame name changed, so no functional Sprint capability is expected to change. Regression scope for confirmation: Gazebo spawn, RobotModel, TF, joint states, differential drive, odometry, LiDAR, IMU, camera (see Section 9).

## 8. Verification

已由 Cursor 验证：

- **Xacro generation**: `xacro amr.gazebo.xacro ros2_control_config:=... > /tmp/amr_final_after_fix.urdf` → exit code 0.
- **check_urdf**: `Successfully Parsed XML`, 9 links, identical tree to pre-fix.
- **xmllint --noout**: passes.
- **Colon+space scan**: `grep -n ': ' /tmp/amr_final_after_fix.urdf` → no matches (previously exactly 1).
- **rclpy reproduction**: same `--param robot_description:=<urdf>` test → `rclpy.init` succeeds (previously raised `RCLError: Couldn't parse parameter override rule`).
- **colcon build --symlink-install** (after `rm -rf build install log`): `Summary: 8 packages finished [5.81s]`, no errors.
- **Headless controller_manager** (`ros2 launch amr_gazebo gazebo.launch.py gui:=false`):
  - No `Couldn't parse parameter override rule` in the log.
  - `ros2 service call /controller_manager/list_controllers ... "{}"` returns a real response:
    `joint_state_broadcaster` (active), `diff_drive_controller` (active).
  - `ros2 control list_controllers`:
    ```
    joint_state_broadcaster joint_state_broadcaster/JointStateBroadcaster  active
    diff_drive_controller   diff_drive_controller/DiffDriveController      active
    ```
  - Topics present: `/joint_states`, `/diff_drive_controller/odom`, `/diff_drive_controller/cmd_vel_unstamped`, `/scan`, `/imu`.
  - Topics **not** observed in this headless (`gui:=false`, no display/GPU) run: camera image topics. `gazebo_ros2_control` and sensor plugin logs show no camera-related errors; absence is consistent with running gzserver without a rendering context rather than a regression from this fix, but this was **not** run with GUI, so it is not treated as conclusively verified either way here.
  - A separate, pre-existing, unrelated issue was found and left unfixed pending separate approval: `cmd_vel_relay.py` has CRLF line endings (`/usr/bin/env: 'python3\r': No such file or directory`, exit code 127), so no plain `/cmd_vel` topic is bridged to `/diff_drive_controller/cmd_vel_unstamped` in this run. This is independent of the `robot_description` parser fix and is documented separately; teleop end-to-end could not be verified as a result.

待用户图形环境验证：

- Gazebo GUI
- RViz
- RobotModel
- TF 可视化
- Teleop 前进、后退、左右转（受限于上述 `cmd_vel_relay.py` CRLF 问题，当前仍无法完整验证，需先决定是否修复该问题）
- 实际 `/odom` 更新（`/diff_drive_controller/odom` 已确认存在并由 active 的 `diff_drive_controller` 发布，但滚动过程中的实际数值变化未在图形环境下人工确认）
- LiDAR、IMU、Camera 可视化

## 9. Regression Scope

| Area | Headless 验证状态 |
|---|---|
| Gazebo (gzserver 启动、entity spawn) | 已验证（headless） |
| RobotModel（URDF 结构） | 已验证（`check_urdf`），图形渲染待用户确认 |
| TF | 结构未变，图形/树状可视化待用户确认 |
| joint states | 已验证（`/joint_states` 存在，`joint_state_broadcaster` active） |
| differential drive | 已验证（`diff_drive_controller` active，接口 claim 正确） |
| odometry | 话题存在已验证，数值待图形环境下人工确认 |
| LiDAR | 话题存在已验证（`/scan`） |
| IMU | 话题存在已验证（`/imu`） |
| camera | 未在本次 headless 运行中观测到相关话题；需图形/渲染环境下验证 |

## 10. Lessons Learned

- 服务名出现在 `ros2 service list` 中不代表服务端已经可用；必须实际调用或检查节点内部初始化是否完成。
- `gazebo_ros2_control` 把 `robot_description` 作为命令行参数覆盖规则（`--param robot_description:=<urdf>`）交给 `rcl` 解析，这是已知的上游限制：URDF/Xacro 注释中的"冒号+空格"会导致该解析失败，且失败发生在 controller_manager 初始化阶段，与 URDF 是否合法（XML 层面）无关。
- 上游 controller_manager 初始化失败会表现为大量看似无关的下游症状（spawner 挂起、`list_controllers` 无响应、Teleop 无反应）；应先定位启动日志中的第一处错误，而不是从下游症状反推。
- 不应凭日志片段直接下结论；本次通过独立的 `rclpy` 复现实验，在修改前后分别验证失败与成功，才将假设升级为已确认根因。
- 工作区从 hgfs/Windows 同步目录迁移到 Ubuntu 原生文件系统后，仍可能残留 CRLF 等 Windows 编码痕迹（如本次发现的 `cmd_vel_relay.py`），需要在回归测试中系统性检查可执行脚本的行尾编码，而不仅是 URDF/Xacro/YAML。
