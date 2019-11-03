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

DEPEND="app-admin/sudo
	dev-lang/mono
	dev-util/desktop-file-utils
	net-misc/curl
	net-misc/openssh
	net-misc/stunnel
	net-vpn/openvpn
	X? ( dev-libs/libappindicator:2 )"

src_prepare() {
	eapply_user
	local i
	# fix paths in wrapper scripts
	for i in \
		ui/usr/bin/eddie-ui \
		ui/usr/share/polkit-1/actions/org.airvpn.eddie.ui.elevated.policy \
		cli/usr/bin/eddie-cli \
		cli/usr/share/polkit-1/actions/org.airvpn.eddie.cli.elevated.policy
	do
		sed -ri 's:(/usr/lib/eddie)-(cl|u)i:\1:g' \
			"repository/linux_arch/bundle/eddie-${i}" || die
	done
	# don't pre-strip executables, let portage do it
	for i in \
		src/App.CLI.Linux.Elevated/build.sh \
		src/Lib.Platform.Linux.Native/build.sh
	do
		sed -i '/^strip /d' "${i}" || die
	done
	# these scripts need to be executable during build
	chmod +x \
		src/eddie.linux.postbuild.sh \
		src/App.CLI.Linux.Elevated/build.sh \
		src/Lib.Platform.Linux.Native/build.sh || die
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
	dobin repository/linux_arch/bundle/eddie-cli/usr/bin/eddie-cli
	use X && dobin repository/linux_arch/bundle/eddie-ui/usr/bin/eddie-ui
	insinto /usr/lib/eddie
	exeinto /usr/lib/eddie
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
		doins repository/linux_arch/bundle/eddie-cli/usr/share/polkit-1/actions/org.airvpn.eddie.cli.elevated.policy
		use X && doins repository/linux_arch/bundle/eddie-ui/usr/share/polkit-1/actions/org.airvpn.eddie.ui.elevated.policy
	fi
}
