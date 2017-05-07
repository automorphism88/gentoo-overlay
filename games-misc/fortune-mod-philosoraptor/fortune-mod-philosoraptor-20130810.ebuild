# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=4
SLOT=0

inherit git-r3

DESCRIPTION="Philosoraptor quotes for games-misc/fortune-mod"
HOMEPAGE="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune/"
KEYWORDS="amd64"

SRC_URI=""
EGIT_REPO_URI="https://bitbucket.org/rohtie/philosoraptor-cowsay-fortune"
EGIT_COMMIT_DATE="${PV}"

DEPEND="${RDEPEND}"
RDEPEND="games-misc/fortune-mod"

src_install()
{
	insinto /usr/share/fortune
	doins philos philos.dat
}
