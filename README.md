# gentoo-overlay
Personal Gentoo overlay

Packages:

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-fs/cryfs  
See https://www.cryfs.org

sys-kernel/amdstaging-sources  
Linux kernel based on the amd-staging-4.9 git tree with DC/DAL support in the
AMDGPU driver, plus the latest 4.9.x patch from kernel.org and the other patches
from gentoo-sources (optional, controlled by USE flags).

virtual/linux-sources  
Modified to accept sys-kernel/amdstaging-sources as a dependency
