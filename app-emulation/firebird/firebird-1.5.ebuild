# Copyright 2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7

inherit qmake-utils xdg

DESCRIPTION="Emulator for the TI-Nspire graphing calculator"
HOMEPAGE="https://github.com/nspire-emus/firebird"
SRC_URI="https://github.com/nspire-emus/firebird/archive/refs/tags/v${PV}.tar.gz -> ${P}.tar.gz
https://raw.githubusercontent.com/jacobly0/gif-h/8cb648fb02d3f18fb7f325cbe71bbb0a56a0bbe7/gif.h -> ${P}-gif.h"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND=">=dev-qt/qtcore-5.9:5=
>=dev-qt/qtgui-5.9:5=
>=dev-qt/qtwidgets-5.9:5="
DEPEND="${RDEPEND}"

src_unpack() {
	unpack "${P}.tar.gz"
	cp -Lv "${DISTDIR}/${P}-gif.h" "${S}/core/gif-h/gif.h" || die
}

src_prepare() {
	# avoid sandbox errors, don't try installing to live filesystem
	sed -i "s:/usr:${D}&:" firebird.pro || die
	default
}

src_compile() {
	eqmake5
	emake
}
