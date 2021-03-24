# Copyright 2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7

inherit xdg

DESCRIPTION="Emulator for TI graphing calculators"
HOMEPAGE="http://lpg.ticalc.org/prj_tilem/"
SRC_URI="mirror://sourceforge/tilem/${P}.tar.bz2"

LICENSE="GPL-3+"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND="sci-libs/libticalcs2
x11-libs/gtk+:2"
DEPEND="${RDEPEND}"

src_configure() {
	econf LIBS="-lm"
}
