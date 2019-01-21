import psycopg2
import psycopg2.extras as extra
from pprint import pprint
import os


class DatabaseConnection:
    def __init__(self):
        """Make a connection to the database"""
        try:
            if os.environ["APP_SETTINGS"] == "TESTING":
                self.con = psycopg2.connect(
                    database="ireporter_db", user="postgres", password="nadra2922", host="localhost", port="5432")
            else:
                self.con = psycopg2.connect(
                    database=os.environ["DATABASE_NAME"], user=os.environ["DATABASE_USER"], password=os.environ["DATABASE_PASSWORD"], host=os.environ["DATABASE_HOST"], port=os.environ["DATABASE_PORT"])
            self.con.autocommit = True
            self.dict_cursor = self.con.cursor(cursor_factory=extra.RealDictCursor)
        except Exception as ex:
            pprint("Database connection error: "+str(ex))

    def create_tables(self):
        """ create the tables"""
        create_tables = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY NOT NULL,
                firstname VARCHAR (40) NOT NULL,
                lastname VARCHAR (40) NOT NULL,
                othernames VARCHAR(40),
                email VARCHAR(60) UNIQUE NOT NULL,
                username VARCHAR (40) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phonenumber VARCHAR(14) UNIQUE NOT NULL,
                isAdmin VARCHAR (5) DEFAULT 'false',
                registered TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updatedOn TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
            """,

            """
            CREATE TABLE IF NOT EXISTS incidents (
				incident_id SERIAL PRIMARY KEY NOT NULL,
				createdBy INTEGER REFERENCES users(user_id),
				type VARCHAR(12) NOT NULL,
				status VARCHAR(13) DEFAULT 'drafted', 
				latitude VARCHAR(25) NOT NULL,
				longitude VARCHAR(25) NOT NULL,
				images VARCHAR(100)[],
				videos VARCHAR(100)[],
			    comment VARCHAR(255) NOT NULL,
				createdOn TIMESTAMP WITH TIME ZONE DEFAULT now(),
				updatedOn TIMESTAMP WITH TIME ZONE DEFAULT now()
				)
             """
            )

        for table in create_tables:
            self.dict_cursor.execute(table)
   

    def delete_tables(self):
        delete_queries = (
            """
            DROP TABLE IF EXISTS users CASCADE
            """,
            """
			DROP TABLE IF EXISTS incidents CASCADE
			""")
        for query in delete_queries:
            self.dict_cursor.execute(query)

