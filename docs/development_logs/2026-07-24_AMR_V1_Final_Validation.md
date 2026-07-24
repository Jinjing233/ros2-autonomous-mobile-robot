# AMR V1 Final Validation — 2026-07-24

## 1. Scope

This log consolidates the AMR V1 / V1.1 acceptance state after the Ubuntu-native workspace migration and the Sprint 7 Phase 1 RGB camera integration, and records the two regressions found and fixed during this migration:

- `robot_description` parameter-parsing failure (`gazebo_ros2_control` / `rcl`) — see [2026-07-24_gazebo_ros2_control_parser_failure.md](2026-07-24_gazebo_ros2_control_parser_failure.md).
- `cmd_vel_relay.py` CRLF shebang failure — documented in Section 3 below (supersedes the "left unfixed" note at the end of the parser-failure log, which predates this fix).

This document distinguishes categories of evidence, and does not claim confirmation that was not actually performed:

- **Verified today (headless, Cursor)** — direct command/log evidence captured in this headless SSH session.
- **Verified today (Ubuntu GUI, user)** — confirmed interactively by the user in a graphical Ubuntu session (Gazebo client / RViz / keyboard teleop), reported back after the headless fixes above.
- **Carried forward (prior sprint acceptance)** — capability was already accepted in `docs/milestones.md` / previous README status before this session; not re-tested today.

## 2. Regressions Found and Fixed Today

### 2.1 `robot_description` parameter override parsing failure

- **Root cause**: a colon immediately followed by a space inside an XML comment in `src/amr_description/urdf/amr_sensors.xacro` (`REP-103 optical frame: z forward, ...`), which broke `rcl`'s parameter-override-rule parser when `gazebo_ros2_control` handed `robot_description` to `controller_manager` via `--param robot_description:=<urdf>`.
- **Fix**: single-line comment edit (colon → hyphen). No geometry, joint, link, sensor, or controller parameter changed.
- **Verification**: `check_urdf`, `xmllint`, a direct `rclpy.init(args=['--ros-args','--param','robot_description:='+urdf])` reproduction (failed before, succeeded after), `colcon build --symlink-install`, and a headless `ros2 launch amr_gazebo gazebo.launch.py gui:=false` run showing `joint_state_broadcaster` and `diff_drive_controller` both `active`.
- Full detail: [2026-07-24_gazebo_ros2_control_parser_failure.md](2026-07-24_gazebo_ros2_control_parser_failure.md).

### 2.2 `cmd_vel_relay.py` CRLF shebang failure

- **Symptom**: `/usr/bin/env: 'python3\r': No such file or directory`, `cmd_vel_relay.py` exited with code 127 immediately after spawn during headless launch, breaking the `/cmd_vel → /diff_drive_controller/cmd_vel_unstamped` bridge (independent of the `robot_description` issue above; it only became visible once `controller_manager` started successfully).
- **Root cause**: `src/amr_control/scripts/cmd_vel_relay.py` had CRLF line endings (`file` reported "with CRLF line terminators"), so the shebang line was interpreted as `#!/usr/bin/env python3\r`, an interpreter name that does not exist. Byte-level confirmed with `xxd` (shebang ended `0d 0a`).
- **Fix**: `sed -i 's/\r$//'` — stripped trailing `\r` from every line. No Python logic, topic name, QoS profile, or file permission changed (verified via `git diff`: 51/51 lines changed only in line-ending, identical text content).
- **Verification**:
  - `file src/amr_control/scripts/cmd_vel_relay.py` → `Python script, ASCII text executable` (no longer reports CRLF).
  - Headless `ros2 launch amr_gazebo gazebo.launch.py gui:=false`: `cmd_vel_relay.py` stayed running (40+ s, no exit), `/cmd_vel_relay` node present in `ros2 node list`.
  - End-to-end: published `/cmd_vel` (`linear.x=0.3`, `angular.z=0.1`) and confirmed identical values arriving on `/diff_drive_controller/cmd_vel_unstamped` via `ros2 topic echo` (6/6 samples matched).
  - Sustained `/cmd_vel` publish for 3 s moved `/diff_drive_controller/odom` position from `(0.5625, 0.0311)` to `(1.6313, 0.1860)` — confirmed actual robot motion, not just message relay.

## 3. Validation Matrix

| Capability | Status | Basis |
|---|---|---|
| Gazebo GUI (gzserver + gzclient, world load, entity spawn) | ✅ Verified today (Ubuntu GUI, user) | Headless spawn verified by Cursor (`gui:=false`); full GUI session confirmed by user |
| ros2_control (`controller_manager`, `joint_state_broadcaster`, `diff_drive_controller`) | ✅ Verified today (headless, Cursor) | `ros2 control list_controllers` → both `active`; `list_controllers` service responds |
| RViz RobotModel | ✅ Verified today (Ubuntu GUI, user) | Confirmed interactively by user |
| TF | ✅ Verified today (Ubuntu GUI, user) | Confirmed interactively by user |
| Teleop (actual keyboard, `teleop_twist_keyboard`) → `/cmd_vel` → `cmd_vel_relay` → `diff_drive_controller` | ✅ Verified today (Ubuntu GUI, user) | Chain mechanics verified headlessly by Cursor (simulated publish, Section 2.2); actual keyboard driving confirmed by user |
| Odometry (`/diff_drive_controller/odom`) | ✅ Verified today (headless, Cursor) | Position changed under sustained `/cmd_vel`, values reasonable |
| LiDAR | ✅ Verified today (Ubuntu GUI, user) | Topic presence verified headlessly by Cursor; visual confirmation by user |
| IMU | ✅ Verified today (Ubuntu GUI, user) | Topic presence verified headlessly by Cursor; visual confirmation by user |
| RGB Camera (`/image_raw`, `/camera_info`, Sprint 7 Phase 1) | ✅ Verified today (Ubuntu GUI, user) | Not observed in Cursor's headless (`gui:=false`, no rendering context) run; confirmed working by user in GUI session |
| SLAM (SLAM Toolbox mapping) | ⏳ Carried forward (prior sprint acceptance) | Accepted in a prior Sprint (`docs/milestones.md` Sprint 4 / prior README status); not re-tested this session |
| AMCL Localization | ⏳ Carried forward (prior sprint acceptance) | Accepted in a prior Sprint; not re-tested this session |
| Nav2 navigation | ⏳ Carried forward (prior sprint acceptance) | Accepted in a prior Sprint; not re-tested this session |

## 4. Regression Scope Confirmed Today

- No geometry, joint, link, sensor, or controller parameter changed (all fixes were comment text / line-ending only).
- No launch architecture, package structure, or CMake/package.xml dependency logic changed beyond what Sprint 7 Phase 1 camera integration required (already reviewed separately).
- `amr_sensors.xacro` is shared by both the Gazebo and non-Gazebo (`amr.urdf.xacro`) description trees; the comment fix applies identically to both, with no link/joint/frame name change.

## 5. Outstanding Items

All graphical items from Section 3 (Gazebo GUI, RViz RobotModel, TF, keyboard Teleop, LiDAR, IMU, RGB Camera) have been confirmed by the user in a Ubuntu GUI session. No outstanding headless-vs-GUI gap remains from today's fixes.

SLAM, AMCL, and Nav2 remain carried forward from prior Sprint acceptance and were not re-tested in this session; they are unaffected by the two regressions fixed today (`robot_description` parser failure, `cmd_vel_relay.py` CRLF), since neither fix touches the SLAM/localization/navigation stacks.
