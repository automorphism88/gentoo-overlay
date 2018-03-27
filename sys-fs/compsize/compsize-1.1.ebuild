# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
SLOT=0
DESCRIPTION="Utility to find btrfs compression ratio"
HOMEPAGE="https://github.com/kilobyte/compsize"
LICENSE="GPL-2+"
DEPEND="sys-fs/btrfs-progs"
RDEPEND=""
inherit flag-o-matic
# Used in upstream Makefile, but clobbered by portage's CFLAGS
append-cflags -Wall -std=gnu90

if [[ "$PV" = 9999 ]] ; then
	inherit git-r3
	KEYWORDS=""
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/kilobyte/compsize"
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/kilobyte/compsize/archive/v${PV}.tar.gz -> ${P}.tar.gz"
fi

src_install() {
	# work around Makefile failing to create this directory
	mkdir -p "${ED}/usr/share/man/man8" || die
	emake PREFIX="$ED" install
	einstalldocs
}
