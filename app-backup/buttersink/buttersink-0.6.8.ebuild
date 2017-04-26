# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=5
PYTHON_COMPAT=( python2_7 )

inherit distutils-r1 git-r3

DESCRIPTION="rsync-like utility for btrfs snapshots"
HOMEPAGE="https://github.com/AmesCornish/buttersink"

LICENSE="GPL-3"
SLOT=0

EGIT_REPO_URI="https://github.com/AmesCornish/buttersink"
SRC_URI=""

if [[ "${PV}" == 9999 ]] ; then
	KEYWORDS=""
else
	KEYWORDS="~amd64"
	EGIT_COMMIT="${PV}"
fi

RDEPEND="${PYTHON_DEPS}
	dev-python/boto
	dev-python/crcmod
	dev-python/flake8
	dev-python/psutil"
DEPEND="${RDEPEND}"

python_prepare()
{
	emake makestamps
	emake buttersink/version.py
}
