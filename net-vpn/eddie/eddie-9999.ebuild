# Copyright 1999-2019 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
SLOT=0
inherit cmake-utils desktop mono

DESCRIPTION="AirVPN client"
HOMEPAGE="https://eddie.website"
LICENSE="GPL-3"
IUSE="+policykit X"

if [[ "${PV}" == 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI=https://github.com/AirVPN/Eddie
	KEYWORDS=
elif [[ "${PV}" == 2.18.5 ]] ; then
	inherit git-r3
	EGIT_REPO_URI=https://github.com/AirVPN/Eddie
	EGIT_COMMIT=899f57d75eb8b9977f7710b86b421cff991d2070
	KEYWORDS="~amd64"
else
	KEYWORDS="~amd64"
	SRC_URI="https://github.com/AirVPN/Eddie/archive/v${PV}.tar.gz -> ${P}.tar.gz"
fi

# CMake is only used to compile the GUI, if USE=X is enabled
CMAKE_USE_DIR="${S}/src/UI.GTK.Linux.Tray"
CMAKE_BUILD_TYPE=Release

DEPEND="dev-lang/mono
	dev-util/desktop-file-utils
	net-misc/curl
	net-misc/openssh
	net-misc/stunnel
	net-vpn/openvpn
	X? ( dev-libs/libappindicator:2
		 x11-libs/gtk+:2 )"

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
	cmake-utils_src_prepare
}

src_configure() {
	use X && cmake-utils_src_configure
}

src_compile() {
	xbuild /verbosity:minimal /p:Configuration="Release" /p:Platform="x64" \
		src/eddie2.linux.sln || die
	src/eddie.linux.postbuild.sh \
		"src/App.Forms.Linux/bin/x64/Release/" \
		cli x64 Release || die
	if use X ; then
		cmake-utils_src_compile
		src/eddie.linux.postbuild.sh \
			"src/App.Forms.Linux/bin/x64/Release/" \
			ui x64 Release || die
	fi
}

src_install() {
	dobin "${FILESDIR}/eddie-cli"
	use X && dobin "${FILESDIR}/eddie-ui"
	insinto /usr/libexec/eddie
	exeinto /usr/libexec/eddie
	newexe src/App.CLI.Linux/bin/x64/Release/App.CLI.Linux.exe eddie-cli.exe
	doexe src/App.Forms.Linux/bin/x64/Release/eddie-cli-elevated
	doins src/App.Forms.Linux/bin/x64/Release/Lib.Core.dll
	doins src/App.Forms.Linux/bin/x64/Release/Lib.Forms.dll
	doins src/App.Forms.Linux/bin/x64/Release/Lib.Platform.Linux.dll
	doins src/Lib.Platform.Linux.Native/bin/libLib.Platform.Linux.Native.so
	if use X ; then
		newexe src/App.Forms.Linux/bin/x64/Release/App.Forms.Linux.exe \
			eddie-ui.exe
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
	if use policykit ; then
		insinto /usr/share/polkit-1/actions
		doins "${FILESDIR}/org.airvpn.eddie.cli.elevated.policy"
	fi
}
