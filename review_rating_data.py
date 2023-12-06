from database_connection import create_connection,close_connection

async def add_rating_and_review(userId,review,rating,name):
    conn,cursor = await create_connection()
    query = "Insert into ratingAndReview(userId, review, rating,name) values(%s,%s,%s,%s)"
    await cursor.execute(query,(userId,review,rating,name))
    await conn.commit()
    await close_connection(cursor=cursor,con=conn)


async def get_all_ratings_and_reviews(userId):
    conn,cursor = await create_connection()
    query = "select * from ratingAndReview where userId = %s"
    await cursor.execute(query,(userId))
    res = await cursor.fetchall()
    await close_connection(cursor=cursor,con=conn)
    return res
