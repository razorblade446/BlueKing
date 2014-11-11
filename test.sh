#!/bin/bash

function limpieza {
	ps axu|grep -v grep|grep BlueKing|awk '{print $2}'|while read bkpids
	do
		echo "Matando pid $bkpids..."
		kill -9	$bkpids
	done
	find $PWD -name \*.pyc|xargs rm -f

	exit
}

trap limpieza SIGINT SIGHUP SIGTERM

DISPLAY=:0 python -m BlueKing &

echo "Probando... CTRL+C para abortar"

while :
do
	sleep 1
done
