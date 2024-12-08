import psycopg2
from psycopg2 import sql


host = "localhost"
port = "5432"
user = "postgres"
password = "postgres"
db_name = "GymPlanner"

try:

    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True

    cursor = conn.cursor()

    query = sql.SQL("CREATE DATABASE {db_name}").format(
        db_name=sql.Identifier(db_name)
    )

    cursor.execute(query)
    print(f"База данных '{db_name}' успешно создана!")

except Exception as e:
    print(f"Ошибка при создании базы данных: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()