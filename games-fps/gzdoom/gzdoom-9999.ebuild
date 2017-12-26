# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit eutils cmake-utils gnome2-utils flag-o-matic

DESCRIPTION="A 3D-accelerated Doom source port based on ZDoom code"
HOMEPAGE="https://gzdoom.drdteam.org/"
LICENSE="GPL-3 LGPL-2.1 BSD DUMB-0.9.2 MPL-2"
SLOT="0"
IUSE="fluidsynth +gtk kde +openal timidity"

if [[ "${PV}" = 9999 ]] ; then
	inherit git-r3
	KEYWORDS=""
	EGIT_REPO_URI="https://github.com/coelckers/gzdoom"
	SRC_URI=""
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://zdoom.org/files/gzdoom/src/${PN}-g${PV}.zip -> ${P}.zip"
	S="${WORKDIR}/${PN}-g${PV}"
fi

RDEPEND="fluidsynth? ( media-sound/fluidsynth )
	gtk? ( x11-libs/gtk+:=
		   x11-misc/gxmessage )
	kde? ( kde-apps/kdialog )
	openal? ( media-libs/libsndfile
			  media-libs/openal
			  media-sound/mpg123 )
	timidity? ( media-sound/timidity++ )
	media-libs/game-music-emu
	>=media-libs/libsdl2-2.0.2
	media-libs/mesa
	media-sound/wildmidi
	sys-libs/zlib:=
	virtual/glu
	virtual/jpeg
	virtual/opengl"
DEPEND="${RDEPEND}
	x86? ( >=dev-lang/nasm-0.98.39 )"

src_prepare() {
	sed -i -e "s:/usr/local/share/:/usr/share/:" src/posix/i_system.h || die
	sed -i -e "s/<unknown version>/${PV}/" \
		tools/updaterevision/updaterevision.c || die
	eapply_user
	cmake-utils_src_prepare
}

src_configure() {
	local mycmakeargs=()
	use gtk || mycmakeargs+="-DNO_GTK=ON"
	use openal || mycmakeargs+="-DNO_OPENAL=ON"
	append-cxxflags "-O3"
	cmake-utils_src_configure
}

pkg_postinst() {
	gnome2_icon_cache_update
	ewarn "Copy or link wad files into ~/.config/gzdoom"
	ewarn "or set the \$DOOMWADDIR environment variable"
}

pkg_postrm() {
	gnome2_icon_cache_update
}
