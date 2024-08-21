import psycopg2
from psycopg2 import extras

class CommentsRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log
    def Create(self, req: dict) -> dict:
        query = f'''INSERT INTO comments(
            user_id, comment, general_rate, food_rate
            ) VALUES(%s, %s, %s, %s)
            '''
        try:

            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (req.get("user_id"), req.get("comment"), req.get("general_rate"), req.get("food_rate")))
            row = cursor.fetchone()
            res = dict(row)
            res["success"] = True
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def GetList(self, offset, limit):
        query = f'''SELECT 
            id, user_id,
             comment, general_rate, food_rate 
            from comments ORDER BY id ASC LIMIT %s OFFSET %s;'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (limit,offset))

            rows = cursor.fetchall()
            res = dict()
            res["success"] = True
            res["body"] = list()
            
            for row in rows:
                res["body"].append(dict(row))
        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return res