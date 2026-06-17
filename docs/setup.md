# Environment Setup

This guide covers the **primary** development environment: native Ubuntu 22.04 with ROS2 Humble.

Docker support is planned for a future milestone and is **not** part of Sprint 0.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Operating System | Ubuntu 22.04 LTS (Jammy Jellyfish) |
| ROS Distribution | ROS2 Humble Hawksbill |
| Build Tool | colcon |
| Shell | bash (recommended) |

## 1. Install ROS2 Humble

Follow the official installation guide for Ubuntu 22.04:

https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

Recommended packages for this project:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-joint-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-dev-tools
```

> **Note:** Navigation, SLAM, and Gazebo packages are listed here for convenience. They are not used until their respective sprints. You may install them incrementally if you prefer a minimal initial setup.

## 2. Configure ROS2 Environment

Add the following to your `~/.bashrc`:

```bash
source /opt/ros/humble/setup.bash
```

Apply the change:

```bash
source ~/.bashrc
```

## 3. Install colcon and rosdep

```bash
sudo apt install -y python3-colcon-common-extensions python3-rosdep
sudo rosdep init    # skip if already initialized
rosdep update
```

## 4. Clone and Build the Workspace

```bash
git clone <repository-url> ros2-autonomous-mobile-robot
cd ros2-autonomous-mobile-robot
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

## 5. Verify the Build

After Sprint 0, a successful build confirms all package scaffolds are valid:

```bash
colcon build
# Expected: 8 packages built with no errors
```

No launch files or nodes are available yet in Sprint 0.

## 6. IDE Setup (optional)

Recommended tools:

- **VS Code** with the ROS extension
- **RViz2** — available via `ros-humble-desktop` (used from Sprint 1)
- **Gazebo Classic** — available via `ros-humble-gazebo-ros-pkgs` (used from Sprint 2)

## Troubleshooting

### `rosdep install` reports missing keys

Ensure `rosdep update` has been run recently. For packages not yet in rosdep, install dependencies manually when their sprint begins.

### colcon build fails on a fresh clone

Confirm ROS2 Humble is sourced before building:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

### Mixed ROS distributions

Do not source multiple ROS distributions in the same terminal. Use a dedicated terminal or workspace for Humble only.

## Next Steps

After completing setup, refer to [milestones.md](milestones.md) for the sprint roadmap. Sprint 1 will add the robot URDF/Xacro model and RViz visualization.
