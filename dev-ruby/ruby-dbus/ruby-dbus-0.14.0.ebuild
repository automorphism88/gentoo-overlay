# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
USE_RUBY="ruby22 ruby23 ruby24"
inherit ruby-fakegem
SLOT=0

DESCRIPTION="Ruby library for D-Bus"
HOMEPAGE="https://github.com/mvidner/ruby-dbus"
LICENSE="LGPL-2.1+"
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/mvidner/ruby-dbus/archive/v${PV}.tar.gz -> ${P}.tar.gz"
