import psycopg2
from config import db_name, host
import getpass
connection = None
system_username = getpass.getuser()

try:
    connection = psycopg2.connect(
        host=host,
        user=system_username,
        database=db_name,
        # port=port
    )
    cursor = connection.cursor()
    cursor.execute('SELECT version();')
    print(cursor.fetchone())
except Exception as _ex:
    print(_ex)
finally:
    if connection:
        cursor.close()
        connection.close()
