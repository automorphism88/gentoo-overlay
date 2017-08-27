# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit multilib

DESCRIPTION="Start a program without caching its reads"
HOMEPAGE="https://github.com/Feh/nocache/releases"
LICENSE="BSD-2"
SLOT=0
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/Feh/nocache/archive/v${PV}.tar.gz -> ${P}.tar.gz"

src_install() {
	emake DESTDIR="${D}" PREFIX="/usr" LIBDIR="/$(get_libdir)" install
	einstalldocs
}
