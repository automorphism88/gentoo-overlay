# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
ETYPE="sources"

inherit kernel-2 git-r3 versionator

DESCRIPTION="amd-staging kernel with DC/DAL, plus gentoo-sources patches"
HOMEPAGE="https://cgit.freedesktop.org/~agd5f/linux/log/?h=amd-staging-4.11"
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
MY_GITV="${MY_TMPV:3:4}-${MY_TMPV:7:2}-${MY_TMPV:9:2}"
MY_GENPATCHESV="${MY_TMPV:13}"

if [[ "MY_MINORV" -ge 1 ]] ; then
	SRC_URI="https://cdn.kernel.org/pub/linux/kernel/v4.x/patch-${MY_PATCHV}.xz"
else
	SRC_URI=""
fi

SRC_URI+="
	gentoo-base? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.base.tar.xz )
	gentoo-extras? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.extras.tar.xz )
	gentoo-experimental? ( genpatches-${MY_MAJORV}-${MY_GENPATCHESV}.experimental.tar.xz )"

# ensure we can merge kernel.org patches with git
EGIT_MIN_CLONE_TYPE="single"

EGIT_REPO_URI="git://people.freedesktop.org/~agd5f/linux"
EGIT_BRANCH="amd-staging-${MY_MAJORV}"
EGIT_COMMIT="e16e1739c334c1e3a180402c7e30391f6de8ddf2"
EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	if [[ "MY_MINORV" -ge 1 ]] ; then
		einfo "Applying $MY_PATCHV to git repo as of $MY_GITV"
		xz -cd "${DISTDIR}"/patch-${MY_PATCHV}.xz | git apply --3way --ignore-whitespace -
		[[ ${PIPESTATUS[0]} -eq 0 ]] || die
		[[ ${PIPESTATUS[1]} -ge 2 ]] && die
	else
		einfo "Using git repo as of $MY_GITV"
	fi

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
	rm -fr .git || die
	touch .scmversion || die
}
