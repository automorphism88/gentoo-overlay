# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
inherit cmake-utils desktop flag-o-matic gnome2-utils xdg-utils

DESCRIPTION="A 3D-accelerated Doom source port based on ZDoom code"
HOMEPAGE="https://zdoom.org/"
LICENSE="GPL-3 LGPL-2.1 BSD MPL-2.0"
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
	virtual/opengl
	!games-fps/qzdoom"
DEPEND="${RDEPEND}
	x86? ( >=dev-lang/nasm-0.98.39 )"

src_prepare() {
	sed -i "s:/usr/local/share/:/usr/share/:" src/posix/i_system.h || die
	sed -i "s/<unknown version>/${PV}/" \
		tools/updaterevision/updaterevision.c || die
	eapply_user
	cmake-utils_src_prepare
}

src_configure() {
	local -a mycmakeargs
	mycmakeargs=()
	use gtk || mycmakeargs+="-DNO_GTK=ON"
	use openal || mycmakeargs+="-DNO_OPENAL=ON"
	append-cxxflags "-O3"
	cmake-utils_src_configure
}

src_install() {
	cmake-utils_src_install
	rm -frv "${ED%/}/usr/share/doc/gzdoom/licenses" || die
	newicon "${S}/src/posix/zdoom.xpm" gzdoom.xpm
	domenu "${FILESDIR}/gzdoom.desktop"
}

pkg_postinst() {
	gnome2_icon_cache_update
	xdg_desktop_database_update
	ewarn "Copy or link wad files into ~/.config/gzdoom"
	ewarn "or set the \$DOOMWADDIR environment variable"
}

pkg_postrm() {
	gnome2_icon_cache_update
	xdg_desktop_database_update
}
