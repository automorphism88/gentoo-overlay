# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit elisp

DESCRIPTION="Major mode to edit sed scripts"
HOMEPAGE="http://elpa.gnu.org/packages/sed-mode.html"
LICENSE="GPL-3+"
SLOT=0
KEYWORDS="~amd64 ~x86"

SRC_URI="https://elpa.gnu.org/packages/${P}.el"
S="${WORKDIR}"
SITEFILE="50${PN}-gentoo.el"

src_unpack() {
	cp -a "${DISTDIR}/${P}.el" "${WORKDIR}/${PN}.el" || die
}
