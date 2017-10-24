# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
# enable ruby24 as soon as dev-ruby/logging supports it
USE_RUBY="ruby22 ruby23"
inherit ruby-fakegem systemd
SLOT=0

DESCRIPTION="A synchronization tool for snapper based on btrfs send/receive"
HOMEPAGE="https://github.com/doudou/snapsync"
LICENSE="MIT"
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/doudou/snapsync/archive/v${PV}.tar.gz -> ${P}.tar.gz"

RDEPEND="app-backup/snapper[btrfs]"
ruby_add_rdepend ">=dev-ruby/concurrent-ruby-0.9.0
				 >=dev-ruby/logging-2.0.0
				 >=dev-ruby/ruby-dbus-0.11.0
				 >=dev-ruby/thor-0.19.1"
DEPEND="${RDEPEND}"

src_prepare() {
	sed -i 's:/opt/snapsync:/usr:' "all/${P}/snapsync.service" || die
	ruby-ng_src_prepare
}

src_install() {
	systemd_dounit "all/${P}/snapsync.service"
	ruby-ng_src_install
}
