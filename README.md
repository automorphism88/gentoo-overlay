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

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-fs/btrfsmaintenance  
Collection of btrfs maintenance scripts from openSUSE. See
https://github.com/kdave/btrfsmaintenance

sys-fs/cryfs  
See https://www.cryfs.org

sys-kernel/amdstaging-sources  
Linux kernel based on the amd-staging-4.9 git tree with DC/DAL support in the
AMDGPU driver, plus the latest 4.9.x patch from kernel.org (using M-Bab's git
tree, found at https://github.com/M-Bab/linux-kernel-amdgpu), and the other
patches from gentoo-sources (optional, controlled by USE flags).

virtual/linux-sources  
Modified to accept sys-kernel/amdstaging-sources as a dependency
