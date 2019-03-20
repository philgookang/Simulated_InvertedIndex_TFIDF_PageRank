import pymysql.cursors
import json
import sys
import time

class Database:

    # postan singleton
    singleton = None

    # mysql connection
    mysqlConnection = None

    # mysql cursor
    mysqlCursor = None

    # connection start time
    connection_start = None

    @staticmethod
    def init():

        if Database.singleton == None:

            # create new object
            Database.singleton = Database()

            # create new connection
            Database.singleton.connect()

        return Database.singleton

    def connect(self):

        # get database config
        config = self.get_config()

        # connection to database
        self.mysqlConnection = pymysql.connect(user=config["user"], password=config["password"], host=config["host"], port=config["port"], database="ADB2018_22788", charset="utf8mb4")

        # makes life easy
        self.mysqlConnection.autocommit = True

        # create cusor
        self.mysqlCursor = self.mysqlConnection.cursor(pymysql.cursors.DictCursor)

        # set names
        self.mysqlCursor.execute("SET NAMES utf8mb4 ")

        # save the connection start time
        self.connection_start = time.time()

    def get_config(self):

        try:
            # load config file
            config = open("./database.config")

            # decode to json
            return json.load(config)

        except FileNotFoundError:
            sys.exit("[Error] Cannot find database config file")

    def check_connection_time(self):

        # get current time
        current_time = time.time()

        # subtract save time
        result = current_time - self.connection_start

        # check if time diff is larger than 5 minutes
        if result >= 20:

            try:
                # clean up cursor
                self.mysqlCursor.close()

                # clean up mysql
                self.mysqlConnection.close()
            except:
                pass

            # re connect
            self.connect()

    def close(self):

        # clean up cursor
        self.mysqlCursor.close()

        # clean up mysql
        self.mysqlConnection.close()

        # clear variable
        self.mysqlCursor = None
        self.mysqlConnection = None

    def execute(self, sql, params=[], show_sql=False):

        # check if connection time has been too long
        self.check_connection_time()

        try:

            # execute sql
            self.mysqlCursor.execute(sql, tuple(params))

        except TypeError as error:
            print("[MYSQL SQL] ", error, sql, params)
        except pymysql.err.ProgrammingError as error:
            code, message = error.args
            print("[MYSQL SQL] ", code, message)
        except pymysql.InternalError as error:
            code, message = error.args
            print("[MYSQL ERROR] ", code, message)

        if show_sql:
            print(self.mysqlCursor.statement)

        # apply transaction to database
        self.mysqlConnection.commit()

        return self.mysqlCursor

    def create(self, sql, params=[], show_sql=False):

        result = self.execute(sql, params, show_sql)
        return result.lastrowid

    def get(self, sql, params=[], show_sql=False):

        result = self.execute(sql, params, show_sql)

        for row in result:
            return row

        return { }

    def getList(self, sql, params=[], show_sql=False):

        result = self.execute(sql, params, show_sql)

        # return list
        list = []

        # loop through result
        for item in result:
            list.append(item)

        return list

    def __del__(self):

        if not self.mysqlCursor:
            return

        if not self.mysqlConnection:
            return

        try:

            # clean up cursor
            self.mysqlCursor.close()

            # clean up mysql
            self.mysqlConnection.close()

        except (ReferenceError, TypeError):
            pass

    def __exit__(self, exc_type, exc_value, traceback):

        # clean up cursor
        self.mysqlCursor.close()

        # clean up mysql
        self.mysqlConnection.close()