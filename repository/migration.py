class Migration:
    def __init__ (self,connection,migration_state):
        self.__conn=connection
        self.__migration_state=migration_state
    def migration (self) -> bool:
        if  not self.migration_users() or not self.migration_payment()  or not self.migration_catalog() or not self.migration_sub_catalog() or not self.migration_booking() or not self.migration_comment() or not self.migration_product() or not self.migration_orders() or not self.alter_catalog_migration() or not self.alter_product_migration()  or not self.alter_subcatalog_migration() :
            return False
        else:
            return True
    def migration_users (self) -> bool:
        query_up='''
                        CREATE TABLE IF NOT EXISTS users (
                        id SERIAL  PRIMARY KEY  NOT NULL,
                        full_name TEXT NOT NULL,
                        chat_id BIGINT NOT NULL,
                        phone VARCHAR(13) NOT NULL,
                        locations POINT[] NULL,
                        set_language VARCHAR(2) NOT NULL CHECK(set_language='ru' or set_language='uz' or set_language='en'),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP NULL,
                        deleted_at TIMESTAMP NULL
                    );
                '''
        query_down='''
                DROP TABLE IF EXISTS users CASCADE
            '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor( )
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_catalog (self) -> bool:
        query_up='''
                        CREATE TABLE IF NOT EXISTS categories (
                        id SERIAL NOT NULL PRIMARY KEY,
                        category_name jsonb NOT NULL,
                        photo VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP NULL,
                        deleted_at TIMESTAMP NULL
                    );
                    ALTER TABLE categories ALTER COLUMN photo TYPE TEXT ,
                    ALTER COLUMN photo SET DEFAULT '';
                '''
        query_down='''
                DROP TABLE IF EXISTS categories CASCADE
            '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor( )
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_sub_catalog (self) -> bool:
        query_up='''
                        CREATE TABLE IF NOT EXISTS subcategories (
                        id SERIAL NOT NULL PRIMARY KEY,
                        subcategory_name jsonb NOT NULL,
                        photo VARCHAR(255) NOT NULL,
                        category_id INT NOT NULL REFERENCES categories(id),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP NULL,
                        deleted_at TIMESTAMP NULL
                    );
                '''
        query_down='''
                DROP TABLE IF EXISTS subcategories CASCADE
            '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor( )
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_booking (self) -> bool:
        query_up='''
                          CREATE TABLE IF NOT EXISTS bookings (
                            id SERIAL NOT NULL PRIMARY KEY,
                            user_id BIGINT NOT NULL REFERENCES users(id),
                            phone VARCHAR(13) NOT NULL,
                            user_name VARCHAR(255) NOT NULL,
                            nick_name VARCHAR(255) NOT NULL,
                            person_count INT NOT NULL CHECK(person_count >= 1),
                            booking_date VARCHAR(50) NOT NULL,
                            booking_time VARCHAR(50) NOT NULL,
                            booking_status VARCHAR(8) NOT NULL CHECK(booking_status=ANY (ARRAY['pending', 'canceled', 'accepted'])) DEFAULT 'pending',
                            created_at TIMESTAMP DEFAULT NOW(),
                            updated_at TIMESTAMP NULL,
                            deleted_at TIMESTAMP NULL
                        )
                  '''
        query_down='''
                  DROP TABLE IF EXISTS bookings CASCADE
              '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_comment (self) -> bool:
        query_up='''
                        CREATE TABLE IF NOT EXISTS comments (
                            id SERIAL NOT NULL PRIMARY KEY,
                            user_id BIGINT NOT NULL REFERENCES users(id),
                            comment TEXT NOT NULL,
                            general_rate INT NOT NULL CHECK(food_rate between 1 and 5),
                            food_rate INT NOT NULL CHECK(food_rate between 1 and 5),
                            created_at TIMESTAMP DEFAULT NOW(),
                            updated_at TIMESTAMP NULL,
                            deleted_at TIMESTAMP NULL
                        )
                  '''
        query_down='''
                  DROP TABLE IF EXISTS comments CASCADE
              '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_product (self) -> bool:
        query_up='''
                          CREATE TABLE IF NOT EXISTS products (
                            id SERIAL NOT NULL PRIMARY KEY,
                            product_name JSON NOT NULL, -- {"en":"product name"}
                            photo TEXT NOT NULL,
                            price INT NOT NULL,
                            special_sign JSON NOT NULL, -- {"en":"big"}
                            ingredients JSON NOT NULL,
                            transaction_id VARCHAR(255)  NULL,
                            subcategory_id BIGINT NOT NULL REFERENCES subcategories(id),
                            created_at TIMESTAMP DEFAULT NOW(),
                            updated_at TIMESTAMP NULL,
                            deleted_at TIMESTAMP NULL
                        )
                  '''
        query_down='''
                  DROP TABLE IF EXISTS products CASCADE
              '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def migration_orders (self) -> bool:
        query_up='''
                         CREATE TABLE IF NOT EXISTS orders (
                            id SERIAL NOT NULL PRIMARY KEY,
                            user_id BIGINT NOT NULL REFERENCES users(id),
                            transaction_id BIGINT  NULL,
                            products JSON NOT NULL , --{"products":[{"id":1,"title":"Lavash","count":7,"unit_price":49000}]}
                            amount INT NOT NULL CHECK(amount>0),
                            delivery_amount INT NOT NULL CHECK(delivery_amount>0),
                            total_amount INT NOT NULL CHECK(total_amount>0),
                            order_status VARCHAR(10) NOT NULL ,
                            phone_number VARCHAR(13) NOT NULL,
                            payment_method VARCHAR(6) NOT NULL ,
                            target_location POINT NOT NULL,
                            delivery_time VARCHAR(256) NOT NULL,
                            created_at TIMESTAMP DEFAULT NOW(),
                            updated_at TIMESTAMP NULL,
                            deleted_at TIMESTAMP NULL
                        )
                  '''
        query_down='''
                  DROP TABLE IF EXISTS orders CASCADE
              '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False

    def migration_payment (self) -> bool:

        query_up='''
                          CREATE TABLE IF NOT EXISTS transactions (
                            id SERIAL NOT NULL PRIMARY KEY,
                            account_id BIGINT NOT NULL REFERENCES users(id),
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            currency VARCHAR(10) NOT NULL,
                            amount BIGINT NOT NULL,
                            payment_system VARCHAR(10) NOT NULL ,
                            payment_status BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT NOW(),
                            updated_at TIMESTAMP NULL,
                            deleted_at TIMESTAMP NULL
                        )
                  '''
        query_down='''
                  DROP TABLE IF EXISTS payment CASCADE
              '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def alter_catalog_migration (self) -> bool:
        query_up='''
                              CREATE OR REPLACE  FUNCTION alter_catalog(catalog_id BIGINT,catalog_title jsonb,catalog_photo text ) RETURNS VOID LANGUAGE PLPGSQL AS
                                $$
                                  BEGIN
                                IF  EXISTS (SELECT id  FROM categories  WHERE id =catalog_id AND  deleted_at IS NULL)
                                THEN
                                UPDATE categories SET category_name=catalog_title,photo=catalog_photo,updated_at=NOW() WHERE id = catalog_id AND deleted_at IS NULL;
                                   ELSE
                                   INSERT INTO categories (category_name  , photo    ) VALUES (catalog_title  , catalog_photo  )  ;
                                   END IF;
                                  END
                                $$;
                      '''
        query_down='''
                      DROP FUNCTION IF EXISTS alter_catalog CASCADE
                  '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def alter_subcatalog_migration (self) -> bool:
        query_up='''
                              CREATE OR REPLACE  FUNCTION alter_subcatalog(subcatalog_id BIGINT,subcatalog_title jsonb,subcatalog_photo text,catalog_id BIGINT ) RETURNS VOID LANGUAGE PLPGSQL AS
                                $$
                                  BEGIN
                                IF  EXISTS (SELECT id  FROM subcategories  WHERE id =subcatalog_id  AND  deleted_at IS NULL)
                                THEN
                                UPDATE subcategories SET subcategory_name=subcatalog_title,photo=subcatalog_photo,category_id = catalog_id,updated_at=NOW() WHERE id = subcatalog_id AND deleted_at IS NULL;
                                   ELSE
                                   INSERT INTO subcategories (subcategory_name  , photo  , category_id  ) VALUES (subcatalog_title  , subcatalog_photo, catalog_id  )  ;
                                   END IF;
                                  END
                                $$;
                      '''
        query_down='''
                      DROP FUNCTION IF EXISTS alter_subcatalog CASCADE
                  '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False
    def alter_product_migration (self) -> bool:
        query_up='''
                      CREATE OR REPLACE FUNCTION alter_product(product_id BIGINT,product_title jsonb,product_photo text,product_price INT,product_ingredients json,subcatalog_id BIGINT,product_special_sign json ) RETURNS VOID LANGUAGE PLPGSQL AS
                        $$
                          BEGIN
                        IF  EXISTS (SELECT id  FROM products  WHERE id =product_id  AND deleted_at IS NULL)
                        THEN
                        UPDATE products SET product_name=product_title,photo=product_photo,price=product_price,ingredients=product_ingredients,subcategory_id=subcatalog_id,special_sign=product_special_sign, updated_at=NOW() WHERE id = product_id AND deleted_at IS NULL;
                           ELSE
                           INSERT INTO products (product_name, photo, price, ingredients,special_sign, subcategory_id    ) VALUES (product_title  , product_photo  , product_price  , product_ingredients  ,product_special_sign , subcatalog_id  )  ;
                           END IF;
                          END
                        $$;
                      '''
        query_down=''' 
                      DROP FUNCTION IF EXISTS alter_product CASCADE
                  '''
        query=query_up
        if not self.__migration_state:
            query=query_down
        try:
            cursor=self.__conn.cursor()
            cursor.execute( query )
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as ex:
            print( ex )
            return False

    # def alter_user_chat_id(self) -> bool:
    #     query_up = ''' ALTER TABLE users ALTER COLUMN chat_id TYPE BIGINT '''
    #     query_down = '''  '''
    #     query = query_up
    #     if not self.__migration_state:
    #         query = query_down
    #     try:
    #         cursor = self.__conn.cursor()
    #         cursor.execute(query)
    #         self.__conn.commit()
    #         cursor.close()
    #         return True
    #     except Exception as ex:
    #         print(ex)
    #         return False