# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=5

inherit cmake-utils versionator

DESCRIPTION="A graphical grub2 settings manager"
HOMEPAGE="https://launchpad.net/grub-customizer"
SRC_URI="https://launchpad.net/${PN}/$(get_version_component_range 1-2)/${PV}/+download/${PN}_${PV}.tar.gz"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64"

DEPEND="dev-cpp/gtkmm:3.0
		dev-libs/openssl
		x11-themes/hicolor-icon-theme
		sys-boot/grub:2
		app-arch/libarchive"

RDEPEND="${DEPEND}"

src_configure() {
	CMAKE_BUILD_TYPE="release"
	cmake-utils_src_configure
}
