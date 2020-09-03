# Copyright 1999-2020 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
DESCRIPTION="Optional tools to help manage data in a mergerfs pool"
HOMEPAGE="https://github.com/trapexit/mergerfs-tools"
LICENSE="ISC"
SLOT=0
PYTHON_COMPAT=( python3_{6,7,8,9} )

inherit git-r3 python-r1
SRC_URI=""
EGIT_REPO_URI="https://github.com/trapexit/mergerfs-tools"
KEYWORDS=""

RDEPEND="sys-fs/mergerfs
	${PYTHON_DEPS}"
DEPEND="${RDEPEND}"
REQUIRED_USE="${PYTHON_REQUIRED_USE}"

src_compile() {
	return
}

src_install() {
	local i
	for i in balance consolidate ctl dedup dup fsck ; do
		python_foreach_impl python_doexe "src/mergerfs.$i"
	done
	dobin src/mergerfs.mktrash
	einstalldocs
}
