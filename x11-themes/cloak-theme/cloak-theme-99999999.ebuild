# Copyright 1999-2018 Gentoo Foundation
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
	insinto /usr/share/themes/Cloak
	cd "${S}/Cloak-3.20" || die
	doins index.theme
	use cinnamon && doins -r cinnamon
	use firefox && doins -r Firefox
	use gnome-shell && doins -r gnome-shell gnome-shell-GDM
	use gtk2 && doins -r gtk-2.0
	use gtk3 && doins -r gtk-3.0
	use mate && doins -r metacity-1
	use openbox && doins -r openbox-3
	use xfce && doins -r xfwm4
	use xfdashboard && doins -r ../xfdashboard-cloak-3.20/xfdashboard-1.0
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
