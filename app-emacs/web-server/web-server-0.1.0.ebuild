# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
NEED_EMACS="24"
inherit elisp

DESCRIPTION="Web server running Emacs Lisp handlers"
HOMEPAGE="https://github.com/eschulte/emacs-web-server"
LICENSE="GPL-3+"
SLOT=0
KEYWORDS="~amd64 ~x86"

SRC_URI="https://github.com/eschulte/emacs-web-server/archive/version-${PV}.tar.gz -> ${P}.tar.gz"
S="${WORKDIR}/emacs-${PN}-version-${PV}"
DOCS="README"
