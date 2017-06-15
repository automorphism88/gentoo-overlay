# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

DESCRIPTION="A black theme set for GTK+"
HOMEPAGE="https://github.com/automorphism88/cloak-theme/"
LICENSE="GPL-3"
SLOT=0

IUSE="cinnamon firefox gnome-shell +gtk2 +gtk3 mate openbox xfce xfdashboard"

RDEPEND="gtk2? ( >=x11-themes/gnome-themes-standard-3.20
	x11-themes/gtk-engines-murrine )
	gtk3? ( >=x11-libs/gtk+-3.20:3 )
	x11-libs/gdk-pixbuf"
DEPEND="${RDEPEND}"

if [[ ${PV} == 99999999 ]] ; then
	KEYWORDS=""
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/automorphism88/cloak-theme"
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/automorphism88/cloak-theme/archive/${PV}.tar.gz -> ${P}.tar.gz"
fi

src_install() {
	dodir /usr/share/themes/Cloak
	cd "${S}/Cloak-3.20" || die
	cp index.theme "${D}/usr/share/themes/Cloak" || die

	use cinnamon && { cp -R cinnamon "${D}/usr/share/themes/Cloak" || die; }
	use firefox && { cp -R Firefox "${D}/usr/share/themes/Cloak" || die; }
	use gnome-shell && { cp -R gnome-shell gnome-shell-GDM "${D}/usr/share/themes/Cloak" || die; }
	use gtk2 && { cp -R gtk-2.0 "${D}/usr/share/themes/Cloak" || die; }
	use gtk3 && { cp -R gtk-3.0 "${D}/usr/share/themes/Cloak" || die; }
	use mate && { cp -R metacity-1 "${D}/usr/share/themes/Cloak" || die; }
	use openbox && { cp -R openbox-3 "${D}/usr/share/themes/Cloak" || die; }
	use xfce && { cp -R xfwm4 "${D}/usr/share/themes/Cloak" || die; }
	use xfdashboard && { cp -R ../xfdashboard-cloak-3.20/xfdashboard-1.0 "${D}/usr/share/themes/Cloak" || die; }
	dodoc README
}

pkg_postinst() {
	if use firefox ; then
		elog "To use Firefox theme, create a symlink from"
		elog "'/usr/share/themes/Cloak/Firefox/chrome'"
		elog "into your Firefox profile directory"
		elog "(e.g. '\$HOME/.mozilla/firefox/foo.default')"
		elog "Cloak must be selected as GTK theme to use Firefox theme."
	fi
}
