# Copyright 2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7

DESCRIPTION="Symlinks and syncs user specified dirs to RAM"
HOMEPAGE="https://wiki.archlinux.org/index.php/Anything-sync-daemon"

if [[ "${PV}" = 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/graysky2/anything-sync-daemon"
	SRC_URI=
	KEYWORDS=
else
	SRC_URI="http://repo-ck.com/source/${PN}/${P}.tar.xz"
	KEYWORDS="amd64 x86"
fi

LICENSE="MIT"
SLOT="0"
IUSE="systemd"

RDEPEND="
	net-misc/rsync[xattr]
	virtual/cron
	systemd? ( sys-apps/systemd )
"

src_prepare(){
	eapply "${FILESDIR}/asd-openrc-support.patch"
	eapply_user
}

src_compile(){
	emake DESTDIR="${D}"
}

src_install() {
	use systemd && emake DESTDIR="${D}" install-systemd-all
	use !systemd && emake DESTDIR="${D}" install-upstart-all
	find "${D}/usr/share/man" -type f -name '*.gz' -exec gunzip '{}' \; || die
	find "${D}/usr/share/man" -type l -name '*.gz' -delete || die
	dosym asd.1 /usr/share/man/man1/anything-sync-daemon.1
}
