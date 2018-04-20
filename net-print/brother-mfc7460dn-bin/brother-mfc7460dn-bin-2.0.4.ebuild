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

DEPEND="app-editors/vim-core"
RDEPEND="net-print/cups"

# Unsure if necessary - copied from brother-overlay
RESTRICT="strip"

QA_PREBUILT="opt/brother/Printers/MFC7460DN/inf/brprintconflsr3
	opt/brother/Printers/MFC7460DN/lpd/rawtobr3"
S="${WORKDIR}/usr/local/Brother/Printer/MFC7460DN"

fix_path_in_binary() {
	local file in_hex out_hex out_str str strings tmp_file IFS
	IFS=$'\n'
	for file in "$@" ; do
		elog "Fixing paths in ${file}..."
		strings="$(strings "${file}" | grep /usr/local/Brother/Printer | sort -u)"
		for str in ${strings} ; do
			tmp_file="${T}/fix_path_in_binary.tmp"
			in_hex="$(printf '%s' "${str}" | xxd -g 0 -u -ps -c 256)00"
			out_str="$(printf '%s' "${str}" | sed -f "${FILESDIR}/fix-path.sed")"
			out_hex="$(printf '%s' "${out_str}" | xxd -g 0 -u -ps -c 256)00"
			while ((${#out_hex} < ${#in_hex})) ; do
				out_hex="${out_hex}00"
			done
			hexdump -ve '1/1 "%.2X"' "${file}" |
				sed "s/${in_hex}/${out_hex}/g" |
				xxd -r -p > "${tmp_file}" || die
			chmod --reference "${file}" "${tmp_file}" || die
			mv "${tmp_file}" "${file}" || die
		done
		if strings "${file}" | grep /usr/local/Brother/Printer > /dev/null ; then
			die "Failed to fix paths in ${file}"
		else
			elog "Fixed paths in ${file}"
		fi
	done
}

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
	sed -i -f "${FILESDIR}/fix-path.sed" "${S}/cupswrapper/cupswrapperMFC7460DN-${PV}" || die
	sed -i -f "${FILESDIR}/fix-path.sed" "${S}/inf/setupPrintcap2" || die
	sed -i -f "${FILESDIR}/fix-path.sed" "${S}/lpd/filterMFC7460DN" || die
	fix_path_in_binary "${S}/cupswrapper/brcupsconfig4"
	fix_path_in_binary "${S}/inf/brprintconflsr3"
	sed -f "${FILESDIR}/extract-cups-ppd.sed" "${S}/cupswrapper/cupswrapperMFC7460DN-${PV}" > "${T}/brother-MFC7460DN.ppd" || die
	sed -f "${FILESDIR}/extract-cups-filter.sed" "${S}/cupswrapper/cupswrapperMFC7460DN-${PV}" > "${T}/brlpdwrapperMFC7460DN" || die
}

src_install() {
	keepdir /var/spool/lpd/MFC7460DN
	dodir /opt/brother/Printers
	cp -a "${S}" "${ED%/}/opt/brother/Printers" || die
	fowners lp:lp /opt/brother/Printers/MFC7460DN/inf/brMFC7460DNrc
	fperms 600 /opt/brother/Printers/MFC7460DN/inf/brMFC7460DNrc
	insinto /opt/brother/Printers/MFC7460DN/cupswrapper
	doins "${T}/brother-MFC7460DN.ppd"
	exeinto /opt/brother/Printers/MFC7460DN/cupswrapper
	doexe "${T}/brlpdwrapperMFC7460DN"
	dosym ../../../../opt/brother/Printers/MFC7460DN/cupswrapper/brother-MFC7460DN.ppd /usr/share/cups/model/brother-MFC7460DN.ppd
	dosym ../../../../opt/brother/Printers/MFC7460DN/cupswrapper/brlpdwrapperMFC7460DN /usr/libexec/cups/filter/brlpdwrapperMFC7460DN
}
