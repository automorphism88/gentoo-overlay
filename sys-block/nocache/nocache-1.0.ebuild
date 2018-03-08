# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit multilib

DESCRIPTION="Minimize the effect a program has on the file system cache"
HOMEPAGE="https://github.com/Feh/nocache/"
LICENSE="BSD-2"
SLOT=0

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/Feh/nocache"
	KEYWORDS=""
else
	SRC_URI="https://github.com/Feh/nocache/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

src_install() {
	emake DESTDIR="${D}" PREFIX="${EPREFIX%/}/usr" LIBDIR="/$(get_libdir)" \
		install
	einstalldocs
}
