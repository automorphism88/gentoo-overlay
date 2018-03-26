#!/bin/sh -
(
    set -e
    CDPATH= cd -- "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/../../../.."
    git subtree pull --prefix x11-drivers/ati-drivers/files/external/arch-AUR \
        https://aur.archlinux.org/catalyst.git master --squash \
        -m 'x11-drivers/ati-drivers: merge updated AUR subtree'
)
