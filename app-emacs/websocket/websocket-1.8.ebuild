# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit elisp

DESCRIPTION="A websocket implementation in elisp, for emacs"
HOMEPAGE="https://github.com/ahyatt/emacs-websocket"
LICENSE="GPL-3+"
SLOT=0
KEYWORDS="~amd64 ~x86"

SRC_URI="https://github.com/ahyatt/emacs-websocket/archive/${PV}.tar.gz -> ${P}.tar.gz"
S="${WORKDIR}/emacs-${P}"
DOCS="README.org"
