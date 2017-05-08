# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=4
SLOT=0

inherit git-r3

DESCRIPTION="Philosoraptor cow for games-misc/cowsay"
HOMEPAGE="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/"
KEYWORDS="amd64"

SRC_URI=""
EGIT_REPO_URI="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune"
EGIT_COMMIT="1c5776d405868f52abd621faef110d3e396d00d5"

DEPEND="${RDEPEND}"
RDEPEND="games-misc/cowsay"

src_install()
{
	insinto /usr/share/cows
	doins raptor.cow
}
