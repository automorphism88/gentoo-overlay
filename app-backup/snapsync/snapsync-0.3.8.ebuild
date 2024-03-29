# Copyright 1999-2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=6
USE_RUBY="ruby26 ruby27"
inherit ruby-fakegem systemd
SLOT=0

DESCRIPTION="A synchronization tool for snapper based on btrfs send/receive"
HOMEPAGE="https://github.com/doudou/snapsync"
LICENSE="MIT"
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/doudou/snapsync/archive/v${PV}.tar.gz -> ${P}.tar.gz"

RDEPEND="${RDEPEND}
	app-backup/snapper
	sys-fs/btrfs-progs"
DEPEND="${DEPEND}
	app-backup/snapper
	sys-fs/btrfs-progs"

ruby_add_rdepend ">=dev-ruby/concurrent-ruby-0.9.0
				 >=dev-ruby/logging-2.0.0
				 >=dev-ruby/ruby-dbus-0.11.0
				 >=dev-ruby/thor-0.19.1"

src_prepare() {
	sed -i "s:/opt/snapsync:${EPREFIX%/}/usr:" \
		"all/${P}/snapsync.service" || die
	ruby-ng_src_prepare
}

src_install() {
	systemd_dounit "all/${P}/snapsync.service"
	dodoc "all/${P}/README.md"
	ruby-ng_src_install
}
