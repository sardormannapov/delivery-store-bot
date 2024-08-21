import psycopg2
from psycopg2 import extras
import json


class OrderRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log
    def create(self, req: dict) -> dict:
        print(req)
        query = f'''INSERT INTO orders(user_id, transaction_id, products, amount, delivery_amount, total_amount, order_status, phone_number, payment_method, target_location, delivery_time) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, POINT(%s, %s), %s) RETURNING id'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (req["user_id"], req["transaction_id"], json.dumps(req["products"]), req["amount"], req["delivery_amount"], req["total_amount"], req["order_status"], req["phone_number"], req["payment_method"], req["target_location"]["long"], req["target_location"]["lat"], req["delivery_time"]))
            res=dict()
            row = cursor.fetchone()
            res["body"] = dict(id=row['id'])
            res["success"] = True
            # Commit the transaction to make the changes persistent
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success":False
            }
        return res

    def UpdateStatus(self, req: dict):
        query = f'''UPDATE orders SET order_status=%s where id=%s AND deleted_at IS NULL;
        '''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, (req["order_status"], req["id"]))

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

    def GetByStatus(self,status, offset, limit):
        query = f'''SELECT id, user_id,payment_method, products,amount,delivery_amount, total_amount,order_status, phone_number, json_object_agg(ST_X(target_location::geometry) as lat, ST_Y(target_location::geometry) as lng)
            from orders WHERE order_status=%s AND deleted_at IS NULL ORDER BY id DESC LIMIT %s OFFSET %s;'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (status, limit,offset))

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

    def GetByUserId(self,id, offset, limit):
        query = f'''SELECTid, user_id,payment_method, products,amount,delivery_amount, total_amount,order_status, phone_number, json_object_agg(ST_X(target_location::geometry) as lat, ST_Y(target_location::geometry) as lng)
            from orders WHERE user_id=%s AND deleted_at IS NULL ORDER BY id DESC LIMIT %s OFFSET %s;'''
        try:
            cursor = self.__conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (id, limit,offset)    )

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

    def GetList(self, offset, limit):
        query = f'''SELECT id, product_id, user_id, amount, phone_number, 
            is_delevery, payment_method, add_location, order_status
            from orders ORDER BY id DESC LIMIT %s OFFSET %s;'''
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

    def Delete(self, id):
        query = f'''Update orders SET deleted_at=NOW() ,updated_by=NOW() FROM orders WHERE id=%s and deleted_at IS NULL;'''

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
