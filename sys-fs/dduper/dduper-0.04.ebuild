# Copyright 2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7

PYTHON_COMPAT=( python3_{7,8,9} )
inherit python-single-r1

DESCRIPTION="btrfs deduplication tool using precomputed filesystem checksums"
HOMEPAGE="https://github.com/Lakshmipathi/dduper"
SRC_URI="https://github.com/Lakshmipathi/dduper/archive/v${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""
REQUIRED_USE="${PYTHON_REQUIRED_USE}"

RDEPEND="
	${PYTHON_DEPS}
	$(python_gen_cond_dep '
		dev-python/numpy[${PYTHON_USEDEP}]
		dev-python/PTable[${PYTHON_USEDEP}]
	')
	sys-fs/btrfs-progs[dump-csum,python]
"
DEPEND="${RDEPEND}"

src_install() {
	python_doscript dduper
}
