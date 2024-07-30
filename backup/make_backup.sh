#!/bin/bash
name=`date +%s`
pg_dump postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -Fc > /backups/$name

cnt=$( ls /backups | wc -l )
let delete_cnt=$cnt-$M
if [[ $delete_cnt -le 0 ]]
then
    exit 0
fi

ls /backups | sort | head -$delete_cnt | xargs -I {} bash -c 'rm /backups/"{}"' 
