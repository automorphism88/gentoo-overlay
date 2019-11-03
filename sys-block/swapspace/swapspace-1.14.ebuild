# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
SLOT=0
inherit systemd

LICENSE="GPL-2"
KEYWORDS="~amd64"
SRC_URI="https://github.com/Tookmund/Swapspace/releases/download/v${PV}/${P}.tar.gz"

src_configure() {
	econf --localstatedir=/var
}

src_install() {
	default
	keepdir /var/lib/swapspace
	systemd_dounit swapspace.service
	newinitd "${FILESDIR}/swapspace.initd" swapspace
}
