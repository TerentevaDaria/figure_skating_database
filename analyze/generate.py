# 1. все соревнования за определенный год 
# 2. конкретное соревнование как параметр. вывести всех участников и их места 
# 3. вывести фигуристов по параметру и отсортировать по рейтингу 
# 4. фигурист как параметр. вывести результаты за все время


from faker import Faker
import psycopg2
import logging
from random import randint
import os
import time
from datetime import datetime


cnt = int(os.getenv("COUNT"))

requests = []
year = 2000
requests.append(f"""
SELECT c.name, c.city, country.name as country_name, c.start_date, c.end_date FROM competition as c
JOIN country on country.country_id = c.country_id
WHERE DATE_PART('year', c.start_date) = {year} or DATE_PART('year', c.end_date) = {year}
""")

competition_id = 100
requests.append(f"""
SELECT team.discipline, pi.place, pi.points, athletes.full_name FROM competition_participants as cp
JOIN participation_information as pi on cp.competition_participant_id = pi.competition_participant_id
JOIN team on team.team_id = cp.team_id
JOIN team_athlete_connection as tac on tac.team_id = cp.team_id
JOIN athletes on athletes.athlete_id = tac.athlete_id
WHERE cp.competition_id = {competition_id} and pi.type = 'total'
ORDER BY team.discipline, pi.place
""")

discipline = 'pair_skating'
requests.append(f"""
SELECT a1.full_name, a2.full_name, team.number_of_bears FROM athletes as a1
	JOIN team_athlete_connection as tac1 on tac1.athlete_id = a1.athlete_id
	JOIN team_athlete_connection as tac2 on tac2.team_id = tac1.team_id
	JOIN athletes as a2 on a2.athlete_id = tac2.athlete_id
	JOIN team on tac1.team_id = team.team_id
	WHERE tac1.athlete_id < tac2.athlete_id and team.discipline = '{discipline}'
    ORDER BY team.number_of_bears DESC;
""")

id = 5
requests.append(f"""
SELECT a.full_name, team.discipline, c.name, DATE_PART('year', c.start_date), pi.place, pi.points FROM athletes as a
JOIN team_athlete_connection as tac on tac.athlete_id = a.athlete_id
JOIN team on team.team_id = tac.team_id
JOIN competition_participants as cp on cp.team_id = team.team_id
JOIN competition as c on c.competition_id = cp.competition_id
JOIN participation_information as pi on pi.competition_participant_id = cp.competition_participant_id
WHERE pi.type = 'total' and a.athlete_id = {id}
ORDER BY c.start_date;
""")

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

filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

for request in requests:
    best = float(10 ** 18)
    worst = float(0)
    s = float(0)
    for i in range(cnt):
        cur.execute(f"EXPLAIN (ANALYZE) {request}")
        res = float(cur.fetchall()[-1][0].split(" ")[-2])
        best = min(best, res)
        worst = max(worst, res)
        s += res
    with open(f'/data/{filename}.txt', "a") as f:
        f.write(f"{worst} {best} {round(s / cnt, 3)}\n")

cur.close()
conn.close()

print("analyze finished")