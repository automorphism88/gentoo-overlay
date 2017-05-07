# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=4
SLOT=0

inherit git-r3

DESCRIPTION="Collection of additional cow files for games-misc/cowsay"
HOMEPAGE="https://github.com/paulkaefer/cowsay-files/"
KEYWORDS="amd64"

SRC_URI=""
EGIT_REPO_URI="https://github.com/paulkaefer/cowsay-files/"
EGIT_COMMIT_DATE="${PV}"

DEPEND="${RDEPEND}"
RDEPEND="games-misc/cowsay"

src_install()
{
	insinto /usr/share/cows
	doins cows/*
}
