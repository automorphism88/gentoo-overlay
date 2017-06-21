# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit systemd

DESCRIPTION="btrfs maintenance scripts from openSUSE"
HOMEPAGE="https://github.com/kdave/btrfsmaintenance"
LICENSE="GPL-2"
SLOT=0

if [[ ${PV} == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/kdave/btrfsmaintenance"
	KEYWORDS=""
else
	SRC_URI="https://github.com/kdave/btrfsmaintenance/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

src_install()
{
	insinto /etc/default
	newins sysconfig.btrfsmaintenance btrfsmaintenance

	insinto /usr/share/btrfsmaintenance
	doins btrfsmaintenance-functions
	insopts -m0755
	doins btrfs*.sh

	dosym /usr/share/btrfsmaintenance/btrfsmaintenance-refresh-cron.sh /usr/sbin/btrfsmaintenance-refresh-cron

	systemd_dounit btrfsmaintenance-refresh.service

	newdoc README.md README
	newdoc btrfsmaintenance.changes CHANGELOG
}

pkg_postinst()
{
	elog "Settings for btrfsmaintenance are in /etc/default/btrfsmaintenance"
	elog "After editing this file, run btrfsmaintenance-refresh-cron"
	elog "or use the systemd service"
}
