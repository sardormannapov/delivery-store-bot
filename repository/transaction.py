import psycopg2
from psycopg2 import extras


class TransactionRepo:
    def __init__ (self,connection,log):
        self.__conn=connection
        self.log=log
    def create (self,req: dict) -> dict:
        query=f'''INSERT INTO transactions(account_id,title,description,currency,amount,payment_system) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id'''
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query,(
                req["id"],req["title"],req["description"],req["currency"],req["amount"],req["payment_system"]) )
            row=cursor.fetchone()
            res=dict()
            res['body']=dict( id = row )
            res["success"]=True
            self.__conn.commit()
        except Exception as ex:
            self.log.error( ex )
            return {
                "success": False
                }
        return res
    def update_transaction_status (self,req: dict):
        query=f'''UPDATE transactions SET payment_status=TRUE WHERE  id=%s AND deleted_at IS NULL RETURNING payment_system, amount;'''
        try:
            cursor=self.__conn.cursor()
            row=cursor.execute( query,(req["id"]) )
            res=dict()
            data=row.fetchone()
            res['body'] = dict(data)
            res["success"]=True
            self.__conn.commit()
        except Exception as ex:
            self.log.error(ex)
            return {
                "success": False
                }
        return res