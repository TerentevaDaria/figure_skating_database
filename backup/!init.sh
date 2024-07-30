#!/bin/bash

while true; do
    bash /init/make_backup.sh
    sleep "${N}"h
done