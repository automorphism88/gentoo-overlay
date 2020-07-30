# Copyright 1999-2020 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
SLOT=0
inherit autotools systemd

LICENSE="GPL-2"
KEYWORDS="~amd64"
DESCRIPTION="Daemon to dynamically add swap space"
SRC_URI="https://github.com/Tookmund/Swapspace/archive/v${PV}.tar.gz -> ${P}.tar.gz"
S="${WORKDIR}/Swapspace-${PV}"

src_prepare() {
	eapply_user
	eautoreconf
	sed -i 's:/usr/local::' swapspace.conf || die
}

src_configure() {
	econf --localstatedir="${EPREFIX%/}/var" --sysconfdir="${EPREFIX%/}/etc"
}

src_install() {
	default
	doman doc/swapspace.8
	keepdir /var/lib/swapspace
	systemd_dounit swapspace.service
	newinitd "${FILESDIR}/swapspace.initd" swapspace
}
