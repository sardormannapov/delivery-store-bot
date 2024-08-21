import psycopg2
from psycopg2 import extras

class BookingRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log
    def create(self, req: dict) -> dict:
        query = f'''INSERT INTO bookings(
            user_id,
            phone,
            user_name,
            nick_name,
            person_count,
            booking_date,
            booking_time
            ) VALUES(%s, %s, %s, %s, %s, %s ,%s)
            '''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (req.get("user_id"), req.get("phone"),req.get("user_name"), req.get("nick_name"), req.get("person_count"),
            req.get("booking_date"), req.get("booking_time")))
            res=dict()
            res["success"] = True
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def update_status(self, id, new_status):
        query = f'''UPDATE bookings SET booking_status=%s WHERE id=%s
        returning
            id,           user_id,
            phone,        person_count,
            booking_date, from_time,
            to_time, booking_status'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (new_status, id))
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

    def get_list(self, offset, limit):
        query = f'''SELECT
            id,           user_id,
            phone,        person_count,
            booking_date, from_time,
            to_time, booking_status
            from bookings ORDER BY id desc LIMIT %s OFFSET %s;'''
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