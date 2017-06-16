# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
DESCRIPTION="Fork of fdupes with better performance and btrfs deduplication support"
HOMEPAGE="https://github.com/jbruchon/jdupes"
LICENSE="MIT"
SLOT=0

IUSE="+btrfs custom-optimization debug hardened low-memory stats"
# the LOUD_DEBUG flag enabled by USE=debug implies
# the DEBUG flag enabled by USE=stats
REQUIRED_USE="debug? ( stats )"

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
	sed -i -e 's/ -pipe//' -e 's/-g //' Makefile || die
	if use custom-optimization ; then
		sed -i 's/-O2 //' Makefile || die
	fi
	eapply_user
}

src_compile() {
	local mymakeopts=()
	use btrfs && mymakeopts+=("ENABLE_BTRFS=1")
	use debug && mymakeopts+=("LOUD=1")
	use hardened && mymakeopts+=("HARDEN=1")
	use low-memory && mymakeopts+=("LOW_MEMORY=1")
	use stats && mymakeopts+=("DEBUG=1")

	emake "${mymakeopts[@]}"
}

src_test() {
	# success of this command does not guarantee that its output is correct
	./jdupes -r testdir || die
}
