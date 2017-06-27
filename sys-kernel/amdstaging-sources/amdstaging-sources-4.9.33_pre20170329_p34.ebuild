# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
ETYPE="sources"

inherit kernel-2 git-r3 versionator

DESCRIPTION="amd-staging kernel with DC/DAL, plus gentoo-sources patches"
HOMEPAGE="https://cgit.freedesktop.org/~agd5f/linux/log/?h=amd-staging-4.9"
LICENSE="GPL-2 freedist"
KEYWORDS="~amd64 ~x86"
IUSE="+gentoo-base +gentoo-extras +gentoo-experimental"

detect_version
detect_arch

MY_PATCHV="$(get_version_component_range 1-3)"
MY_MAJORV="$(get_version_component_range 1-2)"
MY_MINORV="$(get_version_component_range 3)"
# avoid calling sed/cut in global scope
MY_TMPV="$(get_version_component_range 4-5)"
MY_GITV="${MY_TMPV:3:8}"
MY_GENPATCHESV="${MY_TMPV:13}"

SRC_URI="
	gentoo-base? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.base.tar.xz )
	gentoo-extras? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.extras.tar.xz )
	gentoo-experimental? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.experimental.tar.xz )"

EGIT_REPO_URI="https://github.com/automorphism88/amd-staging-sources.git"
EGIT_BRANCH="${MY_MAJORV}-${MY_GITV}"
EGIT_COMMIT="${MY_PATCHV}"
EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	local MY_PATCHDIR="${T}/patches"
	mkdir "${MY_PATCHDIR}" || die
	pushd "${MY_PATCHDIR}" || die
	use gentoo-base && unpack genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.base.tar.xz && rm {0[0-9],1[0-4]}[0-9][0-9]_*
	use gentoo-extras && unpack genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.extras.tar.xz
	use gentoo-experimental && unpack genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.experimental.tar.xz
	popd || die
	for i in "${MY_PATCHDIR}"/* ; do eapply "${i}" ; done

	eapply_user

	unpack_fix_install_path
	unpack_set_extraversion
	rm -fr .git
	touch .scmversion
}
