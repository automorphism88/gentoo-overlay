# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit gnome2-utils

DESCRIPTION="A Widget Factory - theme preview application for GTK+2 and GTK+3"
HOMEPAGE="https://github.com/valr/awf"
LICENSE="GPL-3"
SLOT="0"
SRC_URI="https://github.com/valr/awf/archive/v${PV}.tar.gz -> ${P}.tar.gz"
KEYWORDS="~amd64 ~x86"
DEPEND="x11-libs/gtk+:2
		x11-libs/gtk+:3"
RDEPEND="${DEPEND}"

src_configure() {
	./autogen.sh
	econf
}

pkg_postinst() {
	gnome2_icon_cache_update
}

pkg_postrm() {
	gnome2_icon_cache_update
}
