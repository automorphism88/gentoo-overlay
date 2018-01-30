# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
SLOT=0
DESCRIPTION="Script for using snapraid with btrfs snapshots"
LICENSE="GPL-3+"

if [[ "${PV}" = 9999 ]] ; then
	inherit git-r3
	KEYWORDS=""
	EGIT_REPO_URI="https://github.com/automorphism88/snapraid-btrfs.git"
	SRC_URI=""
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/automorphism88/snapraid-btrfs/archive/v${PV}.tar.gz -> ${P}.tar.gz"
fi

RDEPEND="app-backup/snapper[btrfs]
	sys-fs/snapraid
	>=app-shells/bash-4.1
	virtual/awk"

src_install() {
	dobin snapraid-btrfs
	dodoc README.md
}
