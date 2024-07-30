#!bin/bash

psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/postgres?sslmode=disable -f /init/create_role.sql

psql postgres://creator:creator@haproxy:5000/postgres?sslmode=disable -tc "SELECT 1 FROM pg_database WHERE datname = 'figure_skating'" | grep -q 1 || psql postgres://creator:creator@haproxy:5000/postgres?sslmode=disable -c "CREATE DATABASE figure_skating;"

f () {
    major=$( echo "$1" | awk -F '+' '{print $1}' | awk -F '.' '{print $1}' )
    minor=$( echo "$1" | awk -F '+' '{print $1}' | awk -F '.' '{print $2}' )
    patch=$( echo "$1" | awk -F '+' '{print $1}' | awk -F '.' '{print $3}' )

    last_major=$( echo "$VERSION" | awk -F '.' '{print $1}' )
    last_minor=$( echo "$VERSION" | awk -F '.' '{print $2}' )
    last_patch=$( echo "$VERSION" | awk -F '.' '{print $3}' )

    if [[ $major -lt $last_major || ( $major -eq $last_major && $minor -lt $last_minor ) ||  ( $major -eq $last_major && $minor -eq $last_minor && $patch -le $last_patch ) ]]
    then
        echo "$major $minor $patch ../migration/$1"
    fi
}


export -f f
ls /migration | xargs -I {} bash -c 'f {}' | sort -nk1,1 -nk2,2 -nk3,3 | awk '{print $4}' | xargs -I {} bash -c 'psql postgres://creator:creator@haproxy:5000/figure_skating?sslmode=disable -f {}'
env POSTGRES_DB="figure_skating" POSTGRES_USER="postgres" bash ../roles/init_roles.sh user1 user2