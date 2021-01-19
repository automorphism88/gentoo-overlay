#!/bin/sed -zf
:x
\:/usr/local/Brother/Printer:{
	s:/usr/local/Brother/Printer:/opt/brother/Printers:
	s/$/\x00\x00\x00\x00\x00/
	bx
}
\:/usr/local/Brother/inf:{
	s:/usr/local/Brother/inf:/opt/brother/inf:
	s/$/\x00\x00\x00\x00\x00\x00/
	bx
}
\:/etc/printcap.local:{
	s:/etc/printcap.local:/etc/printcap:
	s/$/\x00\x00\x00\x00\x00\x00/
	bx
}
