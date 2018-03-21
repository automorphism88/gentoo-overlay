#
# spec file for package grub2
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# needssslcertforbuild


Name:           grub2
%ifarch x86_64 ppc64
BuildRequires:  gcc-32bit
BuildRequires:  glibc-32bit
BuildRequires:  glibc-devel-32bit glibc-32bit
%else
BuildRequires:  gcc
BuildRequires:  glibc-devel
%endif
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  dejavu-fonts
BuildRequires:  device-mapper-devel
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  freetype2-devel
BuildRequires:  fuse-devel
%if 0%{?suse_version} >= 1140
BuildRequires:  gnu-unifont
%endif
BuildRequires:  help2man
BuildRequires:  xz
%if 0%{?suse_version} >= 1210
BuildRequires:  makeinfo
%else
BuildRequires:  texinfo
%endif
BuildRequires:  python3
BuildRequires:  xz-devel
%ifarch x86_64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
BuildRequires:  openssl >= 0.9.8
BuildRequires:  pesign-obs-integration
%endif
%endif
%if 0%{?suse_version} >= 1210
# Package systemd services files grub2-once.service
BuildRequires:  systemd-rpm-macros
%define has_systemd 1
%endif
%if 0%{?suse_version} > 1320
BuildRequires:  update-bootloader-rpm-macros
%endif

# Modules code is dynamically loaded and collected from a _fixed_ path.
%define _libdir %{_exec_prefix}/lib

# Build grub2-emu everywhere (it may be "required" by 'grub2-once')
%define emu 1

%ifarch ppc ppc64 ppc64le
%define grubcpu powerpc
%define platform ieee1275
# emu does not build here yet... :-(
%define emu 0
%endif

%ifarch %{ix86} x86_64
%define grubcpu i386
%define platform pc
%endif

%ifarch s390x
%define grubcpu s390x
%define platform emu
%endif

%ifarch %{arm}
%define grubcpu arm
%define platform uboot
%endif

%ifarch aarch64
%define grubcpu arm64
%define platform efi
%define only_efi 1
%endif

%define grubarch %{grubcpu}-%{platform}

# build efi bootloader on some platforms only:
%if ! 0%{?efi:1}
%global efi %{ix86} x86_64 ia64 aarch64 %{arm}
%endif

%ifarch %{efi}
%ifarch %{ix86}
%define grubefiarch i386-efi
%else
%ifarch aarch64
%define grubefiarch arm64-efi
%else
%ifarch %{arm}
%define grubefiarch arm-efi
%else
%define grubefiarch %{_target_cpu}-efi
%endif
%endif
%endif
%endif

%ifarch %{ix86}
%define grubxenarch i386-xen
%endif

%ifarch x86_64
%define grubxenarch x86_64-xen
%endif

%if %{platform} == emu
# force %{emu} to 1, e.g. for s390
%define emu 1
%endif

%if 0%{?suse_version} == 1110
%define only_efi %{nil}
%define only_x86_64 %{nil}
%endif

Version:        2.02
Release:        26.9
Summary:        Bootloader with support for Linux, Multiboot and more
License:        GPL-3.0+
Group:          System/Boot
Url:            http://www.gnu.org/software/grub/
%define rev 20120622
Source0:        grub-%{version}.tar.xz
Source1:        90_persistent
Source2:        grub.default
Source4:        grub2.rpmlintrc
# rsync -Lrtvz  translationproject.org::tp/latest/grub/ po
Source5:        translations-20170427.tar.xz
Source6:        grub2-once
Source7:        20_memtest86+
Source8:        README.ibm3215
Source10:       openSUSE-UEFI-CA-Certificate.crt
Source11:       SLES-UEFI-CA-Certificate.crt
Source12:       grub2-snapper-plugin.sh
Source14:       80_suse_btrfs_snapshot
Source15:       grub2-once.service
Source16:       grub2-xen-pv-firmware.cfg
# required hook for systemd-sleep (bsc#941758)
Source17:       grub2-systemd-sleep.sh
Source18:       grub2-check-default.sh
Source1000:     PATCH_POLICY
Patch1:         rename-grub-info-file-to-grub2.patch
Patch2:         grub2-linux.patch
Patch3:         use-grub2-as-a-package-name.patch
Patch4:         info-dir-entry.patch
Patch6:         grub2-iterate-and-hook-for-extended-partition.patch
Patch8:         grub2-ppc-terminfo.patch
Patch9:         grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
Patch10:        grub2-fix-error-terminal-gfxterm-isn-t-found.patch
Patch11:        grub2-fix-build-with-flex-2.6.4.patch
Patch12:        grub2-fix-menu-in-xen-host-server.patch
Patch15:        not-display-menu-when-boot-once.patch
Patch17:        grub2-pass-corret-root-for-nfsroot.patch
Patch18:        grub2-fix-locale-en.mo.gz-not-found-error-message.patch
Patch19:        grub2-efi-HP-workaround.patch
Patch21:        grub2-secureboot-add-linuxefi.patch
Patch22:        grub2-secureboot-use-linuxefi-on-uefi.patch
Patch23:        grub2-secureboot-no-insmod-on-sb.patch
Patch24:        grub2-secureboot-provide-linuxefi-config.patch
Patch25:        grub2-secureboot-chainloader.patch
Patch26:        grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch
Patch27:        grub2-linuxefi-fix-boot-params.patch
Patch35:        grub2-linguas.sh-no-rsync.patch
Patch37:        grub2-use-Unifont-for-starfield-theme-terminal.patch
Patch38:        grub2-s390x-01-Changes-made-and-files-added-in-order-to-allow-s390x.patch
Patch39:        grub2-s390x-02-kexec-module-added-to-emu.patch
Patch40:        grub2-s390x-03-output-7-bit-ascii.patch
Patch41:        grub2-s390x-04-grub2-install.patch
Patch42:        grub2-s390x-05-grub2-mkconfig.patch
Patch43:        grub2-use-rpmsort-for-version-sorting.patch
Patch53:        grub2-getroot-treat-mdadm-ddf-as-simple-device.patch
Patch56:        grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
Patch58:        grub2-xen-linux16.patch
Patch59:        grub2-efi-disable-video-cirrus-and-bochus.patch
Patch60:        grub2-editenv-add-warning-message.patch
Patch61:        grub2-vbe-blacklist-preferred-1440x900x32.patch
Patch64:        grub2-grubenv-in-btrfs-header.patch
Patch65:        grub2-mkconfig-aarch64.patch
Patch70:        grub2-default-distributor.patch
Patch71:        grub2-menu-unrestricted.patch
Patch72:        grub2-mkconfig-arm.patch
Patch74:        grub2-accept-empty-module.patch
Patch75:        grub2-s390x-06-loadparm.patch
Patch76:        grub2-s390x-07-add-image-param-for-zipl-setup.patch
Patch77:        grub2-s390x-08-workaround-part-to-disk.patch
Patch78:        grub2-commands-introduce-read_file-subcommand.patch
Patch79:        grub2-efi-chainload-harder.patch
Patch80:        grub2-emu-4-all.patch
Patch81:        grub2-lvm-allocate-metadata-buffer-from-raw-contents.patch
Patch82:        grub2-diskfilter-support-pv-without-metadatacopies.patch
Patch83:        grub2-efi-uga-64bit-fb.patch
Patch84:        grub2-s390x-09-improve-zipl-setup.patch
Patch85:        grub2-install-remove-useless-check-PReP-partition-is-empty.patch
Patch86:        grub2-getroot-scan-disk-pv.patch
# Btrfs snapshot booting related patches
Patch101:       grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
Patch102:       grub2-btrfs-02-export-subvolume-envvars.patch
Patch103:       grub2-btrfs-03-follow_default.patch
Patch104:       grub2-btrfs-04-grub2-install.patch
Patch105:       grub2-btrfs-05-grub2-mkconfig.patch
Patch106:       grub2-btrfs-06-subvol-mount.patch
Patch107:       grub2-btrfs-07-subvol-fallback.patch
Patch108:       grub2-btrfs-08-workaround-snapshot-menu-default-entry.patch
Patch109:       grub2-btrfs-09-get-default-subvolume.patch
# Support EFI xen loader
Patch120:       grub2-efi-xen-chainload.patch
Patch121:       grub2-efi-chainloader-root.patch
Patch122:       grub2-efi-xen-cmdline.patch
Patch123:       grub2-efi-xen-cfg-unquote.patch
# Hidden menu entry and hotkey "t" for text console
Patch140:       grub2-Add-hidden-menu-entries.patch
Patch141:       grub2-SUSE-Add-the-t-hotkey.patch
# EFI free memory on exit fix (bsc#980739)
Patch150:       grub2-efi-Move-grub_reboot-into-kernel.patch
Patch151:       grub2-efi-Free-malloc-regions-on-exit.patch
# Linux root device related patches
Patch163:       grub2-zipl-setup-fix-btrfs-multipledev.patch
Patch164:       grub2-suse-remove-linux-root-param.patch
# PPC64 LE support
Patch205:       grub2-ppc64le-disable-video.patch
Patch207:       grub2-ppc64le-memory-map.patch
Patch233:       grub2-use-stat-instead-of-udevadm-for-partition-lookup.patch
Patch234:       fix-grub2-use-stat-instead-of-udevadm-for-partition-lookup-with-new-glibc.patch
Patch235:       0002-Add-Virtual-LAN-support.patch 
Patch236:       grub2-efi_gop-avoid-low-resolution.patch
Patch277:       grub2-ppc64-cas-reboot-support.patch
# Support HTTP Boot IPv4 and IPv6 (fate#320129)
Patch280:       0001-misc-fix-invalid-character-recongition-in-strto-l.patch
Patch281:       0002-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
Patch282:       0003-bootp-New-net_bootp6-command.patch
Patch283:       0004-efinet-UEFI-IPv6-PXE-support.patch
Patch284:       0005-grub.texi-Add-net_bootp6-doument.patch
Patch285:       0006-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
Patch286:       0007-efinet-Setting-network-from-UEFI-device-path.patch
Patch287:       0008-efinet-Setting-DNS-server-from-UEFI-protocol.patch
# Fix GOP BLT support (FATE#322332)
Patch311:       grub2-efi-gop-add-blt.patch
# TPM Support (FATE#315831)
Patch400:       0001-tpm-Core-TPM-support.patch
Patch401:       0002-tpm-Measure-kernel-initrd.patch
Patch402:       0003-tpm-Add-BIOS-boot-measurement.patch
Patch403:       0004-tpm-Rework-linux-command.patch
Patch404:       0005-tpm-Rework-linux16-command.patch
Patch405:       0006-tpm-Measure-kernel-and-initrd-on-BIOS-systems.patch
Patch406:       0007-tpm-Measure-the-kernel-commandline.patch
Patch407:       0008-tpm-Measure-commands.patch
Patch408:       0009-tpm-Measure-multiboot-images-and-modules.patch
Patch409:       0010-tpm-Fix-boot-when-there-s-no-TPM.patch
Patch410:       0011-tpm-Fix-build-error.patch
Patch411:       0012-tpm-Build-tpm-as-module.patch
Patch412:       0013-tpm-i386-pc-diskboot-img.patch
# UEFI HTTP and related network protocol support (FATE#320130)
Patch420:       0001-add-support-for-UEFI-network-protocols.patch
Patch421:       0002-AUDIT-0-http-boot-tracker-bug.patch
# check if default entry need to be corrected for updated distributor version 
# and/or use fallback entry if default kernel entry removed (bsc#1065349)
Patch430:       grub2-mkconfig-default-entry-correction.patch

Requires:       gettext-runtime
%if 0%{?suse_version} >= 1140
%ifnarch s390x
Recommends:     os-prober
%endif
# xorriso not available using grub2-mkrescue (bnc#812681)
Recommends:     libburnia-tools
Recommends:     mtools
%endif
Requires(post): /sbin/install-info
Requires(preun):/sbin/install-info
%if ! 0%{?only_efi:1}
Requires:       grub2-%{grubarch} = %{version}-%{release}
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if 0%{?only_x86_64:1}
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{ix86} x86_64 ppc ppc64 ppc64le s390x aarch64 %{arm}
%endif

%description
This is the second version of the GRUB (Grand Unified Bootloader), a
highly configurable and customizable bootloader with modular
architecture.  It support rich scale of kernel formats, file systems,
computer architectures and hardware devices.

This package includes user space utlities to manage GRUB on your system.


Authors:
--------
    Gordon Matzigkeit
    Yoshinori K. Okuji
    Colin Watson
    Colin D. Bennett
    Vesa Jääskeläinen
    Robert Millan
    Carles Pina

%package branding-upstream

Summary:        Upstream branding for GRUB2's graphical console
Group:          System/Fhs
Requires:       %{name} = %{version}-%{release}

%description branding-upstream
Upstream branding for GRUB2's graphical console

%if ! 0%{?only_efi:1}
%package %{grubarch}

Summary:        Bootloader with support for Linux, Multiboot and more
Group:          System/Boot
Requires:       %{name} = %{version}-%{release}
Requires(post):	%{name} = %{version}-%{release}
%if 0%{?update_bootloader_requires:1}
%update_bootloader_requires
%else
Requires:       perl-Bootloader
Requires(post): perl-Bootloader
%endif
%ifarch s390x
# required utilities by grub2-s390x-04-grub2-install.patch
# use 'showconsole' to determine console device. (bnc#876743)
Requires:       /sbin/showconsole
Requires:       kexec-tools
# for /sbin/zipl used by grub2-zipl-setup
Requires:       s390-tools
%endif
%ifarch ppc64 ppc64le
Requires:       powerpc-utils
%endif

%description %{grubarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for %{platform} systems.

%endif

%ifarch %{efi}

%package %{grubefiarch}

Summary:        Bootloader with support for Linux, Multiboot and more
# Require efibootmgr
# Without it grub-install is broken so break the package as well if unavailable
Group:          System/Boot
Requires:       efibootmgr
Requires(post): efibootmgr
Requires:       %{name} = %{version}-%{release}
Requires(post):	%{name} = %{version}-%{release}
%if 0%{?update_bootloader_requires:1}
%update_bootloader_requires
%else
Requires:       perl-Bootloader >= 0.706
Requires(post): perl-Bootloader >= 0.706
%endif
Provides:       %{name}-efi = %{version}-%{release}
Obsoletes:      %{name}-efi < %{version}-%{release}

%description %{grubefiarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.

%endif

%ifarch %{ix86} x86_64

%package %{grubxenarch}

Summary:        Bootloader with support for Linux, Multiboot and more
Group:          System/Boot
Provides:       %{name}-xen = %{version}-%{release}
Obsoletes:      %{name}-xen < %{version}-%{release}

%description %{grubxenarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for XEN systems.

%endif

%package snapper-plugin

Summary:        Grub2's snapper plugin
Group:          System/Fhs
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-tools
Supplements:    packageand(snapper:grub2)
BuildArch:      noarch

%description snapper-plugin
Grub2's snapper plugin for advanced btrfs snapshot boot menu management

%if 0%{?has_systemd:1}
%package systemd-sleep-plugin

Summary:        Grub2's systemd-sleep plugin
Group:          System/Fhs
Requires:       grub2
Requires:       util-linux
Supplements:    packageand(systemd:grub2)
BuildArch:      noarch

%description systemd-sleep-plugin
Grub2's systemd-sleep plugin for directly booting hibernated kernel image in
swap partition while in resuming
%endif

%prep
# We create (if we build for efi) two copies of the sources in the Builddir
%setup -q -n grub-%{version} -a 5
(cd po && ls *.po | cut -d. -f1 | xargs) >po/LINGUAS
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch15 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch35 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch53 -p1
%patch56 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch64 -p1
%patch65 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch140 -p1
%patch141 -p1
%patch150 -p1
%patch151 -p1
%patch163 -p1
%patch164 -p1
%patch205 -p1
%patch207 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1
%patch236 -p1
%patch277 -p1
%patch280 -p1
%patch281 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch285 -p1
%patch286 -p1
%patch287 -p1
%patch311 -p1
%patch400 -p1
%patch401 -p1
%patch402 -p1
%patch403 -p1
%patch404 -p1
%patch405 -p1
%patch406 -p1
%patch407 -p1
%patch408 -p1
%patch409 -p1
%patch410 -p1
%patch411 -p1
%patch412 -p1
%patch420 -p1
%patch421 -p1
%patch430 -p1

%build
# patches above may update the timestamp of grub.texi
# and via build-aux/mdate-sh they end up in grub2.info, breaking build-compare
[ -z "$SOURCE_DATE_EPOCH" ] ||\
  [ `stat -c %Y docs/grub.texi` -lt $SOURCE_DATE_EPOCH ] ||\
  touch -d@$SOURCE_DATE_EPOCH docs/grub.texi

# This simplifies patch handling without need to use git to create patch
# that renames file
mv docs/grub.texi docs/grub2.texi
# This avoids attempt to rebuild potfiles which fails because necessary
# sources are not included in tarball
mv po/grub.pot po/%{name}.pot

# Generate po/LINGUAS for message catalogs ...
./linguas.sh
# ... and make sure new catalogs are actually created
rm -f po/stamp-po

cp %{SOURCE8} .
mkdir build
%ifarch %{efi}
mkdir build-efi
%endif
%ifarch %{ix86} x86_64
mkdir build-xen
%endif
%if %{emu}
mkdir build-emu
%endif

export PYTHON=%{_bindir}/python3
# autogen calls autoreconf -vi
./autogen.sh
# Not yet:
%define common_conf_options TARGET_LDFLAGS=-static --program-transform-name=s,grub,%{name},
# This does NOT work on SLE11:
%define _configure ../configure

# We don't want to let rpm override *FLAGS with default a.k.a bogus values.
CFLAGS="-fno-strict-aliasing -fno-inline-functions-called-once "
CXXFLAGS=" "
FFLAGS=" "
export CFLAGS CXXFLAGS FFLAGS

%if %{emu}
cd build-emu
%define arch_specific --enable-device-mapper --disable-grub-mount
TFLAGS="-fPIC"

# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
../configure TARGET_LDFLAGS=$TFLAGS     \
	--prefix=%{_prefix}		\
	--sysconfdir=%{_sysconfdir}	\
        --target=%{_target_platform}    \
        --with-platform=emu     \
	%{arch_specific}                \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}
cd ..
if [ "%{platform}" = "emu" ]; then
  rmdir build
  mv build-emu build
fi
%endif

%ifarch %{ix86} x86_64
cd build-xen
../configure                           \
        TARGET_LDFLAGS=-static         \
        --prefix=%{_prefix}            \
        --sysconfdir=%{_sysconfdir}    \
        --target=%{_target_platform}   \
        --libdir=%{_libdir}            \
        --with-platform=xen            \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}

./grub-mkstandalone --grub-mkimage=./grub-mkimage -o grub.xen -O %{grubxenarch} -d grub-core/ "/boot/grub/grub.cfg=%{SOURCE16}"

cd ..
%endif

%ifarch %{efi}
cd build-efi
../configure   				                \
        TARGET_LDFLAGS=-static                          \
	--prefix=%{_prefix}				\
	--sysconfdir=%{_sysconfdir}			\
        --target=%{_target_platform}                    \
        --libdir=%{_libdir}                          \
        --with-platform=efi                             \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}

#TODO: add efifwsetup module

FS_MODULES="ext2 btrfs ext2 xfs jfs reiserfs"
CD_MODULES=" all_video boot cat chain configfile echo true \
		efinet font gfxmenu gfxterm gzio halt iso9660 \
		jpeg minicmd normal part_apple part_msdos part_gpt \
		password_pbkdf2 png reboot search search_fs_uuid \
		search_fs_file search_label sleep test video fat loadenv"
PXE_MODULES="efinet tftp http"
CRYPTO_MODULES="luks gcry_rijndael gcry_sha1 gcry_sha256"

%ifarch x86_64
CD_MODULES="${CD_MODULES} linuxefi" 
%else
CD_MODULES="${CD_MODULES} linux" 
%endif

GRUB_MODULES="${CD_MODULES} ${FS_MODULES} ${PXE_MODULES} ${CRYPTO_MODULES} mdraid09 mdraid1x lvm serial"
./grub-mkimage -O %{grubefiarch} -o grub.efi --prefix= \
		-d grub-core ${GRUB_MODULES}
./grub-mkimage -O %{grubefiarch} -o grub-tpm.efi --prefix= \
		-d grub-core ${GRUB_MODULES} tpm
#./grub-mkimage -O %{grubefiarch} -o grub.efi -d grub-core part_gpt hfsplus fat \
#        ext2 btrfs normal chain boot configfile linux appleldr minicmd \
#        loadbios reboot halt search font gfxterm

%ifarch x86_64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
if test -e %{_sourcedir}/_projectcert.crt ; then
    prjsubject=$(openssl x509 -in %{_sourcedir}/_projectcert.crt -noout -subject_hash)
    prjissuer=$(openssl x509 -in %{_sourcedir}/_projectcert.crt -noout -issuer_hash)
    opensusesubject=$(openssl x509 -in %{SOURCE10} -noout -subject_hash)
    slessubject=$(openssl x509 -in %{SOURCE11} -noout -subject_hash)
    if test "$prjissuer" = "$opensusesubject" ; then
        cert=%{SOURCE10}
    fi
    if test "$prjissuer" = "$slessubject" ; then
        cert=%{SOURCE11}
    fi
    if test "$prjsubject" = "$prjissuer" ; then
        cert=%{_sourcedir}/_projectcert.crt
    fi
fi
if test -z "$cert" ; then
    echo "cannot identify project, assuming openSUSE signing"
    cert=%{SOURCE10}
fi

openssl x509 -in $cert -outform DER -out grub.der
%endif
%endif

cd ..
%endif

%if ! 0%{?only_efi:1}
cd build

# 64-bit x86-64 machines use 32-bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64 
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if %{platform} != "emu"
%define arch_specific --enable-device-mapper
TFLAGS="-static"

# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
../configure TARGET_LDFLAGS=$TFLAGS     \
	--prefix=%{_prefix}		\
	--sysconfdir=%{_sysconfdir}	\
        --target=%{_target_platform}    \
        --with-platform=%{platform}     \
	%{arch_specific}                \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}
%endif
cd ..
%endif

%install

%ifarch %{ix86} x86_64
cd build-xen
make DESTDIR=$RPM_BUILD_ROOT install
install -m 644 grub.xen $RPM_BUILD_ROOT%{_libdir}/%{name}/%{grubxenarch}/.
cd ..
%endif

%ifarch %{efi}
cd build-efi
make DESTDIR=$RPM_BUILD_ROOT install

install -m 644 grub.efi grub-tpm.efi $RPM_BUILD_ROOT%{_libdir}/%{name}/%{grubefiarch}/.

# Create grub.efi link to system efi directory
# This is for tools like kiwi not fiddling with the path
%if "%{grubefiarch}" == "x86_64-efi"
%define sysefidir %{_exec_prefix}/lib64/efi
%else
%define sysefidir %{_libdir}/efi
%endif
install -d $RPM_BUILD_ROOT%{sysefidir}
ln -sf ../../../%{_libdir}/%{name}/%{grubefiarch}/grub.efi $RPM_BUILD_ROOT%{sysefidir}/grub.efi

%ifarch x86_64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
export BRP_PESIGN_FILES="%{_libdir}/%{name}/%{grubefiarch}/grub.efi %{_libdir}/%{name}/%{grubefiarch}/grub-tpm.efi"
install -m 444 grub.der $RPM_BUILD_ROOT%{sysefidir}/
%endif
%endif

cd ..
%endif

%if ! 0%{?only_efi:1}
cd build
make DESTDIR=$RPM_BUILD_ROOT install
cd ..
%endif

if [ -d build-emu/grub-core ]; then
  cd build-emu/grub-core
  install -m 755 grub-emu $RPM_BUILD_ROOT%{_bindir}/%{name}-emu
  install -m 755 grub-emu-lite $RPM_BUILD_ROOT%{_bindir}/%{name}-emu-lite
  install -m 644 grub-emu.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}-emu.1
  cd ../..
fi

# *.module files are installed with executable bits due to the way grub2 build
# system works. Clear executable bits to not confuse find-debuginfo.sh
find $RPM_BUILD_ROOT%{_libdir}/%{name} \
       \( -name '*.module' -o -name '*.image' -o -name '*.exec' \) -print0 | \
       xargs --no-run-if-empty -0 chmod a-x

# Script that makes part of grub.cfg persist across updates
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/

# Script to generate memtest86+ menu entry
install -m 755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg

# Remove devel files
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}/*/*.h
%if 0%{?suse_version} >= 1140
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/*.h
%endif

# Defaults
install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/grub
install -m 755 -D %{SOURCE6} $RPM_BUILD_ROOT%{_sbindir}/grub2-once
install -m 755 -D %{SOURCE12} $RPM_BUILD_ROOT%{_libdir}/snapper/plugins/grub
install -m 755 -D %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/80_suse_btrfs_snapshot
%if 0%{?has_systemd:1}
install -m 644 -D %{SOURCE15} $RPM_BUILD_ROOT%{_unitdir}/grub2-once.service
install -m 755 -D %{SOURCE17} $RPM_BUILD_ROOT%{_libdir}/systemd/system-sleep/grub2.sleep
%endif
install -m 755 -D %{SOURCE18} $RPM_BUILD_ROOT%{_sbindir}/grub2-check-default

R=$RPM_BUILD_ROOT
%ifarch %{ix86} x86_64
%else
rm -f $R%{_sysconfdir}/grub.d/20_memtest86+
%endif

%ifarch ppc ppc64 ppc64le
%else
rm -f $R%{_sysconfdir}/grub.d/20_ppc_terminfo
%endif

%ifarch s390x
mv $R%{_sysconfdir}/{grub.d,default}/zipl2grub.conf.in
chmod 600 $R%{_sysconfdir}/default/zipl2grub.conf.in

%define dracutlibdir %{_prefix}/lib/dracut
%define dracutgrubmoddir %{dracutlibdir}/modules.d/99grub2
install -m 755 -d $R%{dracutgrubmoddir}
for f in module-setup.sh grub2.sh; do
  mv $R%{_libdir}/%{name}/%{grubarch}/dracut-$f $R%{dracutgrubmoddir}/$f
done
rm -f $R%{_sysconfdir}/grub.d/30_os-prober

perl -ni -e '
  sub END() {
    print "\n# on s390x always:\nGRUB_DISABLE_OS_PROBER=true\n";
  }
  if ( s{^#(GRUB_DISABLE_LINUX_RECOVERY)=\"?(true)\"?}{$1=$2} ) {
    $_ .= "GRUB_DISABLE_RECOVERY=true\n";
  }
  if ( s{^#?(GRUB_TERMINAL)=(console|gfxterm)}{$1=console} ) {
    $_ .= "GRUB_GFXPAYLOAD_LINUX=text\n";
  }
  if (	m{^# The resolution used on graphical} ||
	m{^# # note that you can use only modes} ||
	m{^# you can see them in real GRUB} ||
	m{^#?GRUB_GFXMODE=} ) {
    next;
  }
  s{openSUSE}{SUSE Linux Enterprise Server} if (m{^GRUB_DISTRIBUTOR});
  print;
'  $RPM_BUILD_ROOT%{_sysconfdir}/default/grub
%else
%endif

%find_lang %{name}
%fdupes %buildroot%{_bindir}
%fdupes %buildroot%{_libdir}

%pre
%service_add_pre grub2-once.service

%post
%service_add_post grub2-once.service
/sbin/install-info %{_infodir}/grub-dev.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%if ! 0%{?only_efi:1}

%post %{grubarch}
%if 0%{?update_bootloader_check_type_reinit_post:1} 
%update_bootloader_check_type_reinit_post grub2
%else
# To check by current loader settings
if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
  . %{_sysconfdir}/sysconfig/bootloader
fi

# If the grub is the current loader, we'll handle the grub2 testing entry
if [ "x${LOADER_TYPE}" = "xgrub" ]; then

  exec >/dev/null 2>&1

  # check if entry for grub2's core.img exists in the config
  # if yes, we will correct obsoleted path and update grub2 stuff and config to make it work
  # if no, do nothing
  if [ -f /boot/grub/menu.lst ]; then

    # If grub config contains obsolete core.img path, remove and use the new one
    if /usr/bin/grep -l "^\s*kernel\s*.*/boot/%{name}/core.img" /boot/grub/menu.lst; then
      /sbin/update-bootloader --remove --image /boot/%{name}/core.img || true
      /sbin/update-bootloader --add --image /boot/%{name}/i386-pc/core.img --name "GNU GRUB 2" || true
    fi

    # Install grub2 stuff and config to make the grub2 testing entry to work with updated version
    if /usr/bin/grep -l "^\s*kernel\s*.*/boot/%{name}/i386-pc/core.img" /boot/grub/menu.lst; then
      # Determine the partition with /boot
      BOOT_PARTITION=$(df -h /boot | sed -n '2s/[[:blank:]].*//p')
      # Generate core.img, but don't let it be installed in boot sector
      %{name}-install --no-bootsector $BOOT_PARTITION || true
      # Create a working grub2 config, otherwise that entry is un-bootable
      /usr/sbin/grub2-mkconfig -o /boot/%{name}/grub.cfg
    fi
  fi

elif [ "x${LOADER_TYPE}" = "xgrub2" ]; then

  # It's enought to call update-bootloader to install grub2 and update it's config
  # Use new --reinit, if not available use --refresh
  # --reinit: install and update bootloader config
  # --refresh: update bootloader config
  /sbin/update-bootloader --reinit 2>&1 | grep -q 'Unknown option: reinit' &&
  /sbin/update-bootloader --refresh || true
fi
%endif

%posttrans %{grubarch}
%{?update_bootloader_posttrans}

%endif

%ifarch %{efi}

%post %{grubefiarch}
%if 0%{?update_bootloader_check_type_reinit_post:1} 
%update_bootloader_check_type_reinit_post grub2-efi
%else
# To check by current loader settings
if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
  . %{_sysconfdir}/sysconfig/bootloader
fi

if [ "x${LOADER_TYPE}" = "xgrub2-efi" ]; then

  if [ -d /boot/%{name}-efi ]; then
    # Migrate settings to standard prefix /boot/grub2
    for i in custom.cfg grubenv; do
      [ -f /boot/%{name}-efi/$i ] && cp -a /boot/%{name}-efi/$i /boot/%{name} || :
    done

  fi

  # It's enough to call update-bootloader to install grub2 and update it's config
  # Use new --reinit, if not available use --refresh
  # --reinit: install and update bootloader config
  # --refresh: update bootloader config
  /sbin/update-bootloader --reinit 2>&1 | grep -q 'Unknown option: reinit' &&
  /sbin/update-bootloader --refresh || true
fi

if [ -d /boot/%{name}-efi ]; then
  mv /boot/%{name}-efi /boot/%{name}-efi.rpmsave
fi

exit 0
%endif

%posttrans %{grubefiarch}
%{?update_bootloader_posttrans}

%endif

%preun
%service_del_preun grub2-once.service
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/grub-dev.info %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :

# We did not add core.img to grub1 menu.lst in new update-bootloader macro as what
# the old %post ever did, then the %preun counterpart which removed the added core.img
# entry from old %post can be skipped entirely if having new macro in use.
%if ! 0%{?update_bootloader_posttrans:1}%{?only_efi:1}
  # To check by current loader settings
  if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
    . %{_sysconfdir}/sysconfig/bootloader
  fi

  if [ "x${LOADER_TYPE}" = "xgrub" ]; then

    exec >/dev/null 2>&1

    if [ -f /boot/grub/menu.lst ]; then

      # Remove grub2 testing entry in menu.lst if has any
      for i in /boot/%{name}/core.img /boot/%{name}/i386-pc/core.img; do
        if /usr/bin/grep -l "^\s*kernel\s*.*$i" /boot/grub/menu.lst; then
          /sbin/update-bootloader --remove --image "$i" || true
        fi
      done
    fi

    # Cleanup config, to not confuse some tools determining bootloader in use
    rm -f /boot/%{name}/grub.cfg

    # Cleanup installed files
    # Unless grub2 provides grub2-uninstall, we don't remove any file because
    # we have no idea what's been installed. (And a blind remove is dangerous
    # to remove user's or other package's file accidently ..)
  fi
%endif
fi

%postun
%service_del_postun grub2-once.service

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NEWS README
%doc THANKS TODO ChangeLog
%doc docs/autoiso.cfg docs/osdetect.cfg
%ifarch s390x
%doc README.ibm3215
%endif
%dir /boot/%{name}
%ghost /boot/%{name}/grub.cfg
%{_sysconfdir}/bash_completion.d/grub
%config(noreplace) %{_sysconfdir}/default/grub
%dir %{_sysconfdir}/grub.d
%{_sysconfdir}/grub.d/README
%config %{_sysconfdir}/grub.d/00_header
%config %{_sysconfdir}/grub.d/10_linux
%config %{_sysconfdir}/grub.d/20_linux_xen
%config %{_sysconfdir}/grub.d/40_custom
%config %{_sysconfdir}/grub.d/41_custom
%config %{_sysconfdir}/grub.d/90_persistent
%config %{_sysconfdir}/grub.d/95_textmode
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-once
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-check-default
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-file
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-mkrescue
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-syslinux2cfg
%if 0%{?has_systemd:1}
%{_unitdir}/grub2-once.service
%endif
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/themes
%if 0%{?suse_version} >= 1140
%{_datadir}/%{name}/*.pf2
%endif
%{_datadir}/%{name}/grub-mkconfig_lib
%{_infodir}/grub-dev.info*
%{_infodir}/%{name}.info*
%{_mandir}/man1/%{name}-editenv.1.*
%{_mandir}/man1/%{name}-file.1.*
%{_mandir}/man1/%{name}-fstest.1.*
%{_mandir}/man1/%{name}-kbdcomp.1.*
%{_mandir}/man1/%{name}-menulst2cfg.1.*
%{_mandir}/man1/%{name}-mkfont.1.*
%{_mandir}/man1/%{name}-mkimage.1.*
%{_mandir}/man1/%{name}-mklayout.1.*
%{_mandir}/man1/%{name}-mknetdir.1.*
%{_mandir}/man1/%{name}-mkpasswd-pbkdf2.1.*
%{_mandir}/man1/%{name}-mkrelpath.1.*
%{_mandir}/man1/%{name}-mkrescue.1.*
%{_mandir}/man1/%{name}-mkstandalone.1.*
%{_mandir}/man1/%{name}-render-label.1.*
%{_mandir}/man1/%{name}-script-check.1.*
%{_mandir}/man1/%{name}-syslinux2cfg.1.*
%{_mandir}/man8/%{name}-install.8.*
%{_mandir}/man8/%{name}-mkconfig.8.*
%{_mandir}/man8/%{name}-probe.8.*
%{_mandir}/man8/%{name}-reboot.8.*
%{_mandir}/man8/%{name}-set-default.8.*
%if %{emu}
%{_bindir}/%{name}-emu*
%{_mandir}/man1/%{name}-emu.1.*
%endif
%ifnarch s390x
%config %{_sysconfdir}/grub.d/30_os-prober
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-mount
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-sparc64-setup
%{_mandir}/man1/%{name}-glue-efi.1.*
%{_mandir}/man1/%{name}-mount.1.*
%{_mandir}/man8/%{name}-bios-setup.8.*
%{_mandir}/man8/%{name}-macbless.8.*
%{_mandir}/man8/%{name}-ofpathname.8.*
%{_mandir}/man8/%{name}-sparc64-setup.8.*
%endif

%files branding-upstream
%defattr(-,root,root,-)
%{_datadir}/%{name}/themes/starfield

%if ! 0%{?only_efi:1}

%files %{grubarch}
%defattr(-,root,root,-)
%ifarch %{ix86} x86_64
%config %{_sysconfdir}/grub.d/20_memtest86+
%endif
%dir %{_libdir}/%{name}/%{grubarch}
%ifarch ppc ppc64 ppc64le
%config %{_sysconfdir}/grub.d/20_ppc_terminfo
# This is intentionally "grub.chrp" and not "%{name}.chrp"
%{_libdir}/%{name}/%{grubarch}/grub.chrp
%{_libdir}/%{name}/%{grubarch}/bootinfo.txt
%endif
%ifnarch ppc ppc64 ppc64le s390x %{arm}
%{_libdir}/%{name}/%{grubarch}/*.image
%endif
%{_libdir}/%{name}/%{grubarch}/*.img
%{_libdir}/%{name}/%{grubarch}/*.lst
%{_libdir}/%{name}/%{grubarch}/*.mod
%{_libdir}/%{name}/%{grubarch}/*.module
%ifarch x86_64
%{_libdir}/%{name}/%{grubarch}/efiemu*.o
%endif
%{_libdir}/%{name}/%{grubarch}/gdb_grub
%{_libdir}/%{name}/%{grubarch}/gmodule.pl
%{_libdir}/%{name}/%{grubarch}/kernel.exec
%{_libdir}/%{name}/%{grubarch}/modinfo.sh
%endif
%ifarch s390x
%{_sbindir}/%{name}-zipl-setup
%config(noreplace) %{_sysconfdir}/default/zipl2grub.conf.in
%{dracutlibdir}
%endif

%ifarch %{efi}

%files %{grubefiarch}
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}/%{grubefiarch}
%{_libdir}/%{name}/%{grubefiarch}/grub.efi
%{_libdir}/%{name}/%{grubefiarch}/grub-tpm.efi
%{_libdir}/%{name}/%{grubefiarch}/*.img
%{_libdir}/%{name}/%{grubefiarch}/*.lst
%{_libdir}/%{name}/%{grubefiarch}/*.mod
%{_libdir}/%{name}/%{grubefiarch}/*.module
%{_libdir}/%{name}/%{grubefiarch}/gdb_grub
%{_libdir}/%{name}/%{grubefiarch}/gmodule.pl
%{_libdir}/%{name}/%{grubefiarch}/kernel.exec
%{_libdir}/%{name}/%{grubefiarch}/modinfo.sh
%dir %{sysefidir}
%{sysefidir}/grub.efi

%ifarch x86_64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
%{sysefidir}/grub.der
%endif
%endif
%endif

%files snapper-plugin
%defattr(-,root,root,-)
%dir %{_libdir}/snapper
%dir %{_libdir}/snapper/plugins
%config %{_sysconfdir}/grub.d/80_suse_btrfs_snapshot
%{_libdir}/snapper/plugins/grub

%ifarch %{ix86} x86_64
%files %{grubxenarch}
%dir %{_libdir}/%{name}/%{grubxenarch}
%{_libdir}/%{name}/%{grubxenarch}/*
%endif

%if 0%{?has_systemd:1}
%files systemd-sleep-plugin
%defattr(-,root,root,-)
%dir %{_libdir}/systemd/system-sleep
%{_libdir}/systemd/system-sleep/grub2.sleep
%endif

%changelog
* Mon Mar 12 2018 mchang@suse.com
- Fix UEFI HTTPS Boot from ISO installation image (bsc#1076132)
  * 0001-add-support-for-UEFI-network-protocols.patch
* Tue Mar  6 2018 mchang@suse.com
- fix wrong command output when default subvolume is toplevel tree with
  id 5 (bsc#1078775)
  * grub2-btrfs-09-get-default-subvolume.patch
- insert mdraid modules to support software RAID (bsc#1078775)
  * grub2-xen-pv-firmware.cfg
* Thu Mar  1 2018 iforster@suse.com
- Rename grub2-btrfs-workaround-grub2-once.patch to
  grub2-grubenv-in-btrfs-header.patch
- Store GRUB environment variable health_checker_flag in Btrfs header
* Tue Feb 13 2018 mchang@suse.com
- Fix incorrect check preventing the script from running (bsc#1078481)
  * 80_suse_btrfs_snapshot
* Wed Feb  7 2018 mchang@suse.com
- Fix disappeared snapshot menu entry (bsc#1078481)
  * 80_suse_btrfs_snapshot
* Tue Feb  6 2018 mchang@suse.com
- Fix unquoted string error and add some more checks (bsc#1079330)
  * grub2-check-default.sh
* Mon Feb  5 2018 olaf@aepfle.de
- The %%prep section applies patches, the %%build section builds.
  Remove mixup of patching and building from %%prep for quilt setup
  Related to bsc#1065703
* Tue Jan 23 2018 mchang@suse.com
- Check if default entry need to be corrected for updated distributor version
  and/or use fallback entry if default kernel entry removed (bsc#1065349)
  * grub2-check-default.sh
  * grub2-mkconfig-default-entry-correction.patch
- Fix grub2-mkconfig warning when disk is LVM PV (bsc#1071239)
  * grub2-getroot-scan-disk-pv.patch
* Fri Dec  8 2017 mchang@suse.com
-  Filter out autofs and securityfs from /proc/self/mountinfo to speed
  up nfsroot test in large number of autofs mounts (bsc#1069094)
  * modified grub2-pass-corret-root-for-nfsroot.patch
* Tue Nov 28 2017 mchang@suse.com
- Fix http(s) boot security review (bsc#1058090)
  * 0002-AUDIT-0-http-boot-tracker-bug.patch
* Tue Nov 14 2017 mchang@suse.com
- 0001-add-support-for-UEFI-network-protocols.patch:
  * Workaround http data access in firmware
  * Fix DNS device path parsing for efinet device
  * Relaxed UEFI Protocol requirement
  * Support Intel OPA (Omni-Path Architecture) PXE Boot (bsc#1015589)
* Wed Nov  8 2017 olaf@aepfle.de
- grub2-xen-pv-firmware.cfg: remove linemode=1 from cmdline for
  SUSE installer. openQA expects ncurses interface. (bsc#1066919)
* Mon Nov  6 2017 jmatejek@suse.com
- use python3 for autogen.sh (fate#323526)
* Tue Oct 31 2017 msuchanek@suse.com
- Do not check that PReP partition does not contain an ELF during installation
  (bsc#1065738).
  * grub2-install-remove-useless-check-PReP-partition-is-empty.patch
* Tue Sep 26 2017 mchang@suse.com
- Build diskboot_tpm.img as separate image to diskboot.img to prevent failure
  in booting on some bogus firmware. To use the TPM image you have to use
  suse-enable-tpm option of grub2-install (bsc#1052401)
  * 0013-tpm-i386-pc-diskboot-img.patch
* Wed Sep 20 2017 mlatimer@suse.com
- Use /boot/<arch>/loader/linux to determine if install media
  is SUSE instead of /contents file (bsc#1054453)
* Tue Sep 19 2017 mlatimer@suse.com
- Use the pvops-enabled default kernel if the traditional xen
  pv kernel and initrd are not found (bsc#1054453)
* Fri Sep  8 2017 agraf@suse.com
- Fix reboot in UEFI environments (bsc#1047331)
  * Add grub2-efi-Move-grub_reboot-into-kernel.patch
  * Refresh grub2-efi-Free-malloc-regions-on-exit.patch
* Sun Sep  3 2017 mchang@suse.com
- Add preliminary patch for UEFI HTTPS and related network protocol support
  (fate#320130)
  * 0001-add-support-for-UEFI-network-protocols.patch
* Sun Sep  3 2017 mchang@suse.com
- grub2-s390x-04-grub2-install.patch : remove arybase dependency in
  grub2-zipl-setup by not referencing to $[ (bsc#1055280)
* Wed Aug 23 2017 rw@suse.com
- Fix minor oversights in and the exit value of the grub2-install
  helper on s390x.  (bsc#1055343, fate#323298)
  * grub2-s390x-09-improve-zipl-setup.patch
* Mon Jul 24 2017 bwiedemann@suse.com
- Make grub2.info build reproducible (boo#1047218)
* Tue Jul  4 2017 arvidjaar@gmail.com
- add grub2-fix-build-with-flex-2.6.4.patch - fix build with flex 2.6.4+
  that removed explicit (void) cast from fprintf call in yy_fatal_error.
* Thu Jun  1 2017 mchang@suse.com
- Support LVM physical volume created without metadatacopies (bsc#1027526)
  * grub2-diskfilter-support-pv-without-metadatacopies.patch
- Fix page fault exception when grub loads with Nvidia cards (bsc#1038533)
  * grub2-efi-uga-64bit-fb.patch
- Require 'kexec-tools' for System z. (bsc#944358)
  * modified grub2.spec
* Thu May 11 2017 mchang@suse.com
- grub2-xen-pv-firmware.cfg: insmod lvm module as it's not auto-loaded
  to support booting from lvm volume (bsc#1004324)
- Grub not working correctly with xen and btrfs snapshots (bsc#1026511)
  * Add grub2-btrfs-09-get-default-subvolume.patch
  * grub2-xen-pv-firmware.cfg : search path in default subvolume
* Thu Apr 27 2017 arvidjaar@gmail.com
- new upstream version 2.02
  * rediff
  - use-grub2-as-a-package-name.patch
  * drop upstream patches
  - grub2-fix-uninitialized-variable-in-btrfs-with-GCC7.patch
  - grub2-add-FALLTHROUGH-annotations.patch
- update translations
* Sun Mar 26 2017 arvidjaar@gmail.com
- update grub2-btrfs-workaround-grub2-once.patch to also store saved_entry
  in additional environment block (boo#1031025)
* Wed Mar 22 2017 arvidjaar@gmail.com
- fix building with GCC (bsc#1030247)
  * add grub2-fix-uninitialized-variable-in-btrfs-with-GCC7.patch
  * grub2-add-FALLTHROUGH-annotations.patch
* Mon Mar 20 2017 mchang@suse.com
- Fix out of memory error on lvm detection (bsc#1016536) (bsc#1027401)
  * grub2-lvm-allocate-metadata-buffer-from-raw-contents.patch
- Fix boot failure if /boot is separate btrfs partition (bsc#1023160)
  * grub2-btrfs-06-subvol-mount.patch
* Fri Mar 17 2017 mchang@suse.com
- 0004-tpm-Rework-linux-command.patch : Fix out of bound memory copy
  (bsc#1029187)
* Thu Mar 16 2017 arvidjaar@gmail.com
- new upstream version 2.02~rc2
  * rediff
  - use-grub2-as-a-package-name.patch
  - grub2-linguas.sh-no-rsync.patch
  * drop upstream patches
  - 0001-efi-strip-off-final-NULL-from-File-Path-in-grub_efi_.patch
* Mon Mar  6 2017 mchang@suse.com
- TPM Support (FATE#315831)
  * 0001-tpm-Core-TPM-support.patch
  * 0002-tpm-Measure-kernel-initrd.patch
  * 0003-tpm-Add-BIOS-boot-measurement.patch
  * 0004-tpm-Rework-linux-command.patch
  * 0005-tpm-Rework-linux16-command.patch
  * 0006-tpm-Measure-kernel-and-initrd-on-BIOS-systems.patch
  * 0007-tpm-Measure-the-kernel-commandline.patch
  * 0008-tpm-Measure-commands.patch
  * 0009-tpm-Measure-multiboot-images-and-modules.patch
  * 0010-tpm-Fix-boot-when-there-s-no-TPM.patch
  * 0011-tpm-Fix-build-error.patch
  * 0012-tpm-Build-tpm-as-module.patch
- grub2.spec : Add grub-tpm.efi for Secure Boot
* Fri Mar  3 2017 mchang@suse.com
- Fix invalid Xen EFI config files if xen_args include GRUB2 quoting
  (bsc#900418) (bsc#951748)
  * grub2-efi-xen-cfg-unquote.patch
- Fix linuxefi erroneously initialize linux's boot_params with non-zero
  values. (bsc#1025563)
  * grub2-linuxefi-fix-boot-params.patch
- Removed grub2-fix-multi-device-root-kernel-argument.patch as it has
  regression on how GRUB_DISABLE_LINUX_UUID=true interpreted (bsc#1015138)
* Wed Mar  1 2017 mchang@suse.com
- Fix for openQA UEFI USB Boot failure with upstream patch (bsc#1026344)
  * added 0001-efi-strip-off-final-NULL-from-File-Path-in-grub_efi_.patch
  * removed 0001-Revert-efi-properly-terminate-filepath-with-NULL-in-.patch
* Thu Feb 23 2017 mchang@suse.com
- Temporary fix for openQA UEFI USB Boot failure (bsc#1026344)
  * 0001-Revert-efi-properly-terminate-filepath-with-NULL-in-.patch
* Fri Feb 17 2017 mchang@suse.com
- grub2.spec: fix s390x file list.
* Thu Feb 16 2017 msuchanek@suse.com
- require efibootmgr in efi package (boo#1025520)
* Wed Feb 15 2017 mchang@suse.com
- Merge changes from SLE12
- add grub2-emu-4-all.patch
  * Build 'grub2-emu' wherever possible, to allow a better
    implementation of that feature.
- add grub2-s390x-06-loadparm.patch,
- add grub2-commands-introduce-read_file-subcommand.patch:
  * allow s390x to telecontrol grub2.  (bsc#891946, bsc#892852)
- add grub2-s390x-06-loadparm.patch:
  * ignore case and fix transliteration of parameter.  (bsc#891946)
- add grub2-s390x-07-add-image-param-for-zipl-setup.patch
  * Add --image switch to force zipl update to specific kernel
    (bsc#928131)
- add grub2-s390x-08-workaround-part-to-disk.patch
  * Ignore partition tables on s390x. (bsc#935127)
- add grub2-efi-chainload-harder.patch:
  * allow XEN to be chain-loaded despite firmware flaws.  (bnc#887793)
  * Do not use shim lock protocol for reading pe header, it won't be
  available when secure boot disabled (bsc#943380)
  * Make firmware flaw condition be more precisely detected and add
  debug message for the case
  * Check msdos header to find PE file header (bsc#954126)
- grub2-s390x-04-grub2-install.patch:
  * streamline boot to grub menu.  (bsc#898198)
  * Force '/usr' to read-only before calling kexec. (bsc#932951)
- grub2-once:
  * add '--enum' option to enumerate boot-entries in a way
    actually understood by 'grub2'.  (bsc#892852, bsc#892811)
  * Examine variables from grub environment in 'grub2-once'. (fate#319632)
* Fri Feb 10 2017 arvidjaar@gmail.com
- new upstream version 2.02~rc1
  * rediff
  - use-grub2-as-a-package-name.patch
  - grub2-s390x-04-grub2-install.patch
  - grub2-accept-empty-module.patch
  - grub2-btrfs-04-grub2-install.patch
  - grub2-btrfs-06-subvol-mount.patch
  * drop upstream patches
  - 0001-dns-fix-buffer-overflow-for-data-addresses-in-recv_h.patch
  - 0001-build-Use-AC_HEADER_MAJOR-to-find-device-macros.patch
  - 0002-configure-fix-check-for-sys-sysmacros.h-under-glibc-.patch
  - 0001-Fix-fwpath-in-efi-netboot.patch
  - 0001-arm64-Move-firmware-fdt-search-into-global-function.patch
  - 0002-arm-efi-Use-fdt-from-firmware-when-available.patch
  - grub2-arm64-mknetdir-add-suport-for-arm64-efi.patch
  - 0001-10_linux-Fix-grouping-of-tests-for-GRUB_DEVICE.patch
  - 0002-20_linux_xen-fix-test-for-GRUB_DEVICE.patch
  - 0001-xen-make-xen-loader-callable-multiple-times.patch
  - 0002-xen-avoid-memleaks-on-error.patch
  - 0003-xen-reduce-number-of-global-variables-in-xen-loader.patch
  - 0004-xen-add-elfnote.h-to-avoid-using-numbers-instead-of-.patch
  - 0005-xen-synchronize-xen-header.patch
  - 0006-xen-factor-out-p2m-list-allocation-into-separate-fun.patch
  - 0007-xen-factor-out-allocation-of-special-pages-into-sepa.patch
  - 0008-xen-factor-out-allocation-of-page-tables-into-separa.patch
  - 0009-xen-add-capability-to-load-initrd-outside-of-initial.patch
  - 0010-xen-modify-page-table-construction.patch
  - 0011-xen-add-capability-to-load-p2m-list-outside-of-kerne.patch
  * add
  - fix-grub2-use-stat-instead-of-udevadm-for-partition-lookup-with-new-glibc.patch
    fix compilation with new glibc
* Thu Feb  9 2017 mchang@suse.com
- Fix build error on glibc-2.25
  * 0001-build-Use-AC_HEADER_MAJOR-to-find-device-macros.patch
  * 0002-configure-fix-check-for-sys-sysmacros.h-under-glibc-.patch
- Fix fwpath in efi netboot (fate#321993) (bsc#1022294)
  * 0001-Fix-fwpath-in-efi-netboot.patch
* Fri Feb  3 2017 mchang@suse.com
- grub2-systemd-sleep.sh: Fix prematurely abort by commands error return code
  and skip the offending menu entry (bsc#1022880)
* Wed Feb  1 2017 agraf@suse.com
- Add support for BLT only EFI GOP adapters (FATE#322332)
  * grub2-efi-gop-add-blt.patch
* Wed Jan 25 2017 schwab@linux-m68k.org
- info-dir-entry.patch: Update info dir entry to follow renaming to grub2
* Mon Jan 16 2017 matwey.kornilov@gmail.com
- Add serial module to efi image.
  Serial terminal is still useful even with EFI Secure Boot
* Wed Jan 11 2017 mchang@suse.com
- Support %%posttrans with marcos provided by update-bootloader-rpm-macros
  package (bsc#997317)
* Wed Jan  4 2017 mchang@suse.com
- Remove outdated README.openSUSE (bsc#907693)
* Fri Dec 30 2016 sor.alexei@meowr.ru
- 20_memtest86+: avoid adding memtest86+ to the list with UEFI
  booting.
* Fri Oct 28 2016 mchang@suse.com
- Fix new line character in distributor (bsc#1007212)
  * modified grub2-default-distributor.patch
* Fri Oct 21 2016 mchang@suse.com
- From Juergen Gross <jgross@suse.com>: grub-xen: support booting huge
  pv-domains (bsc#1004398) (bsc#899465)
  * 0001-xen-make-xen-loader-callable-multiple-times.patch
  * 0002-xen-avoid-memleaks-on-error.patch
  * 0003-xen-reduce-number-of-global-variables-in-xen-loader.patch
  * 0004-xen-add-elfnote.h-to-avoid-using-numbers-instead-of-.patch
  * 0005-xen-synchronize-xen-header.patch
  * 0006-xen-factor-out-p2m-list-allocation-into-separate-fun.patch
  * 0007-xen-factor-out-allocation-of-special-pages-into-sepa.patch
  * 0008-xen-factor-out-allocation-of-page-tables-into-separa.patch
  * 0009-xen-add-capability-to-load-initrd-outside-of-initial.patch
  * 0010-xen-modify-page-table-construction.patch
  * 0011-xen-add-capability-to-load-p2m-list-outside-of-kerne.patch
* Tue Oct 11 2016 dmueller@suse.com
- add support for netboot on arm64-efi platforms (bsc#998097)
  * grub2-arm64-mknetdir-add-suport-for-arm64-efi.patch
* Fri Sep  2 2016 mchang@suse.com
- use $PRETTY_NAME instead of $NAME $VERSION for $GRUB_DISTRIBUTOR
  in openSUSE Tumbleweed (bsc#995549)
  * modified grub2-default-distributor.patch
- grub2.spec: add http module to grub.efi (fate#320129)
* Wed Aug 31 2016 matz@suse.com
- binutils 2.27 creates empty modules without a symtab.
  Add patch grub2-accept-empty-module.patch to not reject them.
* Sat Aug 20 2016 arvidjaar@gmail.com
- since version 1.7 cryptsetup defaults to SHA256 for LUKS - include
  gcry_sha256 in signed EFI image
* Fri Aug 12 2016 mchang@suse.com
- Workaround default entry in snapshot menu (bsc#956046)
  * grub2-btrfs-08-workaround-snapshot-menu-default-entry.patch
- grub2.spec: Add true command to grub.efi (bsc#993274)
* Wed Aug  3 2016 mchang@suse.com
- grub.default: Empty GRUB_CMDLINE_LINUX_DEFAULT, the value will be fully
  taken from YaST settings. (bsc#989803)
* Wed Aug  3 2016 mchang@suse.com
- Add patches from Roberto Sassu <rsassu@suse.de>
- Fix grub2-10_linux-avoid-multi-device-root-kernel-argument.patch,
  device path is not tested if GRUB_DISABLE_LINUX_UUID="true"
  - added grub2-fix-multi-device-root-kernel-argument.patch
  (bsc#960776)
- grub2-zipl-setup: avoid multi-device root= kernel argument
  * added grub2-zipl-setup-fix-btrfs-multipledev.patch
  (bsc#960776)
- Add SUSE_REMOVE_LINUX_ROOT_PARAM configuration option
  to /etc/default/grub, to remove root= and rootflags= from the
  kernel command line in /boot/grub2/grub.cfg and /boot/zipl/config
  - added grub2-suse-remove-linux-root-param.patch
  (bsc#962585)
* Tue Aug  2 2016 mchang@suse.com
- Support HTTP Boot IPv4 and IPv6 (fate#320129)
  * 0001-misc-fix-invalid-character-recongition-in-strto-l.patch
  * 0002-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
  * 0003-bootp-New-net_bootp6-command.patch
  * 0004-efinet-UEFI-IPv6-PXE-support.patch
  * 0005-grub.texi-Add-net_bootp6-doument.patch
  * 0006-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
  * 0007-efinet-Setting-network-from-UEFI-device-path.patch
  * 0008-efinet-Setting-DNS-server-from-UEFI-protocol.patch
- Fix heap corruption after dns lookup
  * 0001-dns-fix-buffer-overflow-for-data-addresses-in-recv_h.patch
* Mon Jun 27 2016 ro@suse.de
- fix filelist for s390x
* Tue Jun 21 2016 mchang@suse.com
- Fix grub2-editenv error on encrypted lvm installation (bsc#981621)
  * modified grub2-btrfs-workaround-grub2-once.patch
- Add missing closing bracket in 'grub2-snapper-plugin.sh'.
- Fix snapshot booting on s390x (bsc#955115)
  * modified grub2-snapper-plugin.sh
- Fallback to old subvol name scheme to support old snapshot config
  (bsc#953538)
  * added grub2-btrfs-07-subvol-fallback.patch
* Thu Jun  2 2016 arvidjaar@gmail.com
- update grub2-once with patch from Björn Voigt - skip comments in
  /etc/sysconfig/bootloader (boo#963610)
* Fri May 20 2016 jengelh@inai.de
- Make sure all systemd unit files are passed to %%service_ macros.
* Thu May 19 2016 agraf@suse.com
- Add patch to free memory on exit in efi environments (bsc#980739)
  * grub2-efi-Free-malloc-regions-on-exit.patch
* Mon May  2 2016 olaf@aepfle.de
- Remove xen-devel from BuildRequires
  required headers are included in grub-2.0.2
* Thu Apr 28 2016 agraf@suse.com
- Add support for "t" hotkey to switch to text mode (bsc#976836)
  * added grub2-SUSE-Add-the-t-hotkey.patch
- Add support for hidden menu entries (bsc#976836)
  * added grub2-Add-hidden-menu-entries.patch
* Tue Apr 19 2016 mchang@suse.com
- Correct show user defined comments in menu for snapshots (bsc#956698)
  * modified grub2-snapper-plugin.sh
* Mon Mar 21 2016 mchang@suse.com
- Fix GRUB_DISABLE_LINUX_UUID to be ignore and also fallback kernel device
  won't be used if fs uuid not detected (bsc#971867)
  * added 0001-10_linux-Fix-grouping-of-tests-for-GRUB_DEVICE.patch
  * added 0002-20_linux_xen-fix-test-for-GRUB_DEVICE.patch
* Tue Mar  1 2016 arvidjaar@gmail.com
- new upstream version 2.02~beta3
  * highlights of user visible changes not yet present in openSUSE package
  - arm-uboot now generates position independent self relocating image, so
    single binary should run on all supported systems
  - loader for Xen on aarch64. grub-mkconfig support was not in time for
    beta3 yet.
  - improved ZFS support (extensible_dataset, large_blocks, embedded_data,
    hole_birth features)
  - support for IPv6 Router Advertisements
  - support for persistent memory (we do not overwrite it and pass correct
    information to OS)
  - try to display more specific icons for os-prober generated menu entries
  - grub-install detects EFI bit size and selects correct platform (x86_64-efi
    or i386-efi) independent of OS bit size; needs kernel 4.0 or higher.
  - LVM RAID1 support
  - xnu loader fixes which should make OS X menu entry generated by os-prober
    work again
  - key modifiers (Ctrl-X etc) should work on EFI too
  - ... and lot of fixes over entire tree
  * rediff
  - rename-grub-info-file-to-grub2.patch
  - use-grub2-as-a-package-name.patch
  - grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
  - grub2-fix-menu-in-xen-host-server.patch
  - grub2-efi-HP-workaround.patch
  - grub2-secureboot-chainloader.patch
  - grub2-s390x-02-kexec-module-added-to-emu.patch
  - grub2-s390x-04-grub2-install.patch
  - grub2-s390x-05-grub2-mkconfig.patch
  - grub2-efi-xen-chainload.patch
  - grub2-mkconfig-aarch64.patch
  - grub2-btrfs-04-grub2-install.patch
  - grub2-ppc64-cas-reboot-support.patch
  - 0002-Add-Virtual-LAN-support.patch
  * fix grub2-secureboot-add-linuxefi.patch - use grub_memset and
    grub_memcpy instead of memset and memcpy (caused errors due to
    compiler warning)
  * drop upstream patches
  - 0001-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
  - 0001-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch
  - 0001-efidisk-move-device-path-helpers-in-core-for-efinet.patch
  - 0002-efinet-skip-virtual-IPv4-and-IPv6-devices-when-enume.patch
  - 0003-efinet-open-Simple-Network-Protocol-exclusively.patch
  - 0001-efinet-Check-for-immediate-completition.patch
  - 0001-efinet-enable-hardware-filters-when-opening-interfac.patch
  - grub2-xen-legacy-config-device-name.patch
  - grub2-getroot-support-NVMe-device-names.patch
  - grub2-netboot-hang.patch
  - grub2-btrfs-fix-incorrect-address-reference.patch
  - aarch64-reloc.patch
  - grub2-glibc-2.20.patch (related code dropped upstream)
  - grub2-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
  - grub2-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
  - grub2-getroot-fix-get-btrfs-fs-prefix-big-endian.patch
  - grub2-ppc64-qemu.patch
  - grub2-xfs-Add-helper-for-inode-size.patch
  - grub2-xfs-Fix-termination-loop-for-directory-iteration.patch
  - grub2-xfs-Convert-inode-numbers-to-cpu-endianity-immediate.patch
  - grub2-xfs-V5-filesystem-format-support.patch
  - 0001-Add-bootargs-parser-for-open-firmware.patch
  - grub2-arm64-set-correct-length.patch
  - grub2-arm64-setjmp-Add-missing-license-macro.patch
  - grub2-arm64-efinet-handle-get_status-on-buggy-firmware-properly.patch
  - 0001-unix-password-Fix-file-descriptor-leak.patch
  - 0002-linux-getroot-fix-descriptor-leak.patch
  - 0003-util-grub-mount-fix-descriptor-leak.patch
  - 0004-linux-ofpath-fix-descriptor-leak.patch
  - 0005-grub-fstest-fix-descriptor-leak.patch
  - ppc64le.patch
  - libgcc-prereq.patch
  - libgcc.patch
  - 0001-Fix-security-issue-when-reading-username-and-passwor.patch
  - 0001-menu-fix-line-count-calculation-for-long-lines.patch
  - grub2-arm64-Reduce-timer-event-frequency-by-10.patch
  - 0001-unix-do-not-close-stdin-in-grub_passwd_get.patch
  - 0001-grub-core-kern-i386-tsc.c-calibrate_tsc-Ensure-that.patch
  - 0002-i386-tsc-Fix-unused-function-warning-on-xen.patch
  - 0003-acpi-do-not-skip-BIOS-scan-if-EBDA-length-is-zero.patch
  - 0004-tsc-Use-alternative-delay-sources-whenever-appropria.patch
  - 0005-i386-fix-TSC-calibration-using-PIT.patch
  - biendian.patch
  - ppc64_opt.patch
  * drop workarounds for gdb_grub and grub.chrp, they are now installed under fixed name
  * do not patch docs/Makefile.in, it is regenerated anyway
* Tue Mar  1 2016 agraf@suse.com
- Make mkconfig search for zImage on arm
  * grub2-mkconfig-arm.patch
* Sun Feb 28 2016 agraf@suse.com
- Add support to directly pass an EFI FDT table to a kernel on 32bit arm
  * 0001-arm64-Move-firmware-fdt-search-into-global-function.patch
  * 0002-arm-efi-Use-fdt-from-firmware-when-available.patch
* Fri Jan 29 2016 mchang@suse.com
- Add config option to set efi xen loader command line option (bsc#957383)
  * added grub2-efi-xen-cmdline.patch
* Thu Jan 28 2016 dvaleev@suse.com
- Drop ppc64le patches. Build stage1 as BE for Power
  Droped patches:
  - grub2-ppc64le-01-Add-Little-Endian-support-for-Power64-to-the-build.patch
  - grub2-ppc64le-02-Build-grub-as-O1-until-we-add-savegpr-and-restgpr-ro.patch
  - grub2-ppc64le-03-disable-creation-of-vsx-and-altivec-instructions.patch
  - grub2-ppc64le-04-powerpc64-LE-s-linker-knows-how-to-handle-the-undefi.patch
  - grub2-ppc64le-05-grub-install-can-now-recognize-and-install-a-LE-grub.patch
  - grub2-ppc64le-06-set-the-ABI-version-to-0x02-in-the-e_flag-of-the-PPC.patch
  - grub2-ppc64le-07-Add-IEEE1275_ADDR-helper.patch
  - grub2-ppc64le-08-Fix-some-more-warnings-when-casting.patch
  - grub2-ppc64le-09-Add-powerpc64-types.patch
  - grub2-ppc64le-10-powerpc64-is-not-necessarily-BigEndian-anymore.patch
  - grub2-ppc64le-11-Fix-warnings-when-building-powerpc-linux-loader-64bi.patch
  - grub2-ppc64le-12-GRUB_ELF_R_PPC_-processing-is-applicable-only-for-32.patch
  - grub2-ppc64le-13-Fix-powerpc-setjmp-longjmp-64bit-issues.patch
  - grub2-ppc64le-14-Add-powerpc64-ieee1275-trampoline.patch
  - grub2-ppc64le-15-Add-64bit-support-to-powerpc-startup-code.patch
  - grub2-ppc64le-16-Add-grub_dl_find_section_addr.patch
  - grub2-ppc64le-17-Add-ppc64-relocations.patch
  - grub2-ppc64le-18-ppc64-doesn-t-need-libgcc-routines.patch
  - grub2-ppc64le-19-Use-FUNC_START-FUNC_END-for-powerpc-function-definit.patch
  - grub2-ppc64le-20-.TOC.-symbol-is-special-in-ppc64le-.-It-maps-to-the-.patch
  - grub2-ppc64le-21-the-.toc-section-in-powerpc64le-modules-are-sometime.patch
  - grub2-ppc64le-22-all-parameter-to-firmware-calls-should-to-be-BigEndi.patch
  - grub2-ppc64le-fix-64bit-trampoline-in-dyn-linker.patch
  - grub2-ppc64le-timeout.patch
  - grub2-ppc64-build-ppc64-32bit.patch
- Added patches:
  - biendian.patch
  - grub2-ppc64-cas-reboot-support.patch
  - libgcc-prereq.patch
  - libgcc.patch
  - ppc64_opt.patch
  - ppc64le.patch
* Wed Jan 20 2016 mchang@suse.com
- Backport upstream patches for HyperV gen2 TSC timer calbration without
  RTC (bsc#904647)
  * added 0001-grub-core-kern-i386-tsc.c-calibrate_tsc-Ensure-that.patch
  * added 0002-i386-tsc-Fix-unused-function-warning-on-xen.patch
  * added 0003-acpi-do-not-skip-BIOS-scan-if-EBDA-length-is-zero.patch
  * added 0004-tsc-Use-alternative-delay-sources-whenever-appropria.patch
  * added 0005-i386-fix-TSC-calibration-using-PIT.patch
* Mon Dec 28 2015 arvidjaar@gmail.com
- Add 0001-menu-fix-line-count-calculation-for-long-lines.patch (bsc#943585)
* Thu Dec 17 2015 olaf@aepfle.de
- grub2-xen-pv-firmware.cfg: fix hd boot (boo#926795)
* Wed Dec 16 2015 arvidjaar@gmail.com
- Add 0001-Fix-security-issue-when-reading-username-and-passwor.patch
  Fix for CVE-2015-8370 [boo#956631]
* Wed Dec  9 2015 arvidjaar@gmail.com
- Update grub2-efi-xen-chainload.patch - fix copying of Linux kernel
  and initrd to ESP (boo#958193)
* Mon Dec  7 2015 olaf@aepfle.de
- Rename grub2-xen.cfg to grub2-xen-pv-firmware.cfg (boo#926795)
* Fri Dec  4 2015 olaf@aepfle.de
- grub2-xen.cfg: to handle grub1 menu.lst in PV guest (boo#926795)
* Thu Nov 26 2015 mchang@suse.com
- Expand list of grub.cfg search path in PV Xen guest for systems
  installed to btrfs snapshot. (bsc#946148) (bsc#952539)
  * modified grub2-xen.cfg
- drop grub2-fix-Grub2-with-SUSE-Xen-package-install.patch (bsc#774666)
* Wed Nov 18 2015 arvidjaar@gmail.com
- Add 0001-unix-do-not-close-stdin-in-grub_passwd_get.patch
  Fix reading password by grub2-mkpasswd-pbdk2 without controlling
  tty, e.g. when called from Xfce menu (boo#954519)
* Sun Nov  1 2015 arvidjaar@gmail.com
- Modify grub2-linguas.sh-no-rsync.patch to re-enable en@quot catalog
  (boo#953022).  Other autogenerated catalogs still fail to build due
  to missing C.UTF-8 locale.
* Fri Oct 30 2015 mchang@suse.com
- Allow to execute menuentry unrestricted as default (fate#318574)
  * added grub2-menu-unrestricted.patch
* Thu Oct 29 2015 mchang@suse.com
- Add missing quoting for linuxefi (bsc#951962)
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
  * refreshed grub2-secureboot-provide-linuxefi-config.patch
* Sun Oct 18 2015 eich@suse.com
- Include custom.cfg into the files scanned by grub2-once.
  Allows to chose manually added entries as well (FATE#319632).
* Wed Oct  7 2015 mchang@suse.com
- Upstream patches for fixing file descriptor leakage (bsc#943784)
  * added 0001-unix-password-Fix-file-descriptor-leak.patch
  * added 0002-linux-getroot-fix-descriptor-leak.patch
  * added 0003-util-grub-mount-fix-descriptor-leak.patch
  * added 0004-linux-ofpath-fix-descriptor-leak.patch
  * added 0005-grub-fstest-fix-descriptor-leak.patch
* Tue Oct  6 2015 mchang@suse.com
- Do not force ro option in linuxefi patch (bsc#948555)
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
  * refrehed grub2-secureboot-provide-linuxefi-config.patch
* Wed Sep 23 2015 dmueller@suse.com
- add 0001-efinet-Check-for-immediate-completition.patch,
  0001-efinet-enable-hardware-filters-when-opening-interfac.patch,
  grub2-arm64-efinet-handle-get_status-on-buggy-firmware-properly.patch
  (bsc#947203)
* Mon Sep 14 2015 mchang@suse.com
- Set default GRUB_DISTRIBUTOR from /etc/os-release if it is empty
  or not set by user (bsc#942519)
  * added grub2-default-distributor.patch
  * modified grub.default
* Tue Aug 18 2015 mchang@suse.com
- add systemd-sleep-plugin subpackage (bsc#941758)
- evaluate the menu entry's title string by printf
  * modified grub2-once
  * added grub2-systemd-sleep.sh
* Fri Jul 31 2015 mchang@suse.com
- fix for 'rollback' hint (bsc#901487)
  * modified grub2-btrfs-05-grub2-mkconfig.patch:
* Fri Jul 17 2015 mchang@suse.com
- Replace 12.1 with 12 SP1 for the list of snapshots (bsc#934252)
  * modified grub2-snapper-plugin.sh
* Thu Jun 18 2015 mchang@suse.com
- Fix btrfs subvol detection on BigEndian systems (bsc#933541)
  * modified grub2-btrfs-06-subvol-mount.patch
- Fix grub2-mkrelpath outputs wrong path on BigEndian system
  * added grub2-getroot-fix-get-btrfs-fs-prefix-big-endian.patch
* Fri Jun 12 2015 mchang@suse.com
- If we have a post entry and the description field is empty, we should use the
  "Pre" number and add that description to the post entry. (fate#317972)
- Show user defined comments in grub2 menu for snapshots (fate#318101)
  * modified grub2-snapper-plugin.sh
* Sun Jun  7 2015 arvidjaar@gmail.com
- add 0001-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
  make sure firmware path starts with '/' (boo#902982)
* Fri Jun  5 2015 mchang@suse.com
- Fix btrfs patch on BigEndian systems (bsc#933541)
  * modified grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  * modified grub2-btrfs-06-subvol-mount.patch
* Wed Jun  3 2015 agraf@suse.com
- Fix license for setjmp module
  * added grub2-arm64-setjmp-Add-missing-license-macro.patch
* Thu May 21 2015 mchang@suse.com
- Fix install into snapper controlled btrfs subvolume and can't
  load grub modules from separate subvolume (fate#318392)
  * added grub2-btrfs-06-subvol-mount.patch
  * grub2-snapper-plugin.sh: use absolute subvol name
* Tue May 19 2015 arvidjaar@gmail.com
- also Recommends mtools for grub2-mkrescue (used to create EFI
  boot image) in addition to libburnia-tools.
* Mon May 11 2015 mchang@suse.com
- Support booting opensuse installer as PV DomU (boo#926795)
  * added grub2-xen.cfg for tracking default pvgrub2 xen configs rather than
    generating it from spec file
  * grub2-xen.cfg: from Olaf Hering <ohering@suse.com>
* Sun May 10 2015 arvidjaar@gmail.com
- replace grub2-efinet-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
  with upstream version:
  * 0001-efidisk-move-device-path-helpers-in-core-for-efinet.patch
  * 0002-efinet-skip-virtual-IPv4-and-IPv6-devices-when-enume.patch
  * 0003-efinet-open-Simple-Network-Protocol-exclusively.patch
  Fixes EFI network boot in some QEMU configurations.
* Wed Apr 29 2015 dmueller@suse.com
- fix grub2-mkconfig-aarch64.patch: fix arch detection broken
  by malformed patch rediffing
* Wed Apr 15 2015 mchang@suse.com
- Cleanup patch not applied
  * remove grub2-enable-theme-for-terminal-window.patch
  * grub2.rpmlintrc: remove addFilter("patch-not-applied")
* Thu Apr  2 2015 mchang@suse.com
- Merge changes from SLE12
- Do not pass root= when root is on nfs (bnc#894374)
  * modified grub2-pass-corret-root-for-nfsroot.patch
  * modified grub2-secureboot-provide-linuxefi-config.patch
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
- Fix xen pvops kernel not appear on menu (bnc#895286)
  * modified grub2-fix-menu-in-xen-host-server.patch
- Workaround grub2-once (bnc#892358)
  * added grub2-btrfs-workaround-grub2-once.patch
  * added grub2-once.service
  * modified grub2-once
- Fix busy-loop and hang while network booting (bnc#870613)
  * added grub2-netboot-hang.patch
- Add warning in grubenv file about editing it directly (bnc#887008)
  * added grub2-editenv-add-warning-message.patch
- Fix broken graphics with efifb on QEMU/KVM and nomodeset (bnc#884558)
  * added grub2-efi-disable-video-cirrus-and-bochus.patch
- Disable video support on Power (bnc#877142)
  * added grub2-ppc64le-disable-video.patch
- Track occupied memory so it can be released on exit (bnc#885026)
  * added grub2-ppc64le-memory-map.patch
- Fix grub.xen config searching path on boot partition (bnc#884828)
- Add linux16 and initrd16 to grub.xen (bnc#884830)
  * added grub2-xen-linux16.patch
- VLAN tag support (fate#315753)
  * added 0001-Add-bootargs-parser-for-open-firmware.patch
  * added 0002-Add-Virtual-LAN-support.patch
- Use chainloader to boot xen.efi under UEFI (bnc#871857)
  * added grub2-efi-xen-chainload.patch
- Use device part of chainloader target, if present (bnc#871857)
  * added grub2-efi-chainloader-root.patch
- Create only hypervisor pointed by /boot/xen.gz symlink (bnc#877040)
  * modified grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
- Fix xen and native entries differ in grub.cfg (bnc#872014)
  * modified grub2-linux.patch
- Fix install error on ddf md device (bnc#872360)
  * added grub2-getroot-treat-mdadm-ddf-as-simple-device.patch
- Fix booting from NVMe device (bnc#873132)
  * added grub2-getroot-support-NVMe-device-names.patch
- Document peculiarities of s390 terminals
  * added README.ibm3215
- Grub2 for System z (fate#314213)
  * added grub2-s390x-02-kexec-module-added-to-emu.patch
  * added grub2-s390x-03-output-7-bit-ascii.patch
  * added grub2-s390x-04-grub2-install.patch
  * added grub2-s390x-05-grub2-mkconfig.patch
* Mon Mar 16 2015 schwab@suse.de
- grub2-arm64-set-correct-length.patch: arm64: set correct length of
  device path end entry
* Wed Mar  4 2015 mchang@suse.com
- grub2-efi-HP-workaround.patch:
  * try to read config from all-uppercase prefix as last resort.
    (bnc#872503) (boo#902982)
* Mon Feb 16 2015 arvidjaar@gmail.com
- add luks, gcry_rijndael, gcry_sha1 to signed EFI image to support
  LUKS partition in default setup (boo#917427)
* Thu Feb  5 2015 mchang@suse.com
- enable i386-xen (boo#891043)
* Wed Feb  4 2015 mchang@suse.com
- Downgrade os-prober dependency to Recommends (boo#898610)
* Thu Dec 25 2014 mchang@suse.com
- grub2-snapper-plugin.sh: cleanup grub-snapshot.cfg not referring
  to any snapshot (boo#909359)
* Thu Dec 25 2014 mpluskal@suse.com
- Require efibootmgr also on i586
* Tue Dec 16 2014 schwab@suse.de
- Require efibootmgr also on aarch64
* Thu Dec 11 2014 schwab@suse.de
- grub2-snapper-plugin.sh: fix use of printf without format string; fix
  quoting
* Wed Dec 10 2014 schwab@suse.de
- grub2-arm64-Reduce-timer-event-frequency-by-10.patch: fix periodic timer
  on arm64
* Thu Dec  4 2014 agraf@suse.com
- enable 32bit arm targets for uboot and efi
* Sat Nov 29 2014 Led <ledest@gmail.com>
- Replace 'echo -e' command in grub2-snapper-plugin.sh script to
  'printf' command. '-e' option of 'echo' command may be
  unsupported in some POSIX-complete shells.
* Fri Nov 14 2014 Led <ledest@gmail.com>
- fix bashism in post script
* Thu Oct 30 2014 jdelvare@suse.de
- grub2.spec: Fix conditional construct which wasn't supported by
  older versions of rpmbuild (caused error message
  "parseExpressionBoolean returns -1".)
* Thu Oct 30 2014 mchang@suse.com
- fix errors when boot is btrfs with Windows partition scheme. The
  first partition is created on cylinder boundary that can't offer
  enough room for core.img and also the installation has to be in
  logical paritition which made MBR the only location to install.
  (bnc#841247)
  * add grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
* Tue Sep 30 2014 mchang@suse.com
- packaging 20_memtest86+ and 20_ppc_terminfo in corresponing grubarch
  package
* Mon Sep 29 2014 fcastelli@suse.com
- Add '80_suse_btrfs_snapshot' required to show btrfs snapshots inside
  of the boot menu.
* Sun Sep 28 2014 arvidjaar@gmail.com
- fix btrfs on big endian systems (ppc/ppc64)
  * add grub2-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
* Sun Sep 21 2014 arvidjaar@gmail.com
- update translations
- fix possible access to uninitialized pointer in linux loader
  * add grub2-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
  * drop superceded grub2-ppc64le-23-grub-segfaults-if-initrd-is-specified-before-specify.patch
* Thu Sep 18 2014 mchang@suse.com
- fix grub.xen not able to handle legacy menu.lst hdX names (bnc#863821)
  * add grub2-xen-legacy-config-device-name.patch from arvidjaar
- fix the performance of grub2 uefi pxe is bad (bnc#871555)
  * add grub2-efinet-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
* Tue Sep 16 2014 schwab@suse.de
- grub2-mkconfig-aarch64.patch: Look for Image-* instead of vmlinuz-* on
  aarch64
* Mon Sep 15 2014 arvidjaar@gmail.com
- add grub2-glibc-2.20.patch - fix build with glibc 2.20+
  (use _DEFAULT_SOURCE to avoid warning)
* Fri Sep 12 2014 mchang@suse.com
- fix xen pvops kernel not appear on menu (bnc#895286)
  * refresh grub2-fix-menu-in-xen-host-server.patch
* Wed Sep 10 2014 mchang@suse.com
- fix extraneous comma in printf shell command (bnc#895884)
  * refresh grub2-btrfs-04-grub2-install.patch
* Wed Aug 27 2014 schwab@suse.de
- aarch64-reloc.patch: replace with upstream solution
* Mon Aug 25 2014 mchang@suse.com
- remove unused patch, which's supersceded by new snapper rollback
  support patches
  * 0001-script-provide-overridable-root-by-subvol.patch
  * 0002-script-create-menus-for-btrfs-snapshot.patch
* Fri Aug 22 2014 mchang@suse.com
- fix openqa boot error on separate boot partition
  * refresh grub2-btrfs-05-grub2-mkconfig.patch
* Thu Aug 21 2014 mchang@suse.com
- update snapper plugin for rollback support
  * refresh grub2-snapper-plugin.sh
* Fri Aug 15 2014 mchang@suse.com
- snapper rollback support patches.
- rename patch
  * 0002-btrfs-add-ability-to-boot-from-subvolumes.patch to
    grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  * 0004-btrfs-export-subvolume-envvars.patch to
    grub2-btrfs-02-export-subvolume-envvars.patch
- added patches
  * grub2-btrfs-03-follow_default.patch
  * grub2-btrfs-04-grub2-install.patch
  * grub2-btrfs-05-grub2-mkconfig.patch
- remove patch
  * 0003-cmdline-add-envvar-loader_cmdline_append.patch
* Thu Aug 14 2014 mchang@suse.com
- grub2-btrfs-fix-incorrect-address-reference.patch
  * Fix incorrect address reference in GRUB_BTRFS_EXTENT_REGULAR
    range check (bnc#869748)
* Wed Aug 13 2014 mchang@suse.com
- grub2-vbe-blacklist-preferred-1440x900x32.patch
  * Blacklist preferred resolution 1440x900x32 which is broken on
    many Thinkpads (bnc#888727)
* Tue Aug 12 2014 schwab@suse.de
- Enable building on aarch64
- aarch64-reloc.patch: support R_AARCH64_PREL32 relocation
- Build host tools with RPM_OPT_FLAGS
* Mon Aug 11 2014 dvaleev@suse.com
- Fix the 64-bit trampoline code in dynamic linker (bnc#890999)
  grub2-ppc64le-fix-64bit-trampoline-in-dyn-linker.patch
* Tue Jul 29 2014 tiwai@suse.de
- Prefer a higher resolution in efi_gop driver if the mode taking
  over is too small like 640x480 (bnc#887972):
  grub2-efi_gop-avoid-low-resolution.patch
* Wed Jul  9 2014 dvlaeev@suse.com
- Fix ppc64le build by fixing
  grub2-xfs-V5-filesystem-format-support.patch
* Wed Jun 25 2014 jack@suse.cz
- xfs V5 superblock support (bnc#880166 bnc#883942)
- added patches:
  * grub2-xfs-Add-helper-for-inode-size.patch
  * grub2-xfs-Fix-termination-loop-for-directory-iteration.patch
  * grub2-xfs-Convert-inode-numbers-to-cpu-endianity-immediate.patch
  * grub2-xfs-V5-filesystem-format-support.patch
* Fri Jun 20 2014 jeffm@suse.com
- grub2: use stat instead of udevadm for partition lookup (bnc#883635)
  * Added grub2-use-stat-instead-of-udevadm-for-partition-lookup.patch
* Tue Apr 15 2014 tchvatal@suse.com
- Fix sorting of RC kernels to be older than first regular of the
  series. Fixes bnc#827531.
- added patches:
  * grub2-use-rpmsort-for-version-sorting.patch
* Thu Apr 10 2014 dvaleev@suse.com
- Build GRUB2 for ppc64le as LittleEndian and 64bit
- Fix timeout issue on ppc64le (bnc#869166)
- Add powerpc-utils requires to grub2-powerpc-ieee1275
- added patches:
  * grub2-ppc64-build-ppc64-32bit.patch
  * grub2-ppc64-qemu.patch
  * grub2-ppc64le-01-Add-Little-Endian-support-for-Power64-to-the-build.patch
  * grub2-ppc64le-02-Build-grub-as-O1-until-we-add-savegpr-and-restgpr-ro.patch
  * grub2-ppc64le-03-disable-creation-of-vsx-and-altivec-instructions.patch
  * grub2-ppc64le-04-powerpc64-LE-s-linker-knows-how-to-handle-the-undefi.patch
  * grub2-ppc64le-05-grub-install-can-now-recognize-and-install-a-LE-grub.patch
  * grub2-ppc64le-06-set-the-ABI-version-to-0x02-in-the-e_flag-of-the-PPC.patch
  * grub2-ppc64le-07-Add-IEEE1275_ADDR-helper.patch
  * grub2-ppc64le-08-Fix-some-more-warnings-when-casting.patch
  * grub2-ppc64le-09-Add-powerpc64-types.patch
  * grub2-ppc64le-10-powerpc64-is-not-necessarily-BigEndian-anymore.patch
  * grub2-ppc64le-11-Fix-warnings-when-building-powerpc-linux-loader-64bi.patch
  * grub2-ppc64le-12-GRUB_ELF_R_PPC_-processing-is-applicable-only-for-32.patch
  * grub2-ppc64le-13-Fix-powerpc-setjmp-longjmp-64bit-issues.patch
  * grub2-ppc64le-14-Add-powerpc64-ieee1275-trampoline.patch
  * grub2-ppc64le-15-Add-64bit-support-to-powerpc-startup-code.patch
  * grub2-ppc64le-16-Add-grub_dl_find_section_addr.patch
  * grub2-ppc64le-17-Add-ppc64-relocations.patch
  * grub2-ppc64le-18-ppc64-doesn-t-need-libgcc-routines.patch
  * grub2-ppc64le-19-Use-FUNC_START-FUNC_END-for-powerpc-function-definit.patch
  * grub2-ppc64le-20-.TOC.-symbol-is-special-in-ppc64le-.-It-maps-to-the-.patch
  * grub2-ppc64le-21-the-.toc-section-in-powerpc64le-modules-are-sometime.patch
  * grub2-ppc64le-22-all-parameter-to-firmware-calls-should-to-be-BigEndi.patch
  * grub2-ppc64le-23-grub-segfaults-if-initrd-is-specified-before-specify.patch
  * grub2-ppc64le-timeout.patch
- removed patches:
  * grub2-powerpc-libgcc.patch
  * grub2-ppc64le-core-bigendian.patch
  * grub2-ppc64le-platform.patch
* Thu Apr 10 2014 mchang@suse.com
- add grub2-x86_64-xen subpackage (bnc#863821)
* Sat Apr  5 2014 arvidjaar@gmail.com
- rename grub2.chrp back into grub.chrp, otherwise it is not found by
  grub tools
- replace grub2-use-DejaVuSansMono-for-starfield-theme.patch with
  grub2-use-Unifont-for-starfield-theme-terminal.patch - use Unifont
  font for terminal window
* Thu Feb 27 2014 mchang@suse.com
- grub2-snapper-plugin: fix important snapshots are not marked as such
  in grub2 menu, also display the snapshot entries in the format
  "important distribution version (kernel_version, timestamp, pre/post)"
  (bnc#864842)
* Mon Feb 24 2014 mchang@suse.com
- refresh grub2-fix-menu-in-xen-host-server.patch (bnc#859361)
  * prevent 10_linux from booting xen kernel without pv_opt support
    on systems other than xen PV domU guest
  * prevent 20_linux_xen.in from setting up nested virt running from
    Xen domU
- refresh grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
  * adjust accordingly
* Thu Feb 20 2014 jw@suse.com
- updating grub2-once
  - added --list switch.
  - improved --help and error handling.
* Tue Feb 11 2014 mchang@suse.com
- add Supplements: packageand(snapper:grub2) in grub2-snapper-plugin
  to install it while both snapper and grub2 are installed
* Wed Feb  5 2014 mchang@suse.com
- add grub2-snapper-plugin.sh (fate#316232)
  * grub2's snapper plugin for advanced btrfs snapshot menu management
  * package as grub2-snapper-plugin.noarch
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * when booting btrfs snapshots disabled, deleting snapshot master config
    if it's not customized
* Fri Jan 31 2014 dvaleev@suse.com
- Enable grub2 for PowerPC LE (ppc64le)
- Add ppc64le to exclusive arches
- Don't require gcc-32bit (PowerLE don't have 32bit toolchain)
- added patches:
  * grub2-powerpc-libgcc.patch
    Provide 32bit libgcc functions for PowerLE
  * grub2-ppc64le-core-bigendian.patch
    Build grub kernel and images as BE on ppc64le (BL is BE there)
  * grub2-ppc64le-platform.patch
    Enable ppc64le platform
* Fri Jan 24 2014 jjolly@suse.com
- Add changes to allow build for s390x arch: added
  grub2-s390x-01-Changes-made-and-files-added-in-order-to-allow-s390x.patch
* Wed Jan 22 2014 mchang@suse.com
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * Fix bootable snapshots not found while root is on Btrfs subvolume
  (bnc#859587)
  * Create missing slave config in /.snapshots/<num>/
  * Prefix with SUSE_ for related options
* Fri Jan 17 2014 mchang@suse.com
- refresh 0001-script-provide-overridable-root-by-subvol.patch
  * Introduce $boot_prefix for setting prefix on seeking other /boot
  directory.
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * Support existing snapshots by creating their missing slave configs.
  * Temporarily default to disable this feature until receiving more
  tests from QA.
  * Introduce GRUB_ENABLE_CUSTOM_SNAPSHOT_SUBMENU to allow custom
  submenu for listing snapshots rather than the default one.
* Wed Jan 15 2014 arvidjaar@gmail.com
- package autoiso.cfg and osdetect.cfg as documentation
- add 0001-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch -
  fix configure test for DejaVu font
- add dejavu-fonts to BR (needed to build starfield theme)
- package starfield theme as grub2-branding-upstream
- add grub2-use-DejaVuSansMono-for-starfield-theme.patch - use fixed width
  font for starfield theme
- clarify that grub2 subpackage contains only user space tools
* Wed Jan 15 2014 mchang@suse.com
- add new patches for booting btrfs snapshot (fate#316522) (fate#316232)
  * 0001-script-provide-overridable-root-by-subvol.patch
  * 0002-script-create-menus-for-btrfs-snapshot.patch
* Fri Dec 27 2013 arvidjaar@gmail.com
- update to grub-2.02 beta2
  * drop upstream patches
  - grub2-fix-unquoted-string-in-class.patch (different)
  - grub2-cdpath.patch (modified)
  - grub2-fix-parsing-of-short-LVM-PV-names.patch
  - grub2-fix-descriptor-leak-in-grub_util_is_imsm.patch
  - grub2-install-opt-skip-fs-probe.patch (file it patched no more exists,
    functionality included upstream)
  - grub2-fix-x86_64-efi-startup-stack-alignment.patch
  - grub2-fix-x86_64-efi-callwrap-stack-alignment.patch
  - 0001-Fix-build-with-FreeType-2.5.1.patch
  * rediff
  - grub2-linux.patch
  - use-grub2-as-a-package-name.patch (do not patch generated configure)
  - grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
  - grub2-fix-locale-en.mo.gz-not-found-error-message.patch (upstream added
    explicit exclusion for en_* language only; I do not see reason to stop
    with error in this case for any language).
  - not-display-menu-when-boot-once.patch
  - grub2-secureboot-provide-linuxefi-config.patch
  - grub2-pass-corret-root-for-nfsroot.patch
  - 0002-btrfs-add-ability-to-boot-from-subvolumes.patch
  - grub2-fix-menu-in-xen-host-server.patch
  - grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - rename-grub-info-file-to-grub2.patch
  * drop Makefile.util.am and Makefile.core.am, they are now generated
    during build
  * call ./autogen.sh again now when it does not need autogen anymore; drop
    autoreconf call, it is called by autogen.sh
  * drop 0001-btrfs-rename-skip_default-to-follow_default.patch - is not
    needed anymore due to upstream changes
  * package /usr/bin/grub2-file, /usr/bin/grub2-syslinux2cfg and
    /usr/sbin/grub2-macbless
  * use grub-install --no-bootsector instead of --grub-setup=/bin/true
    in postinstall script
* Tue Dec 17 2013 mchang@suse.com
- add new patches for booting btrfs snapshot (fate#316522) (fate#316232)
  * 0001-btrfs-rename-skip_default-to-follow_default.patch
  * 0002-btrfs-add-ability-to-boot-from-subvolumes.patch
  * 0003-cmdline-add-envvar-loader_cmdline_append.patch
  * 0004-btrfs-export-subvolume-envvars.patch
* Tue Dec 10 2013 arvidjaar@gmail.com
- add patch 0001-Fix-build-with-FreeType-2.5.1.patch - fix build with
  freetype2 >= 2.5.1 (backport from fd0df6d098b1e6a4f60275c48a3ec88d15ba1fbb)
* Sun Dec  1 2013 arvidjaar@gmail.com
- reset executable bits on *module, *.exec and *.image files. They are not
  executable.
* Fri Nov 22 2013 glin@suse.com
- add grub2-fix-x86_64-efi-startup-stack-alignment.patch and
  grub2-fix-x86_64-efi-callwrap-stack-alignment.patch: fix the
  stack alignment of x86_64 efi. (bnc#841426)
* Wed Sep 11 2013 mchang@suse.com
- use new update-bootloader option --reinit to install and update
  bootloader config
- refresh grub2-secureboot-no-insmod-on-sb.patch to fobid module
  loading completely.
* Mon Sep  9 2013 lnussel@suse.de
- replace openSUSE UEFI certificate with new 2048 bit certificate.
* Sat Jul 27 2013 arvidjaar@gmail.com
- add grub2-fix-parsing-of-short-LVM-PV-names.patch - fix PV detection in
  grub-probe when PV name is less than 10 charaters
- add grub2-fix-descriptor-leak-in-grub_util_is_imsm.patch - fix decriptor
  leak which later caused LVM warnings during grub-probe invocation
- remove --enable-grub-emu-usb - it is not needed on physical platform
* Tue Jul  9 2013 mchang@suse.com
- refresh grub2-fix-menu-in-xen-host-server.patch: In domU we
  have to add xen kernel to config. (bnc#825528)
* Wed Jun 26 2013 elchevive@opensuse.org
- updated existent translations and include new ones
  (es, lt, pt_BR, sl, tr)
* Sun Jun 16 2013 arvidjaar@gmail.com
- update to current upstream trunk rev 5042
  * drop upstream patches
  - grub2-correct-font-path.patch
  - grub2-fix-mo-not-copied-to-grubdir-locale.patch
  - grub2-stdio.in.patch
  - grub2-fix-build-error-on-flex-2.5.37.patch
  - grub2-quote-messages-in-grub.cfg.patch
  - 30_os-prober_UEFI_support.patch
  - grub2-fix-enumeration-of-extended-partition.patch
  - grub2-add-device-to-os_prober-linux-menuentry.patch
  - grub2-fix-tftp-endianness.patch
  - efidisk-ahci-workaround
  - grub2-grub-mount-return-failure-if-FUSE-failed.patch
  * rediff
  - rename-grub-info-file-to-grub2.patch
  - grub2-linux.patch
  - use-grub2-as-a-package-name.patch
  - grub2-iterate-and-hook-for-extended-partition.patch
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - grub2-secureboot-chainloader.patch
  * add
  - grub2-linguas.sh-no-rsync.patch
    + disable rsync in linguas.sh so it can be used during RPM build
    + disable auto-generated catalogs, they fail at the moment due to
    missing C.UTF-8 locale
  * update Makefile.util.am and Makefile.core.am
  * grub2-mknetdir is now in /usr/bin
  * generate po/LINGUAS for message catalogs using distributed linguas.sh
  * remove po/stamp-po during setup to trigger message catalogs rebuild
  * package bootinfo.txt on PPC (used by grub2-mkrescue)
* Sat Apr 13 2013 arvidjaar@gmail.com
- BuildRequires: help2man to generate man pages and package them too
* Fri Apr  5 2013 arvidjaar@gmail.com
- add grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch (bnc#810912)
  * use linuxefi in 30_os-prober if secure boot is enabled
* Wed Apr  3 2013 arvidjaar@gmail.com
- update rename-grub-info-file-to-grub2.patch
  * do not rename docs/grub2.texi here, do it in %%%%prep (we do it there
    conditionally already). It simplifies patch refreshing using quilt
    which does not support file rename.
* Wed Apr  3 2013 mchang@suse.com
- refresh grub2-secureboot-chainloader.patch: Fix wrongly aligned
  buffer address (bnc#811608)
* Thu Mar 28 2013 mchang@suse.com
- package Secure Boot CA file as /usr/lib64/efi/grub.der which
  could be used to verify signed image from build server
- add openSUSE-UEFI-CA-Certificate.crt, openSUSE Secure Boot CA
- add SLES-UEFI-CA-Certificate.crt, SUSE Linux Enterprise Secure
  Boot CA
* Mon Mar 25 2013 dvaleev@suse.com
- extraconfigure macro is not defined on ppc
* Sat Mar 23 2013 arvidjaar@gmail.com
- corretly set chainloaded image device handle in secure boot mode (bnc#809038)
* Wed Mar 13 2013 mchang@suse.com
- remove all compatible links in grub2-efi as now all concerned
  utilities are fixed
- superseding grub2-efi by grub2-x86_64-efi and grub2-i386-efi on
  x86_64 and ix86 respectively
- make grub2-x86_64-efi and grub2-i386-efi providing grub2-efi
  capability to not break package dependency
- handle upgrade from 12.2 by preseving grubenv and custom.cfg to
  new directory /boot/grub2, rename /boot/grub2-efi to
  /boot/grub2-efi.rpmsave to avoid confusion.
* Mon Mar 11 2013 arvidjaar@gmail.com
- move post scripts into corresponding subpackages to ensure they are
  run after updated binaries are installed. Currently it may happen
  that update-bootlader picks up old binaries.
- move requires for perl-Bootloader to target subpackages. Make sure
  efi requires minimal version that supports /boot/grub2.
- add requires(post) to force order of installation: grub2 => grub2-arch
  => grub2-efi
- split efi post in two parts. One that updates configuration and is part
  of grub2-efiarch and second that migrates settings and is part of
  grub2-efi. Only custom.cfg and grubenv may need migration. device.map
  is not relevant for EFI and new grub.cfg had been created at this point.
* Mon Mar 11 2013 mchang@suse.com
- add grub2-fix-tftp-endianness.patch from upstream (bnc#808582)
- add efinet and tftp to grub.efi (bnc#808582)
* Thu Mar  7 2013 seife+obs@b1-systems.com
- convert spec file to UTF-8
* Thu Mar  7 2013 mchang@suse.com
- add lvm to grub.efi (bnc#807989)
- add loadenv to grub.efi (bnc#807992)
* Mon Mar  4 2013 arvidjaar@gmail.com
- grub2-grub-mount-return-failure-if-FUSE-failed.patch - return error
  if fuse_main failed (bnc#802983)
* Mon Feb 25 2013 fcrozat@suse.com
- Fix build for SLES 11.
* Tue Feb 19 2013 duwe@suse.com
  Fix up bogus items from the previous merge:
  - efi_libdir = _libdir = /usr/lib
  - package /usr/lib/grub2 dir only once
  - move grub.efi to /usr/lib/grub2/%%{grubefiarch}/
  - create a symlink so that scripts can find it there.
* Thu Feb 14 2013 duwe@suse.com
- merge internal+external BS changes into superset spec file,
  remove obsolete dependencies
- merge SLES+openSUSE patches, restrict "grub-efi" to 12.2
- add efidisk-ahci-workaround (bnc#794674)
- fix unquoted-string-in-class.patch (bnc#788322)
* Fri Feb  8 2013 mchang@suse.com
- adapt to pesign-obs-integration changes
* Thu Feb  7 2013 mchang@suse.com
- grub.efi signing on build server.
* Thu Jan 31 2013 duwe@suse.com
- switch to out of source / subdir build
* Wed Jan 30 2013 mchang@suse.com
- sync from SLE-11 SP3 to date
- set empty prefix to grub.efi for looking up in current directory
- grub2-cdpath.patch: fix the grub.cfg not found when booting from
  optical disk
- put grub.efi in grub2's source module directory
- create links in system's efi directory to grub.efi
- arvidjaar: do not overwrite device path in grub2-cdpath.patch
* Wed Jan 30 2013 arvidjaar@gmail.com
- remove obsolete reference to /boot/grub2-efi and /usr/sbin/grub2-efi
  from grub2-once
- add GRUB_SAVEDFAULT description to /etc/default/grub
* Tue Jan 29 2013 mchang@suse.com
- set empty prefix to grub.efi for looking up in current directory
- remove grubcd.efi, as grub.efi can now be used for cdrom booting
* Mon Jan 28 2013 snwint@suse.de
- add fat module to grubcd
- explicitly set empty prefix to get grub to set $prefix to the currrent
  directory
* Fri Jan 18 2013 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- add grub2-secureboot-chainloader.patch, which expands the efi
  chainloader to be able to verify images via shim lock protocol.
* Fri Jan 18 2013 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485).
- update for cdrom boot support.
- grub2-cdpath.patch: fix the grub.cfg not found when booting from
  optical disk.
- grubcd.efi: the efi image used for optial disk booting, with
  reduced size and $prefix set to /EFI/BOOT.
* Tue Jan  8 2013 mchang@suse.com
- add grub2-fix-unquoted-string-in-class.patch (bnc#788322)
* Tue Jan  8 2013 arvidjaar@gmail.com
- add grub2-add-device-to-os_prober-linux-menuentry.patch (bnc#796919)
* Sun Jan  6 2013 arvidjaar@gmail.com
- add patch grub2-fix-enumeration-of-extended-partition.patch to
  fix enumeration of extended partitions with non-standard EBR (bnc#779534)
* Fri Jan  4 2013 arvidjaar@gmail.com
- add support for chainloading another UEFI bootloader to
  30_os-prober (bnc#775610)
* Fri Dec 21 2012 mchang@suse.com
- put 32-bit grub2 modules to /usr/lib/grub2
- put 64-bit grub2 modules to /usr/lib64/grub2 (x86_64-efi)
- put grub.efi to /usr/lib64/efi(x86_64) or /usr/lib/efi(i586)
* Tue Dec 18 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- add grub2-secureboot-chainloader.patch, which expands the efi
  chainloader to be able to verify images via shim lock protocol.
* Fri Nov 30 2012 mchang@suse.com
- replace %%{sles_version} by %%{suse_version}
- use correct product name
* Mon Nov 26 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- added secureboot patches which introduces new linuxefi module
  that is able to perform verifying signed images via exported
  protocol from shim. The insmod command will not function if
  secure boot enabled (as all modules should built in grub.efi
  and signed).
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-use-linuxefi-on-uefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - grub2-secureboot-provide-linuxefi-config.patch
- Makefile.core.am : support building linuxefi module
- Make grub.efi image that is with all relevant modules incorporated
  and signed, it will be the second stage to the shim loader which
  will verified it when secureboot enabled.
- Make grub.efi's path to align with shim loader's default loader
  lookup path.
- The changes has been verified not affecting any factory instalation,
  but will allow us to run & test secure boot setup manually with shim.
* Thu Nov 22 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- In SLE-11 SP3, don't include any other architecture binaries
  except EFI, so we split packages by architecture binaries to
  meet the requirement.
  - grub2 : common utilties and config etc
  - grub2-efi : provide compatibilty to grub2-efi package
  - grub2-i386-pc : binaries for x86 legacy pc firmware
  - grub2-i386-efi : binaries for ia32 EFI firmware
  - grub2-x86_64-efi : binaries for x86_64 firmware
  - grub2-powerpc-ieee1275: binaries for powerpc open firmware
* Tue Nov 20 2012 arvidjaar@gmail.com
- update grub2-quote-messages-in-grub.cfg.patch to use upstream commit
* Mon Nov 19 2012 arvidjaar@gmail.com
- quote localized "Loading ..." messages in grub.cfg (bnc#790195)
* Mon Nov  5 2012 aj@suse.de
- We really only need makeinfo, so require that one where it exists.
* Thu Nov  1 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- Secure boot support in installer DVD (fate#314489)
- prime support for package on SLE-11 (SP3)
  - remove buildrequire to libuse and ncurses 32-bit devel packages
    as they are needed by grub-emu which we don't support
  - remove buildrequire to freetype2-devel-32bit as it's not need
    by grub2-mkfont and others
  - buildrequire to xz instead of lzma
  - buildrequire to texinfo instead of makeinfo
  - remove buildrequire to autogen as it's not available in SLE-11
  - add Makefile.util.am Makefile.core.am generated by autogen
  - run autoreconf -vi instead of ./autogen.sh
  - For SLE-11 remove buildrequire to gnu-unifont as it's not
    yet available. Also do not package pf fonts created from it.
  - workaround SLE-11 patch utility not rename file for us
  - add -fno-inline-functions-called-once to CFLAGS to fix build
    error on gcc 4.3.x
  - not require os-prober for SLE-11, as package not yet ready
* Sat Oct 27 2012 arvidjaar@gmail.com
- grub2-efi now depends on exact grub2 version
* Thu Oct 25 2012 arvidjaar@gmail.com
- build grub2-efi with standard "grub2" prefix (bnc#782891)
  - remove use-grub2-efi-as-a-package-name.patch
  - migrate settings from /boot/grub2-efi to /boot/grub2 in efi post
  - provide some compatibility links grub2-efi-xxx for perl-Bootloader
  - workaround for /boot/grub2-efi linkk and /boot/grub2/grub.cfg
    missing on update from older versions
* Thu Oct 25 2012 mchang@suse.com
- add grub2-fix-build-error-on-flex-2.5.37.patch
* Thu Oct 18 2012 arvidjaar@gmail.com
- modify patch grub2-iterate-and-hook-for-extended-partition.patch to
  ignore extended partitions other then primary (bnc#785341)
* Wed Sep 26 2012 mchang@suse.com
- refresh grub2-fix-locale-en.mo.gz-not-found-error-message.patch
  with the correct fix in upstream bugzilla #35880 by Colin Watson
  (bnc#771393)
* Fri Sep 21 2012 mchang@suse.com
- grub2-fix-locale-en.mo.gz-not-found-error-message.patch (bnc#771393)
* Wed Sep 19 2012 arvidjaar@gmail.com
- add 20_memtest86+ (bnc#780622)
* Tue Sep 18 2012 mchang@suse.com
- Fix un-bootable grub2 testing entry in grub's menu.lst (bnc#779370)
- Not add new grub2 testing entry if it's not found in menu.lst
- Update grub2 stuff and config if there's grub2 entry in menu.lst
- Check for current bootloader as update-bootloader acts on it
* Thu Aug 30 2012 mchang@suse.com
- add grub2-fix-Grub2-with-SUSE-Xen-package-install.patch (bnc#774666)
- add grub2-pass-corret-root-for-nfsroot.patch (bnc#774548)
* Mon Aug 20 2012 mchang@suse.com
- disable grub2-enable-theme-for-terminal-window.patch to use
  default black background due to current background has poor
  contrast to the font color (bnc#776244).
* Fri Aug 10 2012 jslaby@suse.de
- rename grub2once to grub2-once
* Wed Aug  1 2012 mchang@suse.com
- add grub2once (bnc#771587)
- add not-display-menu-when-boot-once.patch
* Sat Jul 28 2012 aj@suse.de
- Fix build with missing gets declaration (glibc 2.16)
* Fri Jul 27 2012 tittiatcoke@gmail.com
- Add grub2-enable-theme-for-terminal-window.patch (bnc#770107)
* Thu Jul 19 2012 mchang@suse.com
- add grub2-fix-menu-in-xen-host-server.patch (bnc#757895)
* Wed Jul 18 2012 mchang@suse.com
- add grub2-fix-error-terminal-gfxterm-isn-t-found.patch
- add grub2-fix-mo-not-copied-to-grubdir-locale.patch
* Wed Jul 18 2012 aj@suse.de
- We only need makeinfo, not texinfo for building.
* Tue Jul 17 2012 jslaby@suse.de
- fix build by adding texinfo to buildrequires.
* Fri Jul  6 2012 mchang@suse.com
- grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch. We
  don't run in sigle user mode for recovery, instead use different
  set kernel command line options which could be specified by this
  GRUB_CMDLINE_LINUX_RECOVERY setting.
* Wed Jul  4 2012 mchang@suse.com
- add use-grub2-efi-as-a-package-name.patch (bnc#769916)
* Fri Jun 29 2012 dvaleev@suse.com
- Add configuration support for serial terminal consoles. This will
  set the maximum screen size so that text is not overwritten.
* Fri Jun 29 2012 dvaleev@suse.com
- don't enable grub-emu-usb on ppc ppc641
* Thu Jun 28 2012 jslaby@suse.de
- update to 2.0 final
  * see ChangeLog for changes
* Mon Jun 25 2012 adrian@suse.de
- enable xz/lzma support for image file generation
* Sun Jun 24 2012 jslaby@suse.de
- update to 2.0 beta6, a snapshot from today
  * see ChangeLog for changes
* Fri Jun 22 2012 mchang@suse.com
- do not package grub.cfg, as it's generated at runtime and the
  presence of it would confuse pygrub (bnc#768063)
* Wed May 16 2012 mchang@suse.com
- fix build error on 12.1 caused by autogen aborts because of
  absence of guile package
* Wed May  2 2012 mchang@suse.com
- grub2-automake-1-11-2.patch : fix grub2 build error on newer
  autotools (automake >= 1.11.2)
- call ./autogen.sh
* Thu Apr 19 2012 mchang@suse.com
- grub2-probe-disk-mountby.patch : fix grub2-probe fails on
  probing mount-by devices under /dev/disk/by-(id|uuid|path).
  (bnc#757746)
* Thu Mar 29 2012 mchang@suse.com
- Add Requires to os-prober as script depends on it for probing
  foreign os (bnc#753229)
* Wed Mar 21 2012 mchang@suse.com
- Mark %%config(noreplace) to /etc/default/grub (bnc#753246)
* Fri Mar 16 2012 aj@suse.de
- Fix build with gcc 4.7 (needs -fno-strict-aliasing for zfs code).
* Tue Mar 13 2012 mchang@suse.com
- Fix error in installation to extended partition (bnc#750897)
  add grub2-iterate-and-hook-for-extended-partition.patch
  add grub2-install-opt-skip-fs-probe.patch
* Mon Mar 12 2012 tittiatcoke@gmail.com
- Added BuildRequires for gnu-unifont in order to create the
  necessary fonts for a graphical boot menu.
* Mon Feb 20 2012 andrea.turrini@gmail.com
- fixed typos in grub2.spec
* Mon Jan  2 2012 mchang@suse.com
- platforms without efi should not specify exclusion of it
* Thu Dec 29 2011 mchang@suse.com
- set --target=%%{_target_plaform) explicitly to %%configure in case
  it wouldn't do that for us implicitly
- when making x86_64-efi image not use i386 target build and keep
  use of x86_64. otherwise it would have error "invalid ELF header"
* Fri Dec  2 2011 coolo@suse.com
- add automake as buildrequire to avoid implicit dependency
* Mon Nov 28 2011 jslaby@suse.de
- remove doubly packaged files
- remove INSTALL from docs
- handle duplicate bindir files
* Mon Oct 31 2011 meissner@suse.de
- make efi exclusion more complete
* Thu Oct 27 2011 aj@suse.de
- efibootmgr only exists on x86-64 and ia64.
* Tue Oct 25 2011 aj@suse.de
- Add requires from efi subpackage to main package (bnc#72596)
* Mon Oct 24 2011 jslaby@suse.de
- update it and pl translations
- cleanup spec file
  * don't package efi files to non-efi package
* Thu Aug 25 2011 aj@suse.de
- Fix directory ownership.
* Tue Aug 23 2011 aj@suse.de
- Build an efi subpackage [bnc#713595].
* Tue Aug  2 2011 dvaleev@novell.com
- enable ppc build
- patch unused-but-set-variable
* Tue Jul 12 2011 aj@suse.de
- Create submenu for all besides primary Linux kernels.
- Only run preun section during package install but not during
  upgrade.
* Tue Jul 12 2011 aj@suse.de
- Update README.openSUSE
* Tue May 31 2011 jslaby@suse.de
- update translations
- update to 1.99 final
  * See NEWS file for changes
* Sat May  7 2011 jslaby@suse.de
- fix build with gcc 4.6
- build in parallel (fixed finally in 1.99)
- add translations from translations project
- update to 1.99-rc2
  * See NEWS file for changes
* Wed Oct 27 2010 jslaby@suse.de
- fix vanishing of /boot/grub2/* if /boot/grub/device.map
  doesn't exist
* Mon Oct 25 2010 jslaby@suse.de
- add missing " in the default file; add "fi" to grub2-linux.patch
* Mon Oct 11 2010 jslaby@suse.de
- repack gz to bz2 (0.5M saving)
* Sat Oct  9 2010 aj@suse.de
- Do not output vmlinux if vmlinuz of same version exists.
- Update default grub file.
* Sat Oct  9 2010 aj@suse.de
- Add patch grub-1.98-follow-dev-mapper-symlinks.patch from Fedora
  for grub2-probe to detect lvm devices correctly
* Sat Sep 11 2010 jslaby@suse.de
- add gettext "requires"
* Sun Mar 14 2010 aj@suse.de
- Fix build on x86-64.
* Fri Mar 12 2010 aj@suse.de
- Don't build parallel.
- Update to grub 1.98 including:
  * Multiboot on EFI support.
  * Saved default menu entry support, with new utilities `grub-reboot' and
    `grub-set-default'.
  * Encrypted password support, with a new utility `grub-mkpasswd-pbkdf2'.
  * `grub-mkfloppy' removed; use `grub-mkrescue' to create floppy images.
* Fri Feb 12 2010 aj@suse.de
- Update to grub 1.97.2:
  * Fix a few 4 GiB limits.
  * Fix license problems with a few BSD headers.
  * Lots of misc bugfixes.
* Wed Dec  9 2009 aj@suse.de
- Fix requires.
* Wed Dec  9 2009 aj@suse.de
- Mark /etc/default/grub as config file.
* Wed Dec  9 2009 aj@suse.de
- Mark root partition rw
* Wed Dec  9 2009 aj@suse.de
- New package grub2.
