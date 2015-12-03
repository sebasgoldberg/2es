#!/bin/bash

A_PROCESAR="a-procesar"
VENDA="venda"
RUPTURA="ruptura"
QUEBRA="quebra"
PROCESADOS="procesados"

log(){
    echo "[$(date --rfc-3339=seconds)]" "[$@]" >> ./evodashd.log
}

info(){
    log "INFO: " $@
}

error(){
    log "ERROR: " $@
}

verify_exists_or_create_path(){

    FOLDER_PATH="$1"

    if [ ! -d "$FOLDER_PATH" ]; then
        mkdir -p "$FOLDER_PATH"

        if [ $? -ne 0 ]; then
            log "ERROR: " /bin/mkdir -p "$FOLDER_PATH"
            exit 1
        fi
    fi

}

procesar_modelo(){

    A_PROCESAR_PATH="$1"
    EXEC_PATH="$2"
    PROCESADOS_PATH="$3"

    verify_exists_or_create_path "$A_PROCESAR_PATH"
    verify_exists_or_create_path "$PROCESADOS_PATH"

    for i in $(/usr/bin/find "$A_PROCESAR_PATH/" -type f)
    do
        info "$EXEC_PATH/prepare-files.sh" "$i"
        "$EXEC_PATH/prepare-files.sh" "$i"

        if [ $? -ne 0 ]; then
            log "ERROR: " "$EXEC_PATH/prepare-files.sh" "$i"
            exit 1
        fi
    done

    for i in $(/usr/bin/find "$A_PROCESAR_PATH/" -type f)
    do

        info "$EXEC_PATH/read.py" "$i"
        "$EXEC_PATH/read.py" "$i"

        if [ $? -ne 0 ]; then
            log "ERROR: " "$EXEC_PATH/read.py" "$i"
            exit 1
        fi

        /bin/mv "$i" "$PROCESADOS_PATH/"

        if [ $? -ne 0 ]; then
            log "ERROR: " /bin/mv "$i" "$PROCESADOS_PATH/"
            exit 1
        fi

    done
}

procesar(){

    procesar_modelo "./$A_PROCESAR/$VENDA" "./$VENDA" "./$PROCESADOS/$VENDA"
    procesar_modelo "./$A_PROCESAR/$QUEBRA" "./$QUEBRA" "./$PROCESADOS/$QUEBRA"
    procesar_modelo "./$A_PROCESAR/$RUPTURA" "./$RUPTURA" "./$PROCESADOS/$RUPTURA"

    for i in $(/usr/bin/find . -maxdepth 1 -name "*.json"); do

        info ./els/upload.sh "$i"
        ./els/upload.sh "$i"

        if [ $? -ne 0 ]; then
            log "ERROR: " ./els/upload.sh "$i"
            exit 1
        fi

    done

    for i in $(/usr/bin/find . -maxdepth 1 -name "*.json"); do
        info /bin/rm "$i"
        /bin/rm "$i"

        if [ $? -ne 0 ]; then
            log "ERROR: " /bin/rm "$i"
            exit 1
        fi
    done

}

verify_exists_or_create_path "./$PROCESADOS"

while true
do
    procesar
    /bin/sleep 10
done
