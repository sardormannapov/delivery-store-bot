import psycopg2
from psycopg2 import extras
from psycopg2.extensions import register_adapter,AsIs

import json


class SubCategoryRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log

    def alter (self,req: dict) -> dict:
        connection=self.__conn
        query=f'''SELECT alter_subcatalog(%s,%s, %s, %s)'''
        category_name={
            "uz": req["uz"],
            "ru": req["ru"],
            "en": req["en"]
            }
        json_data=json.dumps( category_name )
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(req["id"],json_data,req["photo"],req["catalog_id"] ))
            res=dict()
            res["success"]=True
            res["body"]=[]
            # Commit the transaction to make the changes persistent

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
        query=f'''SELECT id, subcategory_name, photo, category_id from subcategories WHERE deleted_at IS NULL  ORDER BY id ASC LIMIT %s OFFSET %s;'''
        connection=self.__conn
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(limit,offset) )
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
            self.log.error( ex )
            return {
                "success": False
                }
        return res
    def get_list_by_category(self,offset,limit,catalog_id):
        query=f'''SELECT id, subcategory_name, photo, category_id from subcategories WHERE category_id = %s AND deleted_at IS NULL ORDER BY id ASC LIMIT %s OFFSET %s;'''
        try:
            cursor=self.__conn.cursor( cursor_factory = extras.RealDictCursor )
            cursor.execute( query,(catalog_id,limit,offset ,) )
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

    def delete(self,id):
        query=f'''UPDATE subcategories SET updated_at = NOW(), deleted_at = NOW()  WHERE deleted_at IS NULL AND id=%s'''
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query,(id,) )

            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
                }
        return {
            "success": True
            }
