# gentoo-overlay
Personal Gentoo overlay, containing a combination of staging ebuilds I may
eventually get merged into the official repos, experimental ebuilds that are
too hackish to upstream, official ebuilds I've modified to reflect my own
preferences, and ebuilds previously removed from the official portage tree
which I continue to find useful.

## Instructions
You can add this overlay to your system using either the layman method or the
repos.conf method, as described below. You may also need to add the package(s)
you wish to install to `/etc/portage/package.keywords` (see the Gentoo wiki).
### Using layman
```
layman -o https://raw.githubusercontent.com/automorphism88/gentoo-overlay/master/automorphism.xml -f -a automorphism
```
### Using repos.conf
Create a file in `/etc/portage/repos.conf` with the following contents (if it
is a directory, otherwise, add the following to the end of the file):
```
[automorphism]
location = /foo/bar
sync-type = git
sync-uri = https://github.com/automorphism88/gentoo-overlay.git/
auto-sync = yes
```

## Packages
See the file `metadata/pkg_desc_index` for a list of available packages.

## Bugs
Please report any bugs on GitHub at
https://github.com/automorphism88/gentoo-overlay
