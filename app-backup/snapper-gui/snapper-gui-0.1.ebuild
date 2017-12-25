# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python3_{4,5,6} )

DESCRIPTION="GUI for snapper, a tool for Linux filesystem snapshot management"
HOMEPAGE="https://github.com/ricardomv/snapper-gui"
inherit distutils-r1
if [[ "${PV}" = 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/ricardomv/${PN}.git"
	SRC_URI=""
	KEYWORDS=""
else
	SRC_URI="https://github.com/ricardomv/${PN}/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

LICENSE="GPL-2"
SLOT="0"
IUSE=""

DEPEND="${RDEPEND}"
RDEPEND="
	${PYTHON_DEPEND}
	app-backup/snapper
	dev-python/dbus-python
	dev-python/pygobject
	x11-libs/gtksourceview
"

src_prepare() {
	cp "${FILESDIR}/snapper-gui.desktop" snapper-gui.desktop || die
	eapply_user
}
