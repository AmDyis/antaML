import psycopg2
import pandas as pd
from model import merged_target

# Установка соединения с базой данных
conn = psycopg2.connect(
    host="localhost",
    database="anta",
    user="postgres",
    password="**********"
)

# Создание объекта курсора для выполнения SQL-запросов
cur = conn.cursor()

# Создание таблицы, если она еще не существует
cur.execute("""
    CREATE TABLE IF NOT EXISTS antarktida (
        id SERIAL PRIMARY KEY,
        station_name VARCHAR(255),
        year2001 FLOAT,
        year2002 FLOAT,
        year2003 FLOAT,
        year2004 FLOAT,
        year2005 FLOAT,
        year2006 FLOAT,
        year2007 FLOAT,
        year2008 FLOAT,
        year2009 FLOAT,
        year2010 FLOAT,
        year2011 FLOAT,
        year2012 FLOAT,
        year2013 FLOAT,
        year2014 FLOAT,
        year2015 FLOAT,
        year2016 FLOAT,
        year2017 FLOAT,
        year2018 FLOAT,
        year2019 FLOAT,
        year2020 FLOAT,
        year2021 FLOAT,
        year2022 FLOAT,
        year2023 FLOAT,
        year2024 FLOAT,
        year2025 FLOAT,
        year2026 FLOAT,
        latitude FLOAT,
        longitude FLOAT,
        lvlsea FLOAT
    )
""")
df = pd.read_excel("Средняя и коорды.xlsx")
df = df.set_index("станция")
# Слияние двух датафреймов по индексам
mega_df = merged_target.merge(df, left_index=True, right_index=True, how='inner')



# Загрузка данных из DataFrame в таблицу PostgreSQL
for index, row in mega_df.iterrows():
    cur.execute("""
        INSERT INTO antarktida (station_name, year2001, year2002, year2003, year2004, year2005,
                                year2006, year2007, year2008, year2009, year2010, year2011, year2012,
                                year2013, year2014, year2015, year2016, year2017, year2018, year2019,
                                year2020, year2021, year2022, year2023, year2024, year2025, year2026,
                                 latitude, longitude, lvlsea)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)
    """, [index] + list(row))

# Подтверждение изменений
conn.commit()

# Выполнение SQL-запроса
cur.execute("SELECT * FROM antarktida LIMIT 5")

# Получение результатов запроса
rows = cur.fetchall()

# Вывод результатов
for row in rows:
    print(row)

# Закрытие соединения
conn.close()
