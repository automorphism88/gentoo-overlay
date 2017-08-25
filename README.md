# gentoo-overlay
Personal Gentoo overlay, containing a combination of staging ebuilds I'm hoping
to eventually get merged into the official repos, experimental ebuilds that are
too hackish to upstream, and official ebuilds I've modified to reflect my own
preferences.

Packages:

~~app-backup/buttersink  
See https://github.com/AmesCornish/buttersink~~  
Removed after being merged into official Portage tree

app-backup/snapper-gui  
See https://github.com/ricardomv/snapper-gui

app-cdr/{cdemu-daemon,gcdemu} and dev-libs/libmirage)  
Version 3.1.0

app-misc/jdupes  
See https://github.com/jbruchon/jdupes

app-text/calibre  
Gentoo ebuild with USE flags added to toggle system vs bundled
dev-python/beautifulsoup and Gentoo patches removing update dialogs and
disabling plugins. Default behavior is as in official Gentoo ebuild.

dev-java/ecj-gcj  
Modified from official Gentoo version to check in $PATH for gcj if it is not
found in the current gcc profile. This allows the package to be built if the
user is using GCC 7+ (or an earlier version without USE=gcj) as the default, so
long as /etc/portage/package.env is used to put a different gcc version with gcj
in the PATH.

dev-python/html5-parser  
Needed as prerequisite for >=app-text/calibre-3.5.0

games-fps/gzdoom  
See https://zdoom.org/

games-misc/cowsay  
Modified from Gentoo version to keep upstream default of installing cow files to
/usr/share/cows

games-misc/cowsay-files  
See https://github.com/paulkaefer/cowsay-files

games-misc/cowsay-philosoraptor  
See https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/

games-misc/fortune-mod-philosoraptor  
See https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/

sys-boot/grub-btrfs  
See https://github.com/Antynea/grub-btrfs

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-fs/btrfsmaintenance  
Collection of btrfs maintenance scripts from openSUSE. See
https://github.com/kdave/btrfsmaintenance

~~sys-fs/cryfs  
See https://www.cryfs.org~~  
Removed after being merged into official Portage tree

sys-kernel/amdstaging-sources  
Linux kernel based on the amd-staging git tree with DC/DAL support in the
AMDGPU driver, plus the latest minor patch from kernel.org and the
other patches from gentoo-sources (optional, controlled by USE flags).
In the version number, _pre represents the AMD git commit date and _p
represents the genkernel patch number (for Gentoo patches only, since
upstream patches are pulled directly from kernel.org).

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

x11-themes/cloak-theme  
See http://killhellokitty.deviantart.com/art/Cloak-3-20-6-05052016-603341133
