# Copyright 1999-2020 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
DESCRIPTION="Optional tools to help manage data in a mergerfs pool"
HOMEPAGE="https://github.com/trapexit/mergerfs-tools"
LICENSE="ISC"
SLOT=0

inherit git-r3
SRC_URI=""
EGIT_REPO_URI="https://github.com/trapexit/mergerfs-tools"
KEYWORDS=""

RDEPEND="sys-fs/mergerfs"
DEPEND="${RDEPEND}"

src_prepare() {
	sed -i '/^PREFIX/s/=/?=/' Makefile || die
	eapply_user
}

src_compile() {
	return
}

src_install() {
	emake DESTDIR="${D}" PREFIX="${EPREFIX%/}/usr" install
}
