# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

DESCRIPTION="A black theme set for GTK"
HOMEPAGE="https://github.com/killhellokitty/Cloak-3.20/"
LICENSE="GPL-3"
SLOT=0

IUSE="cinnamon gnome mate openbox xfce xfdashboard"

RDEPEND=">=x11-themes/gnome-themes-standard-3.20
	x11-themes/gtk-engines-murrine
	x11-libs/gdk-pixbuf"
DEPEND="${RDEPEND}"

if [[ ${PV} == 99999999 ]] ; then
	KEYWORDS=""
	inherit git-r3
	SRC_URI=""
	EGIT_REPO_URI="https://github.com/automorphism88/Cloak-3.20"
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/automorphism88/Cloak-3.20/archive/${PV}.tar.gz -> ${P}.tar.gz"
	S="${WORKDIR}/Cloak-3.20-${PV}"
fi

src_install() {
	dodir /usr/share/themes/Cloak-3.20
	cd "${S}/Cloak-3.20" || die
	cp -R index.theme gtk-2.0 gtk-3.0 "${D}/usr/share/themes/Cloak-3.20" || die

	use cinnamon && { cp -R cinnamon "${D}/usr/share/themes/Cloak-3.20" || die; }
	use gnome && { cp -R gnome-shell gnome-shell-GDM "${D}/usr/share/themes/Cloak-3.20" || die; }
	use mate && { cp -R metacity-1 "${D}/usr/share/themes/Cloak-3.20" || die; }
	use openbox && { cp -R openbox-3 "${D}/usr/share/themes/Cloak-3.20" || die; }
	use xfce && { cp -R xfwm4 "${D}/usr/share/themes/Cloak-3.20" || die; }
	use xfdashboard && { cp -R ../xfdashboard-cloak-3.20/xfdashboard-1.0 "${D}/usr/share/themes/Cloak-3.20" || die; }
}
