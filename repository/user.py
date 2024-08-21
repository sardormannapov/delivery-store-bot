import psycopg2
from psycopg2 import extras

class UserRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log

    def create (self,req: dict) -> dict:
        query=f'''INSERT INTO users(full_name,chat_id,phone, set_language) VALUES(%s, %s, %s, %s)'''
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query,(
            req["full_name"],req["chat_id"],req["phone"],req["lang"]) )
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error(ex)
            return {
                "success": False
                }
        return {
            "success": True
            }

    def update (self,req: dict):
        query=f'''UPDATE users SET  full_name=%s,chat_id=%s ,phone=%s ,locations=%s, set_language=%s WHERE  chat_id=%s AND deleted_at IS NULL;'''
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query,(
            req["full_name"],req["chat_id"],req["phone"],req["location"],req["set_language"],req["id"]) )
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error(ex)
            return {
                "success": False
                }
        return {
            "id": id,
            "success": True
            }

    def update_location(self, req: dict):
        query = f'''UPDATE users SET  locations = array_append(locations,POINT(%s, %s)) WHERE  chat_id=%s AND deleted_at IS NULL'''
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, (
                req['long'], req['lat'], req['chat_id']
                ))

            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
            }
        return {
            "id": id,
            "success": True
        }
    def get_one (self,id):
        query=f'''SELECT id,full_name,chat_id,phone,locations, set_language from users WHERE deleted_at IS NULL AND chat_id=%s;'''
        connection=self.__conn
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(id,) )
            row=cursor.fetchone()
            res=dict()
            res['body']=dict( row )
            res["success"]=True
            cursor.close()
            connection.commit()
        except Exception as ex:
            connection.rollback()
            self.log.error( ex )
            return {
                "success": False
                }
        return res

    def get_list (self,offset,limit):
        connection=self.__conn
        query=f'''SELECT id,full_name,chat_id,phone,location, set_language from users WHERE deleted_at IS NULL LIMIT %s OFFSET %s;'''
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(limit,offset ))
            rows=cursor.fetchall()
            res=dict()
            res["success"]=True
            res["body"]=list()
            for row in rows:
                res["body"].append( dict( row ) )
                cursor.close()
            connection.commit()
        except Exception as ex:
            connection.rollback()
            return {
                "success": False
                }
        return res
    def update_languge(self, req: dict):
        query = f'''UPDATE users SET set_language=%s WHERE  chat_id=%s AND deleted_at IS NULL'''
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, (
                req['lang'], req['chat_id']
                ))
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
            }
        return {
            "id": id,
            "success": True
        }
