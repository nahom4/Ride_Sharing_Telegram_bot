from database_connection import create_connection,close_connection
from User import User

async def add_user(user : User):
    conn,cursor = await create_connection()
    print(user.name,"Helloooooooooooooooooooooooooooo")
    query = "Insert into botUsers(userId, name, role) values(%s,%s,%s)"
    await cursor.execute(query,(user.userId,user.name,user.role))
    await conn.commit()
    await close_connection(cursor=cursor,con=conn)


async def get_name(userId):
    conn,cursor = await create_connection()
    query = "select name from botUsers where userId = %s;"
    await cursor.execute(query,(userId))
    res = await cursor.fetchall()
    await close_connection(cursor=cursor,con=conn)
    return res[0]

async def update_user_name(userId,name):
    conn,cursor = await create_connection()
    query = "UPDATE botUsers SET Name = %s WHERE userId = %s"
    await cursor.execute(query,(name,userId))
    await conn.commit()
    await close_connection(cursor=cursor,con=conn)