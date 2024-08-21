import psycopg2
from psycopg2 import extras
import json

class ProductRepo:

    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log

    def alter(self, req: dict) -> dict:
        connection = self.__conn
        query = f'''SELECT alter_product(%s,%s,%s,%s,%s,%s,%s)'''
        product_name_json = json.dumps({
            "uz":req["title_uz"],
            "ru":req["title_ru"],
            "en":req["title_en"],
        })
        ingredients_json = json.dumps({
            "uz":req["ingredient_uz"],
            "ru":req["ingredient_ru"],
            "en":req["ingredient_en"],
        })
        speacial_sign_json = json.dumps({
            "uz":req["special_sign_uz"],
            "ru":req["special_sign_ru"],
            "en":req["special_sign_en"],
        })
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (req["id"],product_name_json, req["photo"],req["price"], ingredients_json, req["subcatalog_id"],speacial_sign_json))
            res= dict()
            res["success"] = True
            # Commit the transaction to make the changes persistent
            cursor.close()
            connection.commit()
        except Exception as ex:
            connection.rollback()
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def get_list (self,offset,limit):
        query=f'''SELECT  id, product_name, photo, price, ingredients,special_sign, subcategory_id from products WHERE deleted_at IS NULL ORDER BY id ASC LIMIT %s OFFSET %s;'''
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(limit,offset ))
            rows=cursor.fetchall()
            res=dict()
            res["success"]=True
            res["body"]=list()
            for row in rows:
                res["body"].append( dict( row ) )
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
                }
        return res

    def get_list_by_subcategory (self,offset,limit,subcatalog_id):
        query=f'''SELECT  id, product_name, photo, price, ingredients,special_sign, subcategory_id from products WHERE subcategory_id=%s AND deleted_at IS NULL ORDER BY id ASC LIMIT %s OFFSET %s;'''
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(subcatalog_id,limit,offset ))
            rows=cursor.fetchall()
            res=dict()
            res["success"]=True
            res["body"]=list()

            for row in rows:
                res["body"].append( dict( row ) )
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
                }
        return res

    def get_list_by_id(self,category_id, offset, limit):
        query = f'''SELECT  id, product_name, photo, price, ingredients,special_sign, subcategory_id from products WHERE category_id=%s AND deleted_at IS NULL ORDER BY id DESC LIMIT %s OFFSET %s;'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (category_id,limit,offset))

            row = cursor.fetchone()
            res = dict()
            res["success"] = True
            res["body"] = dict(row)

        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def delete(self, id):
        query = f'''UPDATE  products SET updated_at = NOW(), deleted_at = NOW() WHERE id=%s AND deleted_at IS NULL;'''

        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, (id,))
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
