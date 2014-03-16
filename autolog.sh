#!/bin/bash
cd /tmp
while true; do
	cp "/home/aleksandarkubuntu1304/.irssilogs/#floss-magazin.$(date +%d.%m.%Y).log" "/tmp/#floss-magazin.$(date +%d.%m.%Y).log"
	irclog2html "#floss-magazin.$(date +%d.%m.%Y).log" > "/home/aleksandarkubuntu1304/Ubuntu One/LiBRE!/Autolog/log.html"
	sleep 10
done
