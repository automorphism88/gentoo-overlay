# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=6
USE_RUBY="ruby25"
inherit ruby-fakegem
SLOT=0

DESCRIPTION="Ruby library for D-Bus"
HOMEPAGE="https://github.com/mvidner/ruby-dbus"
LICENSE="LGPL-2.1+"
KEYWORDS="~amd64 ~x86"
SRC_URI="https://github.com/mvidner/ruby-dbus/archive/v${PV}.tar.gz -> ${P}.tar.gz"
RDEPEND="${RDEPEND} sys-apps/dbus"
DEPEND="${DEPEND} sys-apps/dbus"
