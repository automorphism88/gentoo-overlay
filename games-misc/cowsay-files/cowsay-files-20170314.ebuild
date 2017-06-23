# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
SLOT=0

inherit git-r3

DESCRIPTION="Collection of additional cow files for games-misc/cowsay"
HOMEPAGE="https://github.com/paulkaefer/cowsay-files/"
KEYWORDS="amd64 x86"

SRC_URI=""
EGIT_REPO_URI="https://github.com/paulkaefer/cowsay-files/"
EGIT_COMMIT="710518b62a2c4644eac72e04a77e4ebb073d58e3"

DEPEND="${RDEPEND}"
RDEPEND="games-misc/cowsay"

src_install()
{
	insinto /usr/share/cows
	doins cows/*.cow
}
