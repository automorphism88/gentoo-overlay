# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit elisp git-r3

DESCRIPTION="UUID generation implemented in elisp"
HOMEPAGE="https://github.com/kanru/uuidgen-el"
LICENSE="GPL-3+"
SLOT=0
KEYWORDS="~amd64 ~x86"

SRC_URI=""
EGIT_REPO_URI="${HOMEPAGE}"
EGIT_CLONE_TYPE="shallow"
EGIT_COMMIT="7eb96415484c3854a3f383d1a3e10b87ae674e22"

DOCS="README"
