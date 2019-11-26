# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# dotnet.eclass broken with EAPI=7, inherits versionator
EAPI=6
SLOT=0

inherit cmake-utils desktop dotnet
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
		 dev-util/desktop-file-utils
		 x11-libs/gtk+:2 )"

pkg_setup() {
	case "$ARCH" in
		amd64) MY_ARCH=x64 ;;
		x86) MY_ARCH=x86 ;;
		*) die "Unsupported ARCH=${ARCH}" ;;
	esac
	dotnet_pkg_setup
}

src_prepare() {
	local i
	# build dynamic eddie-cli-elevated
	sed -ri -e 's/-static//g' -e 's/-Wl,--(no-)?whole-archive//g' \
		src/App.CLI.Linux.Elevated/build.sh || die
	# build eddie_tray with dynamically linked libgcc
	sed -i -e '/target_link_libraries/s/-static-libgcc //' \
		-e '/target_link_libraries/s/-static-libstdc++ //' \
		src/UI.GTK.Linux.Tray/CMakeLists.txt || die
	# don't pre-strip executables, let portage do it
	for i in \
		src/App.CLI.Linux.Elevated/build.sh \
		src/Lib.Platform.Linux.Native/build.sh
	do
		sed -i -e '/^strip /d' -e 's/^set -e/&x/' "${i}" || die
	done
	# these scripts need to be executable during build
	chmod +x \
		src/eddie.linux.postbuild.sh \
		src/App.CLI.Linux.Elevated/build.sh \
		src/Lib.Platform.Linux.Native/build.sh || die
	# Even though CMake is only used if USE=X is enabled, we have to call
	# cmake-utils_src_prepare from src_prepare or portage will throw an error
	CMAKE_USE_DIR="${S}/src/UI.GTK.Linux.Tray"
	CMAKE_BUILD_TYPE=Release
	cmake-utils_src_prepare
}

src_configure() {
	use X && cmake-utils_src_configure
}

src_compile() {
	exbuild src/eddie2.linux.sln \
		/p:Configuration="${CMAKE_BUILD_TYPE}" \
		/p:Platform="${MY_ARCH}"
	src/eddie.linux.postbuild.sh \
		"src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/" \
		cli "${MY_ARCH}" "${CMAKE_BUILD_TYPE}" || die
	if use X ; then
		cmake-utils_src_compile
		src/eddie.linux.postbuild.sh \
			"src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/" \
			ui "${MY_ARCH}" "${CMAKE_BUILD_TYPE}" || die
	fi
}

src_install() {
	dobin "${FILESDIR}/eddie-cli"
	use X && dobin "${FILESDIR}/eddie-ui"
	insinto /usr/libexec/eddie
	exeinto /usr/libexec/eddie
	newexe "src/App.CLI.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/App.CLI.Linux.exe" eddie-cli.exe
	doexe "src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/eddie-cli-elevated"
	doins "src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/Lib.Core.dll"
	doins "src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/Lib.Forms.dll"
	doins "src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/Lib.Platform.Linux.dll"
	doins src/Lib.Platform.Linux.Native/bin/libLib.Platform.Linux.Native.so
	if use X ; then
		newexe "src/App.Forms.Linux/bin/${MY_ARCH}/${CMAKE_BUILD_TYPE}/App.Forms.Linux.exe" eddie-ui.exe
		newexe "${BUILD_DIR}/eddie_tray" eddie-tray
		doicon repository/linux_arch/bundle/eddie-ui/usr/share/pixmaps/eddie-ui.png
		make_desktop_entry /usr/bin/eddie-ui \
			"Eddie AirVPN Client" \
			eddie-ui \
			Network
	fi
	insinto /usr/share/eddie
	doins common/cacert.pem
	doins common/icon.png
	doins common/icon_gray.png
	dosym "${EPREFIX}/usr/share/eddie/icon.png" \
		"${EPREFIX}/usr/share/eddie/tray.png"
	dosym "${EPREFIX}/usr/share/eddie/icon_gray.png" \
		"${EPREFIX}/usr/share/eddie/tray_gray.png"
	doins common/iso-3166.json
	# In Arch PKGBUILD, but this directory doesn't seem to exist
	#doins -r common/webui
	insinto /usr/share/eddie/lang
	doins common/lang/inv.json
	insinto /usr/share/polkit-1/actions
	doins "${FILESDIR}/org.airvpn.eddie.cli.elevated.policy"
}
