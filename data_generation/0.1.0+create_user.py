from faker import Faker
import psycopg2
import logging
from random import randint
import os
import time
import traceback

table = 'users'

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

num_records = int(os.getenv("USERS_COUNT"))

for i in range(num_records):
    name = fake.name()
    email = fake.unique.email()
    password = fake.password(length = randint(10,20))
    number_of_bears = randint(0, 100000)

    sql = f"""
    INSERT INTO {table} (name, email, password, number_of_bears)
    VALUES ('{name}', '{email}', '{password}', {number_of_bears});
    """

    cur.execute(sql)

    if i % 10000 == 0:
        conn.commit()

conn.commit()

cur.close()
conn.close()

print("0.1.0 data generated")