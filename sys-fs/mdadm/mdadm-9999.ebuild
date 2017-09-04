# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=5
inherit eutils flag-o-matic multilib systemd toolchain-funcs udev git-r3

DESCRIPTION="A useful tool for running RAID systems - it can be used as a replacement for the raidtools"
HOMEPAGE="http://neil.brown.name/blog/mdadm"

LICENSE="GPL-2"
SLOT="0"
DEB_PR="4"
SRC_URI="mirror://debian/pool/main/m/mdadm/${PN}_3.4-${DEB_PR}.debian.tar.xz"
EGIT_REPO_URI="https://kernel.googlesource.com/pub/scm/utils/mdadm/mdadm"
KEYWORDS=""
IUSE="static"

DEPEND="virtual/pkgconfig
	app-arch/xz-utils"
RDEPEND=">=sys-apps/util-linux-2.16"

# The tests edit values in /proc and run tests on software raid devices.
# Thus, they shouldn't be run on systems with active software RAID devices.
RESTRICT="test"

src_prepare() {
	unpack "${PN}_3.4-${DEB_PR}.debian.tar.xz"
	epatch "${FILESDIR}"/${PN}-3.4-sysmacros.patch #580188
	epatch "${FILESDIR}"/install-raid6check.patch
}

mdadm_emake() {
	# We should probably make corosync & libdlm into USE flags. #573782
	emake \
		PKG_CONFIG="$(tc-getPKG_CONFIG)" \
		CC="$(tc-getCC)" \
		CWFLAGS="-Wall" \
		CXFLAGS="${CFLAGS}" \
		UDEVDIR="$(get_udevdir)" \
		SYSTEMD_DIR="$(systemd_get_unitdir)" \
		COROSYNC="-DNO_COROSYNC" \
		DLM="-DNO_DLM" \
		"$@"
}

src_compile() {
	use static && append-ldflags -static
	#mdadm_emake all mdassemble
	# The make target 'mdassemble' appears to no longer exist
	mdadm_emake all
}

src_test() {
	mdadm_emake test

	sh ./test || die
}

src_install() {
	mdadm_emake DESTDIR="${D}" install install-systemd
	into /
	#dosbin mdassemble
	#dodoc ChangeLog INSTALL TODO README* ANNOUNCE-4.0
	dodoc ChangeLog INSTALL TODO README*

	insinto /etc
	newins mdadm.conf-example mdadm.conf
	newinitd "${FILESDIR}"/mdadm.rc mdadm
	newconfd "${FILESDIR}"/mdadm.confd mdadm
	newinitd "${FILESDIR}"/mdraid.rc mdraid
	newconfd "${FILESDIR}"/mdraid.confd mdraid

	# From the Debian patchset
	into /usr
	dodoc "${S}"/debian/README.checkarray
	dosbin "${S}"/debian/checkarray
	insinto /etc/default
	newins "${FILESDIR}"/etc-default-mdadm mdadm

	exeinto /etc/cron.weekly
	newexe "${FILESDIR}"/mdadm.weekly mdadm
}

pkg_postinst() {
	if ! systemd_is_booted; then
		if [[ -z ${REPLACING_VERSIONS} ]] ; then
			# Only inform people the first time they install.
			elog "If you're not relying on kernel auto-detect of your RAID"
			elog "devices, you need to add 'mdraid' to your 'boot' runlevel:"
			elog "	rc-update add mdraid boot"
		fi
	fi
}
