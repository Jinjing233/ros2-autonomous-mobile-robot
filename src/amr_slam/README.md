# amr_slam

SLAM Toolbox online mapping for the AMR.

## Run

Gazebo must be running first.

```bash
ros2 launch amr_slam mapping.launch.py use_sim_time:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

`mapping.launch.py` includes RViz. Skip `slam_rviz.launch.py` unless you split SLAM and RViz on purpose:

```bash
ros2 launch amr_slam online_async_slam.launch.py use_sim_time:=true
ros2 launch amr_slam slam_rviz.launch.py use_sim_time:=true
```

Save map:

```bash
ros2 launch amr_slam save_map.launch.py map_name:=my_map
```

## Topics

| Topic | Direction |
|-------|-----------|
| `/scan` | in |
| `/odom` | in |
| `/map` | out |

Publishes `map` → `odom` TF while mapping.
