# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
DESCRIPTION="Featureful FUSE-based union filesystem"
HOMEPAGE="https://github.com/trapexit/mergerfs"
LICENSE="ISC"
SLOT=0

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/trapexit/mergerfs"
	KEYWORDS=""
else
	SRC_URI="https://github.com/trapexit/mergerfs/archive/${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

RDEPEND="sys-apps/attr
		sys-devel/gettext
		sys-fs/fuse"
DEPEND="app-text/pandoc
		${RDEPEND}"

PATCHES=( "${FILESDIR}/makefile-respect-user-cflags.patch" )

src_prepare() {
	[[ "${PV}" == 9999 ]] && emake src/version.hpp
	eapply "${PATCHES[@]}"
	eapply_user
}

src_install() {
	emake DESTDIR="${D}" PREFIX="/usr" install
	einstalldocs
}
