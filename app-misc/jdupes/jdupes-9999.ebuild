# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
DESCRIPTION="Fork of fdupes with better performance and btrfs deduplication support"
HOMEPAGE="https://github.com/jbruchon/jdupes"
LICENSE="MIT"
SLOT=0
IUSE="+btrfs custom-optimization debug hardened"

if [[ ${PV} == 9999 ]] ; then
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/jbruchon/jdupes"
	KEYWORDS=""
else
	SRC_URI="https://github.com/jbruchon/jdupes/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

src_prepare() {
	eapply_user
	sed -i -e 's/ -pipe//' -e 's/-g //' Makefile || die
	use custom-optimization && { sed -i 's/-O2 //' Makefile || die ; }
}

src_compile() {
	local -a mymakeopts
	mymakeopts=()
	use btrfs && mymakeopts+=('ENABLE_BTRFS=1')
	use debug && mymakeopts+=('DEBUG=1' 'LOUD=1')
	use hardened && mymakeopts+=('HARDEN=1')
	emake "${mymakeopts[@]}"
}

src_test() {
	# success of this command does not guarantee that its output is correct
	./jdupes -r testdir || die
}
