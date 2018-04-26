# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI="6"
FRAMEWORK="4.6"
inherit dotnet user

DESCRIPTION="Emby is a server designed to stream media to a variety of devices"
HOMEPAGE="http://emby.media/"
KEYWORDS="~amd64 ~x86"
IUSE="+unlocked"
SRC_URI="
	https://github.com/MediaBrowser/Emby/archive/${PV}.tar.gz -> ${P}.tar.gz
	unlocked? ( https://github.com/nvllsvm/emby-unlocked/archive/${PV}.tar.gz -> ${P}-unlocked.tar.gz )
"
SLOT="0"
LICENSE="GPL-2"

RDEPEND=">=dev-lang/mono-4.6.0
	>=media-video/ffmpeg-2[vpx]
	media-gfx/imagemagick[jpeg,jpeg2k,webp,png]
	>=dev-db/sqlite-3.0.0
	dev-dotnet/referenceassemblies-pcl
	app-misc/ca-certificates"
DEPEND="${RDEPEND}"

S="${WORKDIR}/Emby-${PV}"
INSTALL_DIR="/opt/emby-server"
DATA_DIR="/var/lib/emby-server"
STARTUP_LOG="/var/log/emby-server_start.log"
INIT_SCRIPT="${ROOT}/etc/init.d/emby-server"

do_unlocked() (
	local UNLOCK_S
	UNLOCK_S="${WORKDIR}/emby-unlocked-${PV}"
	cd "${S}/Emby.Server.Implementations/Security"
	epatch "${UNLOCK_S}/patches/PluginSecurityManager.cs.patch"
	cd "${S}/MediaBrowser.WebDashboard/dashboard-ui/bower_components/emby-apiclient"
	[[ -f connectionmanager.js ]] || die "connectionmanager.js not found"
	cp -v "${UNLOCK_S}/replacements/connectionmanager.js" \
		connectionmanager.js || die
)

my_exbuild() {
	elog "xbuild ""$@"" || die"
	xbuild "$@" || die
}

src_prepare() {
	use unlocked && do_unlocked
	eapply_user
}

src_compile() {
	my_exbuild \
		/p:Configuration="Release Mono" \
		/p:Platform="Any CPU" \
		MediaBrowser.sln
}

src_install() {
	newinitd "${FILESDIR}"/emby-server.init ${PN}
	newconfd "${FILESDIR}"/emby-server.conf ${PN}
	insinto "${INSTALL_DIR}"
	doins -r "${S}"/MediaBrowser.Server.Mono/bin/Release/*
}

pkg_preinst() {
	enewgroup emby
	enewuser emby -1 /bin/bash ${INSTALL_DIR} "emby"
}

pkg_prerm() {
	if [ -e "${INIT_SCRIPT}" ]; then
		einfo "Stopping running instances of emby-server"
		${INIT_SCRIPT} stop
	fi
}
