# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI="6"
ETYPE="sources"

DEPEND="dev-util/patchutils"

inherit kernel-2 git-r3 versionator
detect_version
detect_arch

DESCRIPTION="amd-staging kernel with DC/DAL, plus gentoo-sources patches"
HOMEPAGE="https://cgit.freedesktop.org/~agd5f/linux/log/?h=amd-staging-4.9"
LICENSE="GPL-2 freedist"
IUSE="+gentoo-base +gentoo-extras +gentoo-experimental"

GENTOO_BASE_PATCHES="1500_XATTR_USER_PREFIX.patch
1510_fs-enable-link-security-restrictions-by-default.patch
2300_enable-poweroff-on-Mac-Pro-11.patch"

GENTOO_EXTRA_PATCHES="4200_fbcondecor.patch
4400_alpha-sysctl-uac.patch
4567_distro-Gentoo-Kconfig.patch"

GENTOO_EXP_PATCHES="5001_block-cgroups-kconfig-build-bits-for-BFQ-v7r11-4.9.patch
5002_block-introduce-the-BFQ-v7r11-I-O-sched-for-4.9.patch1
5003_block-bfq-add-Early-Queue-Merge-EQM-to-BFQ-v7r11-for-4.9.patch
5004_Turn-BFQ-v7r11-into-BFQ-v8r7-for-4.9.0.patch1
5010_enable-additional-cpu-optimizations-for-gcc.patch"

kver=$(get_version_component_range 1-3)
SRC_URI="https://cdn.kernel.org/pub/linux/kernel/v4.x/patch-${kver}.xz
gentoo-base? ( https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/1500_XATTR_USER_PREFIX.patch
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/1510_fs-enable-link-security-restrictions-by-default.patch
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/2300_enable-poweroff-on-Mac-Pro-11.patch )
gentoo-extras? ( https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/4200_fbcondecor.patch
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/4400_alpha-sysctl-uac.patchhttps://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/4567_distro-Gentoo-Kconfig.patch )
gentoo-experimental? ( https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/5001_block-cgroups-kconfig-build-bits-for-BFQ-v7r11-4.9.patch
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/5002_block-introduce-the-BFQ-v7r11-I-O-sched-for-4.9.patch1
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/5003_block-bfq-add-Early-Queue-Merge-EQM-to-BFQ-v7r11-for-4.9.patch
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/5004_Turn-BFQ-v7r11-into-BFQ-v8r7-for-4.9.0.patch1
https://dev.gentoo.org/~mpagano/genpatches/trunk/4.9/5010_enable-additional-cpu-optimizations-for-gcc.patch )"

EGIT_REPO_URI="git://people.freedesktop.org/~agd5f/linux"
EGIT_BRANCH="amd-staging-4.9"

pdate="$(get_version_component_range 4)"
EGIT_COMMIT_DATE=${pdate%p}
KEYWORDS="~amd64"

EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	xz -d ${DISTDIR}/patch-${kver}.xz -c | filterdiff -x '*/gpu/drm/amd/*' -x '*/gpu/drm/radeon/*' -x '*/gpu/drm/ttm/*' > ${T}/patch-${kver}-fixed.patch
	eapply ${T}/patch-${kver}-fixed.patch

	if use gentoo-base ; then
		for i in ${GENTOO_BASE_PATCHES} ; do
			eapply ${DISTDIR}/${i}
		done
	fi

	if use gentoo-extras ; then
		for i in ${GENTOO_EXTRA_PATCHES} ; do
			eapply ${DISTDIR}/${i}
		done
	fi

	if use gentoo-experimental ; then
		for i in ${GENTOO_EXP_PATCHES} ; do
			eapply ${DISTDIR}/${i}
		done
	fi

	eapply_user

	unpack_fix_install_path
	unpack_set_extraversion
	touch .scmversion
}
