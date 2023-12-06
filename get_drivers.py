from database_connection import create_connection,close_connection

async def get_drivers():
    connection, cursor = await create_connection()

    try:
        query = "SELECT * FROM botUsers WHERE role = 'Driver';"
        await cursor.execute(query)
        drivers = await cursor.fetchall()
        print(drivers)
        return drivers
    finally:
        await close_connection(connection, cursor)
