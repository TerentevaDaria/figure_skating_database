from faker import Faker
import psycopg2
import logging
from random import randint
import random
import os
import time
import traceback
from datetime import date

table = 'participation_information'

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

num_records = int(os.getenv("COMPETITION_COUNT"))

cnt = 0
for competition_id in range(1, num_records + 1):
    cur.execute(f"""SELECT team.team_id, team.discipline, competition_participants.competition_participant_id FROM competition_participants 
                JOIN team on competition_participants.team_id=team.team_id 
                WHERE competition_participants.competition_id={competition_id}""")
    
    data = []
    for i in cur:
        data.append([])
        data[-1].append(i[0])
        data[-1].append(i[1])
        data[-1].append(random.randint(0, 20000) / 100)
        data[-1].append(random.randint(0, 40000) / 100)
        data[-1].append(data[-1][-1] + data[-1][-2])
        data[-1].append(i[2])
    
    map = {"men's_singles": 1, "women's_singles": 1, 'pair_skating': 1, 'ice_dance': 1}

    data.sort(key=lambda x: -x[2])
    for i in data:
        if i == True:
            break
        i.append(map[i[1]])
        map[i[1]] += 1
    
    map = {"men's_singles": 1, "women's_singles": 1, 'pair_skating': 1, 'ice_dance': 1}

    data.sort(key=lambda x: -x[3])
    for i in data:
        i.append(map[i[1]])
        map[i[1]] += 1
    
    map = {"men's_singles": 1, "women's_singles": 1, 'pair_skating': 1, 'ice_dance': 1}

    data.sort(key=lambda x: -x[4])
    for i in data:
        i.append(map[i[1]])
        map[i[1]] += 1
    
    for i in data:
        sql = f"""
        INSERT INTO {table} (competition_participant_id, type, place, points)
        VALUES ({i[5]}, 'short_program', {i[6]}, {i[2]});
        """
        cur.execute(sql)

        sql = f"""
        INSERT INTO {table} (competition_participant_id, type, place, points)
        VALUES ({i[5]}, 'free_skate', {i[7]}, {i[3]});
        """
        cur.execute(sql)

        sql = f"""
        INSERT INTO {table} (competition_participant_id, type, place, points)
        VALUES ({i[5]}, 'total', {i[8]}, {i[4]});
        """
        cur.execute(sql)
        cnt += 3

    if cnt >= 10000:
        cnt = 0
        conn.commit()

conn.commit()

cur.close()
conn.close()

print("0.17.0 data generated")