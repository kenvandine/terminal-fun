#!/bin/bash
# Terminal Fun - Sandbox Common Library
# Shared functions for mock commands

# Get the sandbox directory (parent of lib/)
SANDBOX_DIR="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
STATE_DIR="${SANDBOX_DIR}/state"

# Ensure state directory exists
mkdir -p "${STATE_DIR}" 2>/dev/null

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print colored output
print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_info() {
    echo -e "${CYAN}$1${NC}"
}

# Show learning environment message
show_learning_message() {
    local command="$1"
    local description="$2"

    echo ""
    echo -e "${CYAN}+------------------------------------------------------------------+${NC}"
    echo -e "${CYAN}|${NC}  ${BOLD}Terminal Fun - Learning Environment${NC}                           ${CYAN}|${NC}"
    echo -e "${CYAN}+------------------------------------------------------------------+${NC}"
    echo -e "${CYAN}|${NC}                                                                  ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}  This command is not available in the learning environment.     ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}                                                                  ${CYAN}|${NC}"
    if [ -n "$description" ]; then
        # Word wrap the description
        echo "$description" | fold -s -w 62 | while read -r line; do
            printf "${CYAN}|${NC}  %-64s${CYAN}|${NC}\n" "$line"
        done
    fi
    echo -e "${CYAN}|${NC}                                                                  ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}  For safety, this learning environment only simulates           ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}  commands from the exercises.                                   ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}                                                                  ${CYAN}|${NC}"
    echo -e "${CYAN}|${NC}  ${YELLOW}Try following the exercise instructions on the left!${NC}         ${CYAN}|${NC}"
    echo -e "${CYAN}+------------------------------------------------------------------+${NC}"
    echo ""
}

# State file management for APT packages
APT_STATE_FILE="${STATE_DIR}/installed_packages.txt"
SNAP_STATE_FILE="${STATE_DIR}/snap_packages.txt"

# Initialize state files if they don't exist
init_apt_state() {
    if [ ! -f "${APT_STATE_FILE}" ]; then
        cat > "${APT_STATE_FILE}" << 'EOF'
# Base packages (always shown as installed)
adduser
apt
base-files
base-passwd
bash
bsdutils
coreutils
dash
debconf
debianutils
diffutils
dpkg
e2fsprogs
findutils
grep
gzip
hostname
init-system-helpers
libacl1
libapt-pkg6.0
libattr1
libaudit-common
libaudit1
libblkid1
libbz2-1.0
libc-bin
libc6
libcap-ng0
libcap2
libcom-err2
libcrypt1
libdb5.3
libdebconfclient0
libext2fs2
libffi8
libgcc-s1
libgcrypt20
libgmp10
libgnutls30
libgpg-error0
libgssapi-krb5-2
libhogweed6
libidn2-0
libk5crypto3
libkeyutils1
libkrb5-3
libkrb5support0
liblz4-1
liblzma5
libmount1
libncurses6
libncursesw6
libnettle8
libnsl2
libp11-kit0
libpam-modules
libpam-modules-bin
libpam-runtime
libpam0g
libpcre2-8-0
libpcre3
libprocps8
libseccomp2
libselinux1
libsemanage-common
libsemanage2
libsepol2
libsmartcols1
libss2
libssl3
libstdc++6
libsystemd0
libtasn1-6
libtinfo6
libtirpc-common
libtirpc3
libudev1
libunistring2
libuuid1
libxxhash0
libzstd1
login
logsave
lsb-base
mawk
mount
ncurses-base
ncurses-bin
passwd
perl-base
procps
sed
sensible-utils
sysvinit-utils
tar
ubuntu-keyring
usrmerge
util-linux
zlib1g
EOF
    fi
}

init_snap_state() {
    if [ ! -f "${SNAP_STATE_FILE}" ]; then
        cat > "${SNAP_STATE_FILE}" << 'EOF'
# Format: name,version,rev,tracking,publisher,notes
bare,1.0,5,latest/stable,canonical,base
core24,20241210,562,latest/stable,canonical,base
gnome-46-2404,0+git.89a8e32,98,latest/stable,canonical,-
gtk-common-themes,0.1-81-g442e511,1548,latest/stable,canonical,-
snapd,2.67,22458,latest/stable,canonical,snapd
EOF
    fi
}

# Check if an apt package is installed (in our mock state)
is_apt_package_installed() {
    local package="$1"
    init_apt_state
    grep -q "^${package}$" "${APT_STATE_FILE}" 2>/dev/null
}

# Add an apt package to installed state
add_apt_package() {
    local package="$1"
    init_apt_state
    if ! is_apt_package_installed "$package"; then
        echo "$package" >> "${APT_STATE_FILE}"
    fi
}

# Remove an apt package from installed state
remove_apt_package() {
    local package="$1"
    init_apt_state
    if [ -f "${APT_STATE_FILE}" ]; then
        grep -v "^${package}$" "${APT_STATE_FILE}" > "${APT_STATE_FILE}.tmp" 2>/dev/null
        mv "${APT_STATE_FILE}.tmp" "${APT_STATE_FILE}"
    fi
}

# Get list of installed apt packages
get_installed_apt_packages() {
    init_apt_state
    grep -v "^#" "${APT_STATE_FILE}" 2>/dev/null | grep -v "^$" | sort
}

# Check if a snap is installed
is_snap_installed() {
    local snap_name="$1"
    init_snap_state
    grep -q "^${snap_name}," "${SNAP_STATE_FILE}" 2>/dev/null
}

# Add a snap to installed state
add_snap() {
    local snap_name="$1"
    local version="${2:-1.0}"
    local rev="${3:-1}"
    init_snap_state
    if ! is_snap_installed "$snap_name"; then
        echo "${snap_name},${version},${rev},latest/stable,publisher,-" >> "${SNAP_STATE_FILE}"
    fi
}

# Remove a snap from installed state
remove_snap() {
    local snap_name="$1"
    init_snap_state
    if [ -f "${SNAP_STATE_FILE}" ]; then
        grep -v "^${snap_name}," "${SNAP_STATE_FILE}" > "${SNAP_STATE_FILE}.tmp" 2>/dev/null
        mv "${SNAP_STATE_FILE}.tmp" "${SNAP_STATE_FILE}"
    fi
}

# Simulate typing/progress effect
simulate_progress() {
    local message="$1"
    local delay="${2:-0.02}"
    echo -n "$message"
    sleep "$delay"
}

# Random number in range
random_range() {
    local min="$1"
    local max="$2"
    echo $((min + RANDOM % (max - min + 1)))
}

# Generate fake package size
fake_package_size() {
    local size=$((RANDOM % 5000 + 100))
    if [ $size -gt 1000 ]; then
        echo "$((size / 1000)).$((size % 1000 / 100)) MB"
    else
        echo "${size} kB"
    fi
}

# Sleep with slight randomization for realism
realistic_sleep() {
    local base="$1"
    local variance="${2:-0.1}"
    # Use bc if available, otherwise just sleep base time
    if command -v bc &>/dev/null; then
        local actual=$(echo "$base + ($RANDOM % 100) * $variance / 100" | bc -l 2>/dev/null || echo "$base")
        sleep "$actual" 2>/dev/null || sleep "$base"
    else
        sleep "$base" 2>/dev/null || true
    fi
}
