#!/bin/bash

[ -z "$1" ] && exit 1

DATA=`date +%Y-%m-%d`

NET="$2"
LOCAL="$1"
DESC="$3"
BULK=bulk/bulk_"$1"-"$DATA"-$5.txt

nmap_win(){

    IFS=$'\n'
    > $BULK
    #nmap -iL $NET --open -p 3389 | grep ^'Nmap scan report' > $NMAP_TMP
    for line in $(nmap $NET -P0 --open -p3389,445 | grep ^'Nmap scan report')
    #for line in $(nmap $NET -P0 --open -p 3389 --host-timeout .3 | grep ^'Nmap scan report')
    do 
	WHOST=`echo "$line" |cut -d' ' -f5`
	WIP=`echo "$line" |cut -d' ' -f6 | sed -e 's/[\)\(]//g'`

	./winmap2.sh "$WHOST" "$WIP" "$LOCAL" "$DESC" "$BULK"

    done
}
nmap_win;
