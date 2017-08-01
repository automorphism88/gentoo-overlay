# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
PYTHON_COMPAT=( python{2_7,3_{4,5,6}} )

inherit distutils-r1

DESCRIPTION="Fast C based HTML 5 parsing for Python"
HOMEPAGE="https://github.com/kovidgoyal/html5-parser"

LICENSE="Apache-2.0"
SLOT=0

SRC_URI="https://github.com/kovidgoyal/html5-parser/archive/v${PV}.tar.gz -> ${P}.tar.gz"

RDEPEND="${PYTHON_DEPS}
	dev-python/beautifulsoup[${PYTHON_USEDEP}]
	dev-python/chardet[${PYTHON_USEDEP}]
	>=dev-python/lxml-3.8.0[${PYTHON_USEDEP}]"

KEYWORDS="~amd64 ~x86"
