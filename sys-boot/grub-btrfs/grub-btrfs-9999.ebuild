# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=4
SLOT=0

DESCRIPTION="grub2 plugin for btrfs snapshots"
HOMEPAGE="https://github.com/Antynea/grub-btrfs/"

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/Antynea/grub-btrfs/"
	KEYWORDS=""
else
	SRC_URI="https://github.com/Antynea/grub-btrfs/archive/v${PV}.tar.gz"
	KEYWORDS="~amd64"
fi

RDEPEND="sys-boot/grub:2"
DEPEND="${RDEPEND}"

src_prepare()
{
	sed -i 's/#! \/usr\/bin\/bash/#!\/usr\/bin\/env bash/' 41_snapshots-btrfs ||
		die "Couldn't sed shebang in 41_snapshots-btrfs"
}

src_install()
{
	insinto /etc/grub.d
	doins 41_snapshots-btrfs
	newdoc README.md README
}
