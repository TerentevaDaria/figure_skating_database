from faker import Faker
import psycopg2
import logging
from random import randint
import random
import os
import time
import traceback
from datetime import date

table = 'predictions'

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

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table,))
if not cur.fetchone()[0]:
    exit(0)

fake = Faker()

num_records = int(os.getenv("COMPETITION_COUNT")) // 10

cnt = 0
for competition_id in range(1, num_records + 1):
    cur.execute(f"""SELECT team.team_id, team.discipline, competition_participants.competition_participant_id FROM competition_participants 
                JOIN team on competition_participants.team_id=team.team_id 
                WHERE competition_participants.competition_id={competition_id}""")
    
    data = cur.fetchall()
    for i in range(randint(50, 300)):
        user_id = fake.unique.pyint(min_value=1, max_value=int(os.getenv("USERS_COUNT")))
        
        for tp in ["men's_singles", "women's_singles", 'pair_skating', 'ice_dance']:
            place = 1
            cur_ = list(filter(lambda x: x[1] == tp, data))
            random.shuffle(cur_)
            for i in range(randint(0, 3)):
                sql = f"""
                INSERT INTO {table} (user_id, competition_participant_id, place)
                VALUES ({user_id}, {cur_[i][2]}, {place});
                """
                cur.execute(sql)
                place += 1
                cnt += 1

        if cnt >= 10000:
            conn.commit()

    fake.unique.clear()
conn.commit()

cur.close()
conn.close()

print("1.0.0 data generated")