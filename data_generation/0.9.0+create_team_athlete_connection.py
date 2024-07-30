from faker import Faker
import psycopg2
import logging
from random import randint
import random
import os
import time
import traceback
from datetime import date

table = 'team_athlete_connection'

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

num_records = 3 * int(os.getenv("ATHLETES_COUNT")) // 2

for team_id in range(1, num_records + 1):
    cur.execute(F"SELECT discipline FROM team WHERE team_id={team_id}")
    discipline = cur.fetchone()
    if discipline[0] in ["men's_singles", "women's_singles"]:
        athlete_id = randint(1, int(os.getenv("ATHLETES_COUNT")))

        sql = f"""
        INSERT INTO {table} (team_id, athlete_id)
        VALUES ({team_id}, {athlete_id});
        """
        cur.execute(sql)
    else:
        athlete_id = randint(1, int(os.getenv("ATHLETES_COUNT")))

        sql = f"""
        INSERT INTO {table} (team_id, athlete_id)
        VALUES ({team_id}, {athlete_id});
        """
        cur.execute(sql)

        athlete_id2 = randint(1, int(os.getenv("ATHLETES_COUNT")))
        while athlete_id == athlete_id2:
            athlete_id2 = randint(1, int(os.getenv("ATHLETES_COUNT")))

        sql = f"""
        INSERT INTO {table} (team_id, athlete_id)
        VALUES ({team_id}, {athlete_id2});
        """
        cur.execute(sql)

    if team_id % 10000 == 0:
        conn.commit()

conn.commit()

cur.close()
conn.close()

print("0.9.0 data generated")