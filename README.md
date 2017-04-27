# gentoo-overlay
Personal Gentoo overlay

Packages:

app-backup/buttersink  
See https://github.com/AmesCornish/buttersink

app-text/calibre  
Gentoo ebuild with a USE flag added to toggle system vs bundled
dev-python/beautifulsoup. Also updated to latest version of calibre more
quickly than official Gentoo ebuild.

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-fs/cryfs  
See https://www.cryfs.org

sys-kernel/amdstaging-sources  
Linux kernel based on the amd-staging-4.9 git tree with DC/DAL support in the
AMDGPU driver, plus the latest 4.9.x patch from kernel.org (using M-Bab's git
tree, found at https://github.com/M-Bab/linux-kernel-amdgpu), and the other
patches from gentoo-sources (optional, controlled by USE flags).

virtual/linux-sources  
Modified to accept sys-kernel/amdstaging-sources as a dependency
