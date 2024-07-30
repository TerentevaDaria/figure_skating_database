#!bin/bash

psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/postgres?sslmode=disable -tc "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'reader'" | grep -q 1 && exit;


psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "CREATE ROLE reader LOGIN;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "CREATE ROLE writer LOGIN;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "CREATE ROLE analytic LOGIN;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "CREATE ROLE group_role;"

psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader, writer, group_role;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT UPDATE ON ALL TABLES IN SCHEMA public TO writer, group_role;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT INSERT ON ALL TABLES IN SCHEMA public TO writer, group_role;"
psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT DELETE ON ALL TABLES IN SCHEMA public TO group_role;"

psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT SELECT ON TABLE predictions TO analytic;"

for role_name in "$@"
do 
    psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "CREATE ROLE $role_name LOGIN;"
    psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT group_role TO $role_name;"
    psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@haproxy:5000/figure_skating?sslmode=disable -c "GRANT CONNECT ON DATABASE $POSTGRES_DB TO $role_name"
done