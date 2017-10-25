# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
NEED_EMACS="24"
inherit elisp

DESCRIPTION="Minor mode to preview Markdown output as you save"
HOMEPAGE="https://github.com/ancane/markdown-preview-mode"
LICENSE="GPL-3+"
SLOT=0
KEYWORDS="~amd64 ~x86"
RDEPEND="app-emacs/markdown-mode
		 app-emacs/uuidgen
		 app-emacs/websocket
		 app-emacs/web-server"
DEPEND="${RDEPEND}"

SRC_URI="https://github.com/ancane/markdown-preview-mode/archive/v${PV}.tar.gz -> ${P}.tar.gz"
DOCS="README.md"
