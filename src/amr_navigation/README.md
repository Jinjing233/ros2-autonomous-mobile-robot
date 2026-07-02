# amr_navigation

Map server, AMCL, and Nav2 for the AMR.

## Run

Gazebo + saved map required. Default map path is in `launch/navigation.launch.py`.

```bash
ros2 launch amr_navigation navigation.launch.py use_sim_time:=true
ros2 launch amr_navigation navigation_rviz.launch.py use_sim_time:=true
```

Set goal with RViz **2D Goal Pose** (`/goal_pose_rviz` → `nav_goal_relay` → Nav2). Avoid the Nav2 panel goal in sim — short action timeout.

Optional map override:

```bash
ros2 launch amr_navigation navigation.launch.py use_sim_time:=true map:=/path/to/map.yaml
```

## Params

`config/amr_nav2_params.yaml` — fork of `nav2_bringup` Humble params. AMR-specific: `base_footprint`, `/diff_drive_controller/odom`, `/scan`. Controller gains adjusted slightly for goal approach in sim.

## Topics / actions

| Name | Type |
|------|------|
| `/cmd_vel` | out (via velocity_smoother) |
| `/scan` | in (costmaps) |
| `/map` | in |
| `navigate_to_pose` | action |
