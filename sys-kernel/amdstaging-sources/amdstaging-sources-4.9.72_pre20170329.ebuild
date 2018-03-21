# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
ETYPE="sources"

inherit kernel-2 git-r3 versionator

DESCRIPTION="amd-staging kernel with DC/DAL, plus gentoo-sources patches"
HOMEPAGE="https://cgit.freedesktop.org/~agd5f/linux/log/?h=amd-staging-4.9"
LICENSE="GPL-2 freedist"
KEYWORDS="amd64 x86"
IUSE="+gentoo-base +gentoo-extras +gentoo-experimental"

detect_version
detect_arch

MY_PATCHV="$(get_version_component_range 1-3)"
MY_MAJORV="$(get_version_component_range 1-2)"
MY_MINORV="$(get_version_component_range 3)"
# avoid calling sed/cut in global scope
MY_TMPV="$(get_version_component_range 4)"
MY_GITV="${MY_TMPV:3:8}"

EGIT_REPO_URI="https://github.com/automorphism88/amd-staging-sources.git"
EGIT_BRANCH="${MY_MAJORV}-${MY_GITV}"
EGIT_COMMIT="${MY_PATCHV}_pre${MY_GITV}"
EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	local i j
	for i in base extras experimental ; do
		if use gentoo-${i} ; then
			for j in "${FILESDIR}/gentoo-${MY_MAJORV}-${i}/"* ; do
				eapply "${j}"
			done
		fi
	done
	eapply_user
	unpack_fix_install_path
	unpack_set_extraversion
	rm -fr .git || die
	touch .scmversion || die
}
