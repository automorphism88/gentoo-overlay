# Copyright 1999-2020 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# dotnet.eclass broken with EAPI=7, inherits versionator
# Gentoo bug #701186
EAPI=6
SLOT=0

inherit cmake-utils desktop dotnet git-r3 mono-env toolchain-funcs xdg
FRAMEWORK="4.5"

DESCRIPTION="AirVPN client"
HOMEPAGE="https://eddie.website"
LICENSE="GPL-3"
IUSE="X"

EGIT_REPO_URI="https://github.com/AirVPN/Eddie"
SRC_URI=

case "${PV}" in
	9999)
		KEYWORDS=
		;;
	2.18.7)
		EGIT_COMMIT=0d75935ceeffebdc24ebe03b41c1274a286aea99
		KEYWORDS="~amd64 ~x86"
		;;
	*)
		die "Unknown version"
		;;
esac

DEPEND="net-misc/curl
	net-vpn/openvpn
	X? ( dev-libs/libappindicator:2
		 x11-libs/gtk+:2 )"
RDEPEND="acct-group/eddie
	${DEPEND}"

pkg_setup() {
	case "$ARCH" in
		amd64) EDDIE_ARCH=x64 ;;
		x86) EDDIE_ARCH=x86 ;;
		*) die "Unsupported ARCH=${ARCH}" ;;
	esac
	CMAKE_USE_DIR="${S}/src/UI.GTK.Linux.Tray"
	# Gentoo bug #659422
	mono-env_pkg_setup
	dotnet_pkg_setup
}

src_prepare() {
	# xdg_src_prepare, without running the default src_prepare twice
	xdg_environment_reset
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
	# This .sln builds both the GUI and CLI .exe and .dll files, regardless of
	# whether USE=X is enabled. We install the GUI only if USE=X is enabled
	exbuild /p:Platform="${EDDIE_ARCH}" src/eddie2.linux.sln
	# Instead of src/Lib.Platform.Linux.Native/build.sh
	$(tc-getCXX) \
		-o libLib.Platform.Linux.Native.so \
		src/Lib.Platform.Linux.Native/src/api.cpp \
		${CXXFLAGS} ${CPPFLAGS} ${LDFLAGS} \
		-shared -fPIC -Wall -std=c++11 -DRelease || die
	# Instead of src/App.CLI.Linux.Elevated/build.sh
	$(tc-getCXX) \
		-o eddie-cli-elevated \
		src/App.CLI.Linux.Elevated/src/main.cpp \
		src/App.CLI.Linux.Elevated/src/impl.cpp \
		src/App.CLI.Linux.Elevated/src/loadmod.c \
		src/App.CLI.Common.Elevated.C/iposix.cpp \
		src/App.CLI.Common.Elevated.C/ibase.cpp \
		src/App.CLI.Common.Elevated.C/sha256.c \
		${CXXFLAGS} ${CPPFLAGS} ${LDFLAGS} \
		-Wall -std=c++11 -pthread -lpthread -llzma -DRelease || die
	# build eddie-tray
	use X && cmake-utils_src_compile
}

src_install() {
	dobin "${FILESDIR}/eddie-cli"
	if use X ; then
		dobin "${FILESDIR}/eddie-ui"
		newicon common/icon.png eddie-ui.png
		make_desktop_entry \
			/usr/bin/eddie-ui \
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
	insinto /usr/share/polkit-1/rules
	doins "${FILESDIR}/org.airvpn.eddie.cli.elevated.rules"
}

pkg_postinst() {
	xdg_pkg_postinst
	elog "net-misc/openssh required for SSH tunnels"
	elog "net-misc/stunnel required for SSL tunnels"
}
