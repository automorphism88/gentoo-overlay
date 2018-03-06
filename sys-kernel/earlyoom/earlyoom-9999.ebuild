# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
SLOT=0
inherit systemd
DESCRIPTION="Daemon to kill processes before the kernel OOM killer"
HOMEPAGE="https://github.com/rfjakob/earlyoom"
LICENSE="MIT"

if [[ "$PV" = 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/rfjakob/earlyoom.git"
	SRC_URI=""
	KEYWORDS=""
else
	SRC_URI="https://github.com/rfjakob/earlyoom/archive/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

src_prepare() {
	sed -i 's#:SYSCONFDIR:/default#:SYSCONFDIR:/conf.d#' \
		"${PN}.service.in" || die
	eapply_user
}

src_compile() {
	emake DESTDIR="${D}" PREFIX="/usr" "${PN}" "${PN}.service"
}

src_install() {
	emake DESTDIR="${D}" PREFIX="/usr" install-bin
	newinitd "${FILESDIR}/${PN}.openrc" "${PN}"
	newconfd "${PN}.default" "${PN}"
	systemd_dounit "${PN}.service"
	doman "${PN}.1"
	einstalldocs
}
