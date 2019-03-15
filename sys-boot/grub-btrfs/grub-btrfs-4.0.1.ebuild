# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
SLOT=0

DESCRIPTION="grub2 plugin for btrfs snapshots"
HOMEPAGE="https://github.com/Antynea/grub-btrfs/"

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/Antynea/grub-btrfs/"
	KEYWORDS=""
else
	SRC_URI="https://github.com/Antynea/grub-btrfs/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64"
fi

RDEPEND="sys-boot/grub:2"
DEPEND="${RDEPEND}"

src_compile() {
	# avoid default function trying to install and creating sandbox violation
	return
}

src_install() {
	emake DESTDIR="${D}" install
}
