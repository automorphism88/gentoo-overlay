# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

inherit eutils cmake-utils

DESCRIPTION="A 3D-accelerated Doom source port based on ZDoom code"
HOMEPAGE="https://gzdoom.drdteam.org/"
SRC_URI="https://zdoom.org/files/gzdoom/src/${PN}-g${PV}.zip"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="fluidsynth +gtk openal timidity"

RDEPEND="fluidsynth? ( media-sound/fluidsynth )
	gtk? ( x11-libs/gtk+ )
	openal? ( media-libs/libsndfile
			  media-libs/openal
			  media-sound/mpg123 )
	timidity? ( media-sound/timidity++ )
	media-libs/game-music-emu
	>=media-libs/libsdl2-2.0.2
	media-libs/mesa
	media-sound/wildmidi
	sys-libs/zlib
	virtual/glu
	virtual/jpeg
	virtual/opengl"

DEPEND="${RDEPEND}
	x86? ( >=dev-lang/nasm-0.98.39 )"

S="${WORKDIR}/${PN}-g${PV}"

src_prepare() {
	sed -i -e "s:/usr/local/share/:/usr/share/games/doom/:" src/posix/i_system.h
	eapply_user
}

src_configure() {
	mycmakeargs=()
	use gtk || mycmakeargs+="-DNO_GTK=ON"
	use openal || mycmakeargs+="-DNO_OPENAL=ON"
	cmake-utils_src_configure
}

src_install() {
	dodoc docs/*.txt
	dohtml docs/console*.{css,html}

	newicon "src/win32/icon1.ico" "${PN}.ico"
	make_desktop_entry "${PN}" "GZDoom" "${PN}.ico" "Game;ActionGame;"

	cd "${BUILD_DIR}"

	insinto "/usr/share/games/doom"
	doins *.pk3

	dobin "${PN}"
}

pkg_postinst() {
	elog "Copy or link wad files into /usr/share/games/doom/"
}
