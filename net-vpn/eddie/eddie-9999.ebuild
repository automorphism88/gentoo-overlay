# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# dotnet.eclass broken with EAPI=7, inherits versionator
EAPI=6
SLOT=0

inherit cmake-utils desktop dotnet toolchain-funcs
FRAMEWORK="4.5"

DESCRIPTION="AirVPN client"
HOMEPAGE="https://eddie.website"
LICENSE="GPL-3"
IUSE="X"

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/AirVPN/Eddie"
	SRC_URI=
	KEYWORDS=
elif [[ "${PV}" == 2.18.5 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/AirVPN/Eddie"
	SRC_URI=
	EGIT_COMMIT=899f57d75eb8b9977f7710b86b421cff991d2070
	KEYWORDS="~amd64 ~x86"
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/AirVPN/Eddie/archive/v${PV}.tar.gz -> ${P}.tar.gz"
fi

DEPEND="net-misc/curl
	net-misc/openssh
	net-misc/stunnel
	net-vpn/openvpn
	X? ( dev-libs/libappindicator:2
		 x11-libs/gtk+:2 )"

pkg_setup() {
	case "$ARCH" in
		amd64) EDDIE_ARCH=x64 ;;
		x86) EDDIE_ARCH=x86 ;;
		*) die "Unsupported ARCH=${ARCH}" ;;
	esac
	CMAKE_USE_DIR="${S}/src/UI.GTK.Linux.Tray"
	dotnet_pkg_setup
}

src_prepare() {
	# Even though CMake is only used if USE=X is enabled, we have to call
	# cmake-utils_src_prepare from src_prepare or portage will throw an error
	cmake-utils_src_prepare
	# build eddie_tray with dynamically linked libgcc
	sed -ri 's/-static-lib(gcc|stdc\+\+)//g' \
		src/UI.GTK.Linux.Tray/CMakeLists.txt || die
}

src_configure() {
	use X && cmake-utils_src_configure
}

# Upstream build scripts have so many flaws that it's easier to invoke xbuild
# and cmake and compile the remaining two files we need manually
src_compile() {
	exbuild /p:Platform="${EDDIE_ARCH}" src/eddie2.linux.sln
	# Instead of src/Lib.Platform.Linux.Native/build.sh
	$(tc-getCXX) \
		-o libLib.Platform.Linux.Native.so \
		src/Lib.Platform.Linux.Native/src/api.cpp \
		${CXXFLAGS} ${CPPFLAGS} ${LDFLAGS} \
		-shared -fPIC -Wall -std=c++11 -DRelease
	# Instead of src/App.CLI.Linux.Elevated/build.sh
	$(tc-getCXX) \
		-o eddie-cli-elevated \
		src/App.CLI.Linux.Elevated/src/main.cpp \
		src/App.CLI.Linux.Elevated/src/impl.cpp \
		src/App.CLI.Common.Elevated.C/iposix.cpp \
		src/App.CLI.Common.Elevated.C/ibase.cpp \
		src/App.CLI.Common.Elevated.C/sha256.cpp \
		${CXXFLAGS} ${CPPFLAGS} ${LDFLAGS} \
		-Wall -std=c++11 -pthread -lpthread -DRelease
	# build eddie-tray
	use X && cmake-utils_src_compile
}

src_install() {
	dobin "${FILESDIR}/eddie-cli"
	if use X ; then
		dobin "${FILESDIR}/eddie-ui"
		newicon common/icon.png eddie-ui.png
		make_desktop_entry /usr/bin/eddie-ui \
			"Eddie AirVPN Client" \
			eddie-ui \
			Network
	fi

	insinto /usr/libexec/eddie
	exeinto /usr/libexec/eddie
	newexe \
		"src/App.CLI.Linux/bin/${EDDIE_ARCH}/Release/App.CLI.Linux.exe" \
		eddie-cli.exe
	use X && newexe \
		"src/App.Forms.Linux/bin/${EDDIE_ARCH}/Release/App.Forms.Linux.exe" \
		eddie-ui.exe
	doexe eddie-cli-elevated
	use X && newexe "${BUILD_DIR}/eddie_tray" eddie-tray
	doins \
		libLib.Platform.Linux.Native.so \
		"src/App.Forms.Linux/bin/${EDDIE_ARCH}/Release/Lib.Core.dll" \
		"src/App.Forms.Linux/bin/${EDDIE_ARCH}/Release/Lib.Platform.Linux.dll"
	use X && doins \
		"src/App.Forms.Linux/bin/${EDDIE_ARCH}/Release/Lib.Forms.dll"

	insinto /usr/share/eddie
	doins -r \
		common/lang \
		common/providers \
		common/cacert.pem \
		common/iso-3166.json
	use X && doins \
		common/icon.png \
		common/icon_gray.png \
		common/tray.png \
		common/tray_gray.png

	insinto /usr/share/polkit-1/actions
	doins "${FILESDIR}/org.airvpn.eddie.cli.elevated.policy"
}
