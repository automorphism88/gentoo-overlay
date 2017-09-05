# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

inherit qmake-utils git-r3

DESCRIPTION="Additional style plugins for Qt"
HOMEPAGE="https://code.qt.io/cgit/qt/qtstyleplugins.git"
LICENSE="LGPL-2.1"
SLOT="0"

EGIT_REPO_URI="https://code.qt.io/cgit/qt/qtstyleplugins.git"
EGIT_BRANCH="master"
SRC_URI=""
KEYWORDS=""

RDEPEND="dev-qt/qtcore:5
		 x11-libs/gtk+:2
		 x11-libs/libX11"
DEPEND="${RDEPEND}"

src_configure() {
	eqmake5 PREFIX="${D}"/usr
}

src_install() {
	emake INSTALL_ROOT="${D}" install
}
