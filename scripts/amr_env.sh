#!/usr/bin/env bash
# Source this file to mount VMware share (if needed), enter AMR workspace, and load ROS.
# Usage (add to ~/.bashrc):  source /mnt/hgfs/ros2_autonomous_mobile_robot/scripts/amr_env.sh
# Or after local clone:       source ~/robot_project/scripts/amr_env.sh
#
# Typical ~/.bashrc helper:
#   amr() { source "$HOME/robot_project/scripts/amr_env.sh"; }

# --- config (edit if your paths differ) ---
AMR_SHARE_NAME="ros2_autonomous_mobile_robot"
AMR_HGFS_MOUNT="/mnt/hgfs"
AMR_LINK="$HOME/robot_project"

# Resolve workspace root: prefer working symlink, then share path, then link target
_amr_ws=""
if [[ -L "$AMR_LINK" ]] && [[ -d "$AMR_LINK/src" ]]; then
  _amr_ws="$(readlink -f "$AMR_LINK")"
elif [[ -d "$AMR_HGFS_MOUNT/$AMR_SHARE_NAME/src" ]]; then
  _amr_ws="$AMR_HGFS_MOUNT/$AMR_SHARE_NAME"
elif [[ -d "$AMR_LINK/src" ]]; then
  _amr_ws="$(readlink -f "$AMR_LINK" 2>/dev/null || echo "$AMR_LINK")"
fi

# Mount VMware shared folders if the project path is missing
if [[ -z "$_amr_ws" ]] && [[ ! -d "$AMR_HGFS_MOUNT/$AMR_SHARE_NAME" ]]; then
  if [[ ! -d "$AMR_HGFS_MOUNT" ]]; then
    sudo mkdir -p "$AMR_HGFS_MOUNT"
  fi
  if ! mountpoint -q "$AMR_HGFS_MOUNT" 2>/dev/null; then
    echo "[amr] mounting VMware shared folders..."
    sudo vmhgfs-fuse .host:/ "$AMR_HGFS_MOUNT" -o allow_other || {
      echo "[amr] mount failed — enable Shared Folders in VMware VM settings" >&2
      return 1 2>/dev/null || exit 1
    }
  fi
  if [[ -d "$AMR_HGFS_MOUNT/$AMR_SHARE_NAME/src" ]]; then
    _amr_ws="$AMR_HGFS_MOUNT/$AMR_SHARE_NAME"
  fi
fi

if [[ -z "$_amr_ws" ]] || [[ ! -d "$_amr_ws/src" ]]; then
  echo "[amr] workspace not found. Options:" >&2
  echo "  1) VMware: enable Shared Folders for this VM" >&2
  echo "  2) Local:  git clone into ~/robot_project and rebuild" >&2
  return 1 2>/dev/null || exit 1
fi

# Keep ~/robot_project symlink valid
if [[ ! -L "$AMR_LINK" ]] || [[ "$(readlink -f "$AMR_LINK" 2>/dev/null)" != "$_amr_ws" ]]; then
  ln -sfn "$_amr_ws" "$AMR_LINK"
fi

cd "$_amr_ws" || return 1 2>/dev/null || exit 1

if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck source=/dev/null
  source /opt/ros/humble/setup.bash
else
  echo "[amr] ROS Humble not found at /opt/ros/humble" >&2
  return 1 2>/dev/null || exit 1
fi

if [[ -f "$_amr_ws/install/setup.bash" ]]; then
  # shellcheck source=/dev/null
  source "$_amr_ws/install/setup.bash"
else
  echo "[amr] no install/setup.bash — run: colcon build" >&2
fi

export AMR_WS="$_amr_ws"
echo "[amr] ready: $AMR_WS"
