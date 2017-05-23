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

SRC_URI="https://cdn.kernel.org/pub/linux/kernel/v4.x/patch-4.11.2.xz
	gentoo-base? ( genpatches-4.11-4.base.tar.xz )
	gentoo-extras? ( genpatches-4.11-4.extras.tar.xz )
	gentoo-experimental? ( genpatches-4.11-4.experimental.tar.xz )"

EGIT_REPO_URI="git://people.freedesktop.org/~agd5f/linux"
EGIT_BRANCH="amd-staging-4.11"

EGIT_COMMIT="c285c73f2213f503a93aa142fff186e160b4a371"
KEYWORDS="~amd64"

EGIT_CHECKOUT_DIR="${WORKDIR}/linux-${PVR}-amdstaging"
S="${EGIT_CHECKOUT_DIR}"

src_prepare() {
	unpack patch-4.11.2.xz
	eapply patch-4.11.2

	if use gentoo-base ; then
		unpack genpatches-4.11-4.base.tar.xz
		for i in ${GENTOO_BASE_PATCHES} ; do
			eapply ${i}
		done
	fi

	if use gentoo-extras ; then
		unpack genpatches-4.11-4.extras.tar.xz
		for i in ${GENTOO_EXTRA_PATCHES} ; do
			eapply ${i}
		done
	fi

	if use gentoo-experimental ; then
		unpack genpatches-4.11-4.experimental.tar.xz
		for i in ${GENTOO_EXP_PATCHES} ; do
			eapply ${i}
		done
	fi

	eapply_user

	unpack_fix_install_path
	unpack_set_extraversion
	touch .scmversion
}
