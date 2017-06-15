# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
ETYPE="sources"

inherit kernel-2 git-r3
detect_version
detect_arch

DESCRIPTION="amd-staging kernel with DC/DAL, plus gentoo-sources patches"
HOMEPAGE="https://cgit.freedesktop.org/~agd5f/linux/log/?h=amd-staging-4.11"
LICENSE="GPL-2 freedist"
IUSE="+gentoo-base +gentoo-extras +gentoo-experimental"

DEPEND="dev-util/patchutils"

GENTOO_BASE_PATCHES="
	1500_XATTR_USER_PREFIX.patch
	1510_fs-enable-link-security-restrictions-by-default.patch
	2300_enable-poweroff-on-Mac-Pro-11.patch
	2900_dev-root-proc-mount-fix.patch
"

GENTOO_EXTRA_PATCHES="
	4200_fbcondecor.patch
	4400_alpha-sysctl-uac.patch
	4567_distro-Gentoo-Kconfig.patch
"

GENTOO_EXP_PATCHES="
	5001_block-cgroups-kconfig-build-bits-for-BFQ-v7r11-4.11.patch
	5002_block-introduce-the-BFQ-v7r11-I-O-sched-for-4.11.0.patch1
	5003_block-bfq-add-Early-Queue-Merge-EQM-to-BFQ-v7r11-for-4.11.patch
	5004_blkck-bfq-turn-BFQ-v7r11-for-4.11.0-into-BFQ-v8r11-for-4.patch1
	5010_enable-additional-cpu-optimizations-for-gcc.patch
"

SRC_URI="https://cdn.kernel.org/pub/linux/kernel/v4.x/patch-4.11.5.xz
	gentoo-base? ( genpatches-4.11-7.base.tar.xz )
	gentoo-extras? ( genpatches-4.11-7.extras.tar.xz )
	gentoo-experimental? ( genpatches-4.11-7.experimental.tar.xz )"

EGIT_REPO_URI="git://people.freedesktop.org/~agd5f/linux"
EGIT_BRANCH="amd-staging-4.11"

EGIT_COMMIT_DATE="2017-06-13"
KEYWORDS="~amd64"

EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	xz -cd "${DISTDIR}"/patch-4.11.5.xz |
		filterdiff -x "*/drivers/gpu/drm/amd/amdgpu/ci_dpm.c" -x "*/drivers/gpu/drm/amd/amdgpu/dce_v10_0.c" -x "*/drivers/gpu/drm/amd/amdgpu/dce_v11_0.c" -x "*/drivers/gpu/drm/amd/amdgpu/dce_v6_0.c" -x "*/drivers/gpu/drm/amd/amdgpu/dce_v8_0.c" -x "*/drivers/gpu/drm/amd/powerplay/hwmgr/smu7_hwmgr.c" -x "*/drivers/gpu/drm/radeon/*" > ${T}/patch-4.11.5-fixed
	eapply "${T}"/patch-4.11.5-fixed

	if use gentoo-base ; then
		pushd "${T}" && unpack genpatches-4.11-7.base.tar.xz && popd
		for i in ${GENTOO_BASE_PATCHES} ; do
			eapply "${T}"/${i}
		done
	fi

	if use gentoo-extras ; then
		pushd "${T}" && unpack genpatches-4.11-7.extras.tar.xz && popd
		for i in ${GENTOO_EXTRA_PATCHES} ; do
			eapply "${T}"/${i}
		done
	fi

	if use gentoo-experimental ; then
		pushd "${T}" && unpack genpatches-4.11-7.experimental.tar.xz && popd
		for i in ${GENTOO_EXP_PATCHES} ; do
			eapply "${T}"/${i}
		done
	fi

	eapply_user

	unpack_fix_install_path
	unpack_set_extraversion
	touch .scmversion
}
