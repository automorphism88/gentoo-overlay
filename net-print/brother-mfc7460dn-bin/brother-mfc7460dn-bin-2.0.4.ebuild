# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI="6"
inherit rpm linux-info multilib

DESCRIPTION="Brother MFC-7460DN printer driver"
HOMEPAGE="http://support.brother.com"

SRC_URI="http://download.brother.com/welcome/dlf006257/mfc7460dnlpr-2.1.0-1.i386.rpm
http://download.brother.com/welcome/dlf006259/cupswrapperMFC7460DN-2.0.4-2.i386.rpm"

LICENSE="brother-eula GPL-2"
SLOT="0"
KEYWORDS="amd64 x86"

RESTRICT="strip"
RDEPEND="net-print/cups"
S="${WORKDIR}"

pkg_setup() {
	CONFIG_CHECK=""
	if use amd64; then
		CONFIG_CHECK="${CONFIG_CHECK} ~IA32_EMULATION"
		if ! has_multilib_profile; then
			die "This package CANNOT be installed on pure 64-bit system. You need multilib enabled."
		fi
	fi
	linux-info_pkg_setup
}

src_unpack() {
	rpm_unpack ${A}
}

src_prepare() {
	default
	sed -i 's:/usr/local/Brother/Printer:/opt/brother/Printers:' "${S}/usr/local/Brother/Printer/MFC7460DN/lpd/filterMFC7460DN" || die
	sed -e '/^\*PPD-Adobe:/,/^ENDOFPPDFILE/!d' -e '/^ENDOFPPDFILE/d' "${S}/usr/local/Brother/Printer/MFC7460DN/cupswrapper/cupswrapperMFC7460DN-2.0.4" > "${T}/brother-MFC7460DN.ppd" || die
	sed -e '/^cat <<!ENDOFWFILTER!/,/^!ENDOFWFILTER!/!d' -e '/!ENDOFWFILTER!/d' -e 's:/usr/local/Brother/Printer:/opt/brother/Printers:' -e 's/\\//g' "${S}/usr/local/Brother/Printer/MFC7460DN/cupswrapper/cupswrapperMFC7460DN-2.0.4" > "${T}/brlpdwrapperMFC7460DN" || die
}

src_install() {
	keepdir /var/spool/lpd/MFC7460DN
	dodir /opt/brother/Printers
	cp -a "${S}/usr/local/Brother/Printer/MFC7460DN" "${ED%/}/opt/brother/Printers" || die
	insinto /opt/brother/Printers/MFC7460DN/cupswrapper
	insopts -m644
	doins "${T}/brother-MFC7460DN.ppd"
	insopts -m755
	doins "${T}/brlpdwrapperMFC7460DN"
	dosym ../../../../opt/brother/Printers/MFC7460DN/cupswrapper/brother-MFC7460DN.ppd /usr/share/cups/model/brother-MFC7460DN.ppd
	dosym ../../../../opt/brother/Printers/MFC7460DN/cupswrapper/brlpdwrapperMFC7460DN /usr/libexec/cups/filter/brlpdwrapperMFC7460DN
}