#!/bin/sh





while true; do
	fdm -kmvv fetch 2>&1 | tee -a ~/.fdm.log
	sleep 5
done
