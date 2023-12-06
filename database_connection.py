import aiomysql

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'botUsers',
}

async def create_connection():

    connection = await aiomysql.connect(**DATABASE_CONFIG)
    cursor = await connection.cursor()
    return connection, cursor

async def close_connection(cursor,con):
    cursor.close()
    con.close()