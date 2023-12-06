from database_connection import create_connection,close_connection

async def get_ride_booking(userId):
    connection, cursor = await create_connection()

    try:
        query = "SELECT * FROM rideBooking WHERE userId = %s and status = 'pending';"
        await cursor.execute(query,(userId))
        drivers = await cursor.fetchall()
        return drivers[0]
    finally:
        await close_connection(connection, cursor)

async def add_booking_data(userId,status,date):
    conn,cursor = await create_connection()
    query = "Insert into rideBooking(userId, status, date) values(%s,%s,%s)"
    await cursor.execute(query,(userId,status,date))
    await conn.commit()
    await close_connection(cursor=cursor,con=conn)

async def update_booking_data(userId,status,date,name):
    conn,cursor = await create_connection()
    query = "UPDATE rideBooking SET status = %s, driver = %s WHERE userId = %s and date = %s"
    await cursor.execute(query,(status,name,userId,date))
    await conn.commit()
    await close_connection(cursor=cursor,con=conn)

async def get_all_booking(userId):
    conn,cursor = await create_connection()
    query = "select * from rideBooking where userId = %s"
    await cursor.execute(query,(userId))
    res = await cursor.fetchall()
    await close_connection(cursor=cursor,con=conn)
    return res
