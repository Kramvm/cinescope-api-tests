import psycopg2
from resources.db_creds import DbCreds


def get_server_info():
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname=DbCreds.DBNAME,
            user=DbCreds.USER,
            password=DbCreds.PASSWORD,
            host=DbCreds.HOST,
            port=DbCreds.PORT
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        connection.close()

    except Exception as error:
        print("ошибка при работе с базой данных", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    get_server_info()


