# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

DESCRIPTION="Dracut module which allows remote unlocking of systems"
HOMEPAGE="https://github.com/dracut-crypt-ssh/dracut-crypt-ssh/pulls"

LICENSE="GPL-2"
SLOT="0"

if [[ "${PV}" = 9999 ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/dracut-crypt-ssh/dracut-crypt-ssh.git"
	KEYWORDS=""
	SRC_URI=""
else
	KEYWORDS="~amd64 ~x86"
	SRC_URI="https://github.com/${PN}/${PN}/archive/v${PV}.tar.gz"
fi

DEPEND="sys-kernel/dracut"
RDEPEND="${DEPEND}"

DOCS=( README.md )
