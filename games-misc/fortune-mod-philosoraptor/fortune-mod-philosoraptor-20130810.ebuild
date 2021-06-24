# Copyright 1999-2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7
SLOT=0

inherit git-r3

DESCRIPTION="Philosoraptor quotes for games-misc/fortune-mod"
HOMEPAGE="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/"
KEYWORDS="amd64 x86"

SRC_URI=""
EGIT_REPO_URI="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune"
EGIT_COMMIT="1c5776d405868f52abd621faef110d3e396d00d5"

DEPEND="${RDEPEND}"
RDEPEND="games-misc/fortune-mod"

src_install()
{
	insinto /usr/share/fortune
	doins philos philos.dat
}
