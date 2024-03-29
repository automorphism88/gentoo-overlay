# Copyright 1999-2021 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI="7"

inherit font

DESCRIPTION="Mathematica's Fonts for MathML"
HOMEPAGE="http://www.wolfram.com/mathematica"
SRC_URI="http://support.wolfram.com/kb/data/uploads/2014/08/TrueType.zip -> ${P}.zip"

LICENSE="WRI-EULA"
SLOT="0"
KEYWORDS="~alpha amd64 ~ia64 ~ppc ~ppc64 ~sparc x86 ~amd64-linux ~x86-linux"
IUSE=""

RESTRICT="binchecks mirror strip"

S="${WORKDIR}"
FONT_S="${S}"/TrueType
FONT_SUFFIX="ttf"
