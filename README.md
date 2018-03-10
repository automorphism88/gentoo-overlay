# gentoo-overlay
Personal Gentoo overlay, containing a combination of staging ebuilds I'm hoping
to eventually get merged into the official repos, experimental ebuilds that are
too hackish to upstream, and official ebuilds I've modified to reflect my own
preferences.

## Instructions
You can add this overlay to your system using either the layman method or the
repos.conf method, as described below. You may also need to add the package(s)
you wish to install to `/etc/portage/package.keywords` (see the Gentoo wiki).
### Using layman
```
layman -o https://raw.githubusercontent.com/automorphism88/gentoo-overlay/master/automorphism.xml -f -a automorphism
```
### Using repos.conf
Create a file in `/etc/portage/repos.conf` with the following contents (if it
is a directory, otherwise, add the following to the end of the file):
```
[automorphism]
location = /foo/bar
sync-type = git
sync-uri = https://github.com/automorphism88/gentoo-overlay.git/
auto-sync = yes
```

## Packages

app-backup/snapper-gui  
See https://github.com/ricardomv/snapper-gui

app-backup/snapsync  
See https://github.com/doudou/snapsync/

app-emacs/markdown-preview-mode  
See https://github.com/ancane/markdown-preview-mode

app-emacs/uuidgen  
See https://github.com/kanru/uuidgen-el

app-emacs/web-server  
See https://github.com/eschulte/emacs-web-server

app-emacs/websocket  
See https://github.com/ahyatt/emacs-websocket

app-misc/jdupes  
See https://github.com/jbruchon/jdupes

app-text/acroread  
Old Gentoo ebuild (removed from official portage tree)

app-text/calibre  
Gentoo ebuild with USE flags added to toggle system vs bundled
dev-python/beautifulsoup and Gentoo patches removing update dialogs and
disabling plugins. A USE flag is also available to patch sending deleted
files to the trash out of the source code since the upstream author does
not want to make this configurable. Default behavior is as in official
Gentoo ebuild.

dev-java/ecj-gcj  
Modified from official Gentoo version to check in $PATH for gcj if it is not
found in the current gcc profile. This allows the package to be built if the
user is using GCC 7+ (or an earlier version without USE=gcj) as the default, so
long as /etc/portage/package.env is used to put a different gcc version with gcj
in the PATH.

dev-java/icedtea  
Original icedtea:7 (removed from official tree). Useful for bootstrapping newer
icedtea from gcj.

dev-qt/qtstyleplugins  
See https://code.qt.io/cgit/qt/qtstyleplugins.git/ - needed to use GTK+ style
in Qt 5.7+

dev-ruby/ruby-dbus  
Needed as dependency for app-backup/snapsync

games-fps/{,g,q}zdoom  
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

media-sound/codec2  
See http://www.rowetel.com/?page_id=452

sys-block/nocache
See https://github.com/Feh/nocache

sys-boot/grub-btrfs  
See https://github.com/Antynea/grub-btrfs

sys-boot/grub-customizer  
See https://launchpad.net/grub-customizer

sys-boot/grub  
GRUB2 with openSUSE patches applied (useful for booting into btrfs snapshots).
Controlled via opensuse USE flag, which also requires the multislot USE flag
to be enabled.

sys-fs/btrfsmaintenance  
Collection of btrfs maintenance scripts from openSUSE. See
https://github.com/kdave/btrfsmaintenance

sys-fs/mdadm  
Git version. Also patches Makefile to build and install the 'raid6check' binary.

sys-fs/mergerfs  
See https://www.github.com/trapexit/mergerfs

sys-fs/mergerfs-tools  
See https://github.com/trapexit/mergerfs-tools

sys-fs/snapraid-btrfs  
See https://github.com/automorphism88/snapraid-btrfs

sys-kernel/amdstaging-sources  
Linux kernel 4.9 LTS based on the amd-staging git tree with DC/DAL support in
the AMDGPU driver, plus the latest minor patch from kernel.org and the
other patches from gentoo-sources (optional, controlled by USE flags).
In the version number, _pre represents the AMD git commit date and _p
represents the genkernel patch number (for Gentoo patches only, since
upstream patches are pulled directly from kernel.org).

sys-kernel/dracut-crypt-ssh  
See https://github.com/dracut-crypt-ssh/dracut-crypt-ssh

sys-kernel/earlyoom  
See https://github.com/rfjakob/earlyoom

virtual/linux-sources  
Modified to accept sys-kernel/amdstaging-sources as a dependency

x11-base/xorg-drivers and x11-base/xorg-server  
Xorg version 1.17.4 for use with x11-drivers/ati-drivers (previously removed
from portage tree)

x11-drivers/ati-drivers  
Old closed source fglrx driver for ATI/AMD graphics cards (previously removed
from portage tree, with patches added for kernels up to 4.14 - may work with
newer kernels, but has not been tested and may require further patching)

x11-libs/amd-sdl-sdk and x11-libs/xvba-video  
For use with x11-drivers/ati-drivers (previously removed from portage tree)

x11-misc/awf  
A Widget Factory - theme preview application for GTK+2 and GTK+3
(see https://github.com/valr/awf)

x11-themes/cloak-theme  
See http://killhellokitty.deviantart.com/art/Cloak-3-20-6-05052016-603341133

I also proxy maintain the following ebuilds in the official portage tree which
originated from this overlay:

app-backup/buttersink  
See https://github.com/AmesCornish/buttersink  
Removed after being merged into official Portage tree

sys-fs/cryfs  
See https://www.cryfs.org  
Removed after being merged into official Portage tree
