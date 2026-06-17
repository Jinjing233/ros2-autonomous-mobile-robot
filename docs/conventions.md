# Engineering Conventions

Project-wide conventions for the AMR ROS2 platform. All contributors and sprint deliverables must follow these rules.

## Naming

### Package Names

- Prefix all ROS2 packages with `amr_`.
- Use lowercase with underscores: `amr_description`, not `AMR-Description` or `amrDescription`.
- One package per capability domain; do not combine unrelated concerns.

### File and Directory Names

| Type | Convention | Example |
|------|------------|---------|
| Launch files | `{purpose}.launch.py` | `display.launch.py` |
| Parameter files | `{node_or_stack}_params.yaml` | `nav2_params.yaml` |
| URDF/Xacro | `{robot_name}.urdf.xacro` | `amr.urdf.xacro` |
| RViz config | `{purpose}.rviz` | `display.rviz` |
| Gazebo world | `{environment}.world` | `warehouse.world` |

### ROS Graph Names

| Element | Convention | Example |
|---------|------------|---------|
| Topics | Standard names where applicable | `/scan`, `/imu`, `/odom`, `/cmd_vel` |
| TF frames | REP-105 style | `base_link`, `laser_link`, `map`, `odom` |
| Nodes | `{package}_{function}` | `amr_control_teleop` |

## Code Organization

### Within a Package

```
amr_<package>/
├── CMakeLists.txt
├── package.xml
├── README.md
├── config/          # YAML parameter files
├── launch/          # Python launch files
├── urdf/            # Robot description (amr_description only)
├── worlds/          # Gazebo worlds (amr_gazebo only)
├── meshes/          # Visual/collision meshes (amr_description only)
├── rviz/            # RViz configs (amr_description or amr_bringup)
├── src/             # C++ source (when applicable)
└── amr_<package>/   # Python module (when applicable)
```

Create directories only when their sprint deliverable begins — do not add empty placeholder folders.

### Launch Files

- Use **Python launch** (`launch_ros.actions`, `launch.substitutions`).
- Keep launch files declarative; avoid embedded business logic.
- Reference parameters from `config/` YAML files via `PathJoinSubstitution`.
- Compose launches with `IncludeLaunchDescription`; do not duplicate node definitions.

### Parameters

- Store all tunable values in YAML under `config/`.
- Do not hardcode frame names, topic names, or rates in source code when they belong in configuration.
- Document non-obvious parameter choices in the package README or inline YAML comments.

## Build Conventions

- Build system: **ament_cmake** for description, bringup, simulation, and navigation packages.
- Use `colcon build --symlink-install` during active development.
- Declare all dependencies explicitly in `package.xml`; do not rely on transitive dependencies.

## Documentation

- Every package must maintain an up-to-date `README.md` with:
  - **Status:** Implemented / In Progress / Planned / Future
  - **Purpose:** What the package owns
  - **Expected components:** What will be added in upcoming sprints
- Update [milestones.md](milestones.md) when a sprint is completed.
- Update package status in README when work begins or finishes.

## Git Conventions

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable, sprint-complete milestones |
| `develop` | Integration branch (optional) |
| `sprint/<n>-<short-description>` | Sprint feature work |

### Commits

Use imperative mood with a sprint or scope prefix when helpful:

```
sprint-1: add amr base xacro and wheel macros
amr_gazebo: configure lidar plugin for /scan
docs: update milestone status for sprint 2
```

## Testing Conventions (future)

- Lint launch files and validate URDF with `check_urdf` / `xacro` before merging.
- Simulation smoke test: robot spawns, topics publish, teleop moves robot.
- Navigation smoke test: goal pose reached within tolerance in simulation.

## Robot-Specific Constants (planned)

These values will be defined in Sprint 1 Xacro and shared across packages:

| Parameter | Planned location |
|-----------|-----------------|
| Wheel separation | Xacro property |
| Wheel radius | Xacro property |
| Base footprint offset | Xacro / URDF |
| LiDAR mount pose | Xacro |
| IMU mount pose | Xacro |

Downstream packages (Gazebo plugins, controllers, Nav2) must reference these values consistently — never duplicate with conflicting numbers.
