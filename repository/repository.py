import pylogrus as pylogrus

import config.config as conf
import psycopg2
import repository.user as u
import repository.booking as b
import repository.comments as c
import repository.category as ca
import repository.product as p
import repository.order as o
import repository.migration as m
import repository.subcategory as sc
import repository.transaction as tr

import sys


class Repository:
    def __init__(self, cfg: conf.BotConfig, log: pylogrus.base.PyLogrus, migration_state) -> None:
        self.cfg = cfg
        self.log = log
        self.connection = None
        self.connection_db()
        self.user = u.UserRepo(self.connection,log)
        self.booking = b.BookingRepo(self.connection,log)
        self.comment = c.CommentsRepo(self.connection,log)
        self.category = ca.CategoryRepo(self.connection,log)
        self.subcategory = sc.SubCategoryRepo(self.connection,log)
        self.product = p.ProductRepo(self.connection,log)
        self.order = o.OrderRepo(self.connection,log)
        self.transaction = tr.TransactionRepo(self.connection,log)
        self.migration = m.Migration(self.connection, migration_state)

    def connection_db(self):
        try:
            self.connection = psycopg2.connect(
                host=self.cfg.db_host,
                user=self.cfg.db_user,
                password=self.cfg.db_password,
                database=self.cfg.db_name,
                port=int(self.cfg.db_port),
                sslmode='disable'
            )
        except Exception as ex:
            print(ex)
            sys.exit(1)
        finally:
            print("Successfully connected to database")

    def close_connection_db(self):
        try:
            self.connection.close()
        except Exception as ex:
            print(ex)
            sys.exit(1)
        finally:
            print("Close db-connection")
