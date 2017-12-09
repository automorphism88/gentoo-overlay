# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
SLOT=0
inherit cmake-utils subversion
DEPEND="media-libs/speex"

if [[ "${PV}" == 9999 ]] ; then
	ESVN_REPO_URI="https://svn.code.sf.net/p/freetel/code/codec2-dev"
	KEYWORDS=""
else
	ESVN_REPO_URI="https://svn.code.sf.net/p/freetel/code/codec2/branches/${PV}"
	KEYWORDS="~amd64 ~x86"
fi
