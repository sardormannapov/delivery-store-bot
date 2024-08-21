from psycopg2 import extras
import json


class CategoryRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log

    def alter(self, req: dict) -> dict:
        query = f'''SELECT alter_catalog(%s,%s, %s)
            '''
        category_name = {
            "uz":req["uz"],
            "ru":req["ru"],
            "en":req["en"]
        }
        json_data = json.dumps(category_name)
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (req["id"],json_data, req["photo"]))
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

    def get_list(self, offset, limit, lang):
        query = f'''SELECT id, category_name, photo from categories WHERE deleted_at IS NULL ORDER BY id ASC  LIMIT %s OFFSET %s;'''

        if lang =='uz':
            query = '''SELECT id, category_name, photo, created_at, updated_at, deleted_at FROM public.categories where deleted_at is null order by category_name ->> 'uz'::text asc ;'''

        elif lang =='ru':
            query = '''SELECT id, category_name, photo, created_at, updated_at, deleted_at FROM public.categories where deleted_at is null order by category_name ->> 'ru'::text asc ;'''

        elif lang =='en':
            query = '''SELECT id, category_name, photo, created_at, updated_at, deleted_at FROM public.categories where deleted_at is null order by category_name ->> 'en'::text asc ;'''

        connection= self.__conn
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (limit,offset))
            rows = cursor.fetchall()
            res = dict()
            res["success"] = True
            res["body"] = []
            for row in rows:
                res["body"].append(dict(row))
            cursor.close()
            connection.commit()
        except Exception as ex:
            connection.rollback()
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def delete(self, id):
        query = f'''UPDATE categories SET updated_at = NOW(), deleted_at = NOW()  WHERE id=%s AND deleted_at IS NULL;'''
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, (id))
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return {
            "success":True
        }

    def get_list_without_lang(self, offset, limit):
        query = f'''SELECT id, category_name, photo from categories WHERE deleted_at IS NULL ORDER BY id ASC  LIMIT %s OFFSET %s;'''
        connection= self.__conn
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (limit,offset))
            rows = cursor.fetchall()
            res = dict()
            res["success"] = True
            res["body"] = []
            for row in rows:
                res["body"].append(dict(row))
            cursor.close()
            connection.commit()
        except Exception as ex:
            connection.rollback()
            self.log.error( ex )
            return {
                "success":False
            }
        return res

