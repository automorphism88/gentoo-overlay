#!/bin/sed -f
s:/usr/local/Brother/Printer:/opt/brother/Printers:g
s:\(/etc/printcap\).local:\1:g
