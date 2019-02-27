# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
PYTHON_COMPAT=( python3_{5,6,7} )
inherit python-single-r1 cmake-utils flag-o-matic

DESCRIPTION="Open Source Commander Keen clone (needs original game files)"
HOMEPAGE="http://clonekeenplus.sourceforge.net"
SRC_URI="https://gitlab.com/Dringgstein/Commander-Genius/-/archive/v${PV}/Commander-Genius-v${PV}.tar.bz2 -> ${P}.tar.bz2"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="opengl python"
RESTRICT="mirror" # contains keen files, but we do not install them

RDEPEND="media-libs/libsdl2[X,opengl?,sound,video]
	media-libs/libvorbis
	media-libs/sdl2-image
	media-libs/sdl2-mixer
	sys-libs/zlib[minizip]
	opengl? ( virtual/opengl )
	python? ( ${PYTHON_DEPS} )"
DEPEND="${RDEPEND}
	dev-libs/boost
	virtual/pkgconfig"
REQUIRED_USE="python? ( ${PYTHON_REQUIRED_USE} )"

S="${WORKDIR}/Commander-Genius-v${PV}"

src_prepare() {
	# don't clobber existing CFLAGS
	sed -i -e '/-std=c99/d' CMakeLists.txt || die
	# fix filenames
	mv share/cgenius.desktop share/commandergenius.desktop || die
	mv src/CGLogo.png src/commandergenius.png || die
	sed -i -e 's/cgenius.desktop/commandergenius.desktop/' \
		-e 's/CGLogo.png/commandergenius.png/' \
		src/install.cmake || die
	sed -i -e 's/CGeniusExe/commandergenius/' \
		-e 's/CGLogo.png/commandergenius.png/' \
		-e '/^Categories=/s/Application;//' \
		share/commandergenius.desktop || die
	sed -i -e 's/cgenius.desktop/commandergenius.desktop/' \
		package.cmake || die
	cmake-utils_src_prepare
}

src_configure() {
	use python && python_setup
	# add the flag we removed from CMakeLists.txt in src_prepare()
	append-cflags -std=c99
	# fix bundled minizip issue
	append-cppflags -DOF=_Z_OF -DON=_Z_ON
	local -a mycmakeargs
	mycmakeargs=(
		-DAPPDIR="${EPREFIX%/}/usr/bin"
		-DSHAREDIR="${EPREFIX%/}/usr/share"
		-DDOCDIR="${EPREFIX%/}/usr/share/doc/${PF}"
		-DBUILD_TARGET="LINUX"
		-DOPENGL="$(usex opengl)"
		-DUSE_PYTHON3="$(usex python)"
		-DUSE_SDL2=1
	)
	cmake-utils_src_configure
}

src_compile() {
	cmake-utils_src_compile
}

src_install() {
	cmake-utils_src_install
	newbin "${FILESDIR}"/commandergenius-wrapper commandergenius
	mv "${ED}/usr/bin/CGeniusExe" "${ED}/usr/bin/CommanderGenius" || die
}

pkg_postinst() {
	elog "Check your settings in ~/.CommanderGenius/cgenius.cfg"
	elog "after you have started the game for the first time."
	use opengl && elog "You may also want to set \"OpenGL = true\""
	elog
	elog "Run the game via:"
	elog "    'commandergenius [path-to-keen-data]'"
	elog "or add your keen data dir to the search paths in cgenius.cfg"
}
