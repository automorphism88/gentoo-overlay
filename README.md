# gentoo-overlay
Personal Gentoo overlay

Packages:

app-backup/buttersink  
See https://github.com/AmesCornish/buttersink

app-backup/snapper-gui  
See https://github.com/ricardomv/snapper-gui

app-text/calibre  
Gentoo ebuild with USE flags added to toggle system vs bundled
dev-python/beautifulsoup and Gentoo patches removing update dialogs and
disabling plugins. Default behavior is as in official Gentoo ebuild. Also
updated to latest version of calibre more quickly than official Gentoo ebuild.

games-misc/cowsay  
Modified from Gentoo version to keep upstream default of installing cow files to
/usr/share/cows

games-misc/cowsay-files  
See https://github.com/paulkaefer/cowsay-files

games-misc/cowsay-philosoraptor  
See https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/

games-misc/fortune-mod-philosoraptor  
See https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/

sys-boot/btrfs  
See https://github.com/Antynea/grub-btrfs

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-fs/btrfsmaintenance  
Collection of btrfs maintenance scripts from openSUSE. See
https://github.com/kdave/btrfsmaintenance

sys-fs/cryfs  
See https://www.cryfs.org

sys-kernel/amdstaging-sources  
Linux kernel based on the amd-staging git tree with DC/DAL support in the
AMDGPU driver, plus the latest 4.9.x patch from kernel.org and the other
patches from gentoo-sources (optional, controlled by USE flags).

sys-kernel/mbab-sources  
Linux kernel based on M-Bab's git tree (found at
https://github.com/M-Bab/linux-kernel-amdgpu) with the DC/DAL support from
the amd-staging kernel.

virtual/linux-sources  
Modified to accept sys-kernel/amdstaging-sources or sys-kernel/mbab-sources
as a dependency

x11-base/xorg-drivers and x11-base/xorg-server  
Xorg version 1.17.4 for use with x11-drivers/ati-drivers (previously removed
from portage tree)

x11-drivers/ati-drivers  
Old closed source fglrx driver for ATI/AMD graphics cards (previously removed
from portage tree, with patches added for kernels up to 4.9)

x11-libs/amd-sdl-sdk and x11-libs/xvba-video  
For use with x11-drivers/ati-drivers (previously removed from portage tree)
