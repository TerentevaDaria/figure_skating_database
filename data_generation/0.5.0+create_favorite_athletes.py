from faker import Faker
import psycopg2
import logging
from random import randint
import random
import os
import time
import traceback

table = 'favorite_athletes'

conn = None
for i in range(int(os.getenv("CONNECTION_ATTEMPTS"))):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        break
    except Exception as e:
        conn = None
    time.sleep(20)

cur = conn.cursor()

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table,))
if not cur.fetchone()[0]:
    exit(0)

cur.execute(f"select count(*) from {table}")
if int(cur.fetchone()[0]) != 0:
    exit(0)


fake = Faker()

num_records = 10 * int(os.getenv("USERS_COUNT"))

added = set()

for i in range(num_records):
    user_id = randint(1, int(os.getenv("USERS_COUNT")))
    team_id = int(random.expovariate(1 / int(os.getenv("ATHLETES_COUNT"))) % int(os.getenv("ATHLETES_COUNT"))) + 1

    while (user_id, team_id) in added:
        user_id = randint(1, int(os.getenv("USERS_COUNT")))
        team_id = int(random.expovariate(1 / int(os.getenv("ATHLETES_COUNT"))) % int(os.getenv("ATHLETES_COUNT"))) + 1
    added.add((user_id, team_id))

    sql = f"""
    INSERT INTO {table} (user_id, team_id)
    VALUES ({user_id}, {team_id});
    """

    cur.execute(sql)

    if i % 10000 == 0:
        conn.commit()

conn.commit()

cur.close()
conn.close()

print("0.5.0 data generated")