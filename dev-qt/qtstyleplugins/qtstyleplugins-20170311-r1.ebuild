# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

inherit qmake-utils

DESCRIPTION="Additional style plugins for Qt"
HOMEPAGE="https://code.qt.io/cgit/qt/qtstyleplugins.git"
LICENSE="LGPL-2.1"
SLOT="0"

if [[ "${PV}" = 99999999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://code.qt.io/cgit/qt/qtstyleplugins.git"
	EGIT_BRANCH="master"
	SRC_URI=""
	KEYWORDS=""
else
	KEYWORDS="amd64 x86"
	SRC_URI="https://github.com/automorphism88/qtstyleplugins/archive/${PV}.tar.gz -> ${P}.tar.gz"
fi

RDEPEND="dev-qt/qtcore:5=
		 x11-libs/gtk+:2
		 x11-libs/libX11"
DEPEND="${RDEPEND}"

src_configure() {
	eqmake5 PREFIX="${EPREFIX%/}/usr"
}

src_install() {
	emake INSTALL_ROOT="${D}" install
}
