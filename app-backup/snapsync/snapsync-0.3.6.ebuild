# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
USE_RUBY="ruby22 ruby23"
inherit ruby-fakegem
SLOT=0

DESCRIPTION="A synchronization tool for snapper based on btrfs send/receive"
HOMEPAGE="https://github.com/doudou/snapsync"
LICENSE="MIT"
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/doudou/snapsync/archive/v${PV}.tar.gz -> ${P}.tar.gz"

ruby_add_rdepend ">=dev-ruby/concurrent-ruby-0.9.0
				 >=dev-ruby/logging-2.0.0
				 >=dev-ruby/ruby-dbus-0.11.0
				 >=dev-ruby/thor-0.19.1"
