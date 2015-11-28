#!/bin/bash
#
#
#{
#      "_index": "mac",
#      "_type": "mac",
#      "_id": "78:2B:CB:C0:85:37",
#      "_score": 1,
#      "_source": {
#          "estado_antivirus": "Atualizado",
#          "nome_usuario": "ANDERSON ANDRADE MOTA",
#          "usuario_red": "aandmota",
#          "nome_maquina": "g300603ws211",
#          "mac_address": "78:2B:CB:C0:85:37"
#       }
#}

WSTATUS=0
AV=0
GS=0
LY=0
AT=0
PCA=0
OSA=0

LOCAL="$3"
DESC="$4"
BULK="$5"

WUSER_WPASS='DOMAIN\user%pass'

WHOST="$1"
WIP="$2"

### DATA
DATA=`date +%Y-%m-%d`

smbclient -t 8 -U "$WUSER_WPASS" "//$WHOST/c$" 2>/tmp/smbclient.tmp$$ <<EOF
 mkdir Temp
 cd Temp
 put winmap.bat
EOF
if [ "$?" == 0 ]; then
    WSTATUS=1
    echo "$WHOST - ok"
fi

if [ "$WSTATUS" == 1 ]; then
    if grep -q 2000 /tmp/smbclient.tmp$$ ; then
	echo "$WHOST failll"
	OSV='Windows XP'
	OSA='32'

    else 
	OSV=$(cat /tmp/smbclient.tmp$$ |grep Doma | awk -F'=' '{ print $3 }')

	FULL=$(winexe -U $WUSER_WPASS //$WHOST 'cmd /c "c:\Temp\winmap.bat" ')

	if echo "$FULL" | grep 'Arch: 64' ; then
	    OSA=64
	else
	    OSA=32
	fi

	if echo "$FULL" | grep 'AV: 1'; then
	    AV=1
	fi
	if echo "$FULL" | grep 'GS: 1'; then
	    GS=1
	fi
	if echo "$FULL" | grep 'PCA: 1'; then
	    PCA=1
	fi
	if echo "$FULL" | grep 'AT: 1'; then
	    AT=1
	fi
	if echo "$FULL" | grep 'LY: 1'; then
	    LY=1
	fi
    fi

    unset http_proxy
    echo 
    echo "{\"index\": {\"_type\": \"status\", \"_id\": \"$WHOST-$DATA\", \"_index\": \"windows_clients\"}}
{ \"status\": "$WSTATUS", \"estado_antivirus\": "$AV", \"nome_maquina\": \"$WHOST\", \"auto_gestao_senha\": "$GS", \"lync\": "$LY", \"altiris\": "$AT", \"ip\": \"$WIP\", \"local\": \"$LOCAL\", \"data\": \"$DATA 12:00:00\", \"pcA\": "$PCA", \"osArch\": \"$OSA\", \"osVersion\": \"$OSV\", \"descricao\": \"$DESC\" }" >> $BULK

    echo "{\"index\": {\"_type\": \"status\", \"_id\": \"$WHOST-$DATA\", \"_index\": \"windows_clients\"}}
{ \"status\": "$WSTATUS", \"estado_antivirus\": "$AV", \"nome_maquina\": \"$WHOST\", \"auto_gestao_senha\": "$GS", \"lync\": "$LY", \"altiris\": "$AT", \"ip\": \"$WIP\", \"local\": \"$LOCAL\", \"data\": \"$DATA 12:00:00\", \"pcA\": "$PCA", \"osArch\": \"$OSA\", \"osVersion\": \"$OSV\", \"descricao\": \"$DESC\" } -- $BULK"

fi
#echo "
#curl -XPOST 'http://10.151.1.21:9200/_bulk?pretty' -d "
#{\"index\": {\"_type\": \"status\", \"_id\": \"$WHOST-$DATA\", \"_index\": \"windows_clients\"}}
#{\"estado_antivirus\": "$AV", \"nome_maquina\": \"$WHOST\", \"auto_gestao_senha\": "$GS", \"lync\": "$LY", \"altiris\": "$AT", \"ip\": \"$WIP\", \"local\": \"$LOCAL\", \"data\": \"$DATA 12:00:00\", \"pcA\": "$PCA" }
#"

