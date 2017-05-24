# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

inherit systemd

DESCRIPTION="btrfs maintenance scripts from openSUSE"
HOMEPAGE="https://github.com/kdave/btrfsmaintenance"
LICENSE="GPL-2"

IUSE="-systemd"
SLOT=0

if [[ ${PV} == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/kdave/btrfsmaintenance"
	KEYWORDS=""
else
	SRC_URI="https://github.com/kdave/btrfsmaintenance/archive/v${PV}.tar.gz"
	KEYWORDS="~amd64"
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

	if use systemd ; then
		systemd_dounit btrfsmaintenance-refresh.service
	fi

	newdoc README.md README
	newdoc btrfsmaintenance.changes CHANGES
}

pkg_postinst()
{
	einfo "Settings for btrfsmaintenance are in /etc/default/btrfsmaintenance"
	einfo "After editing this file, run btrfsmaintenance-refresh-cron"
	if use systemd ; then
		einfo "or use the systemd service"
	fi
}
