import psycopg2
import psycopg2.errors as error
import psycopg2.extras as extras

import sys
from common.config import service_config

# Define the running environment
# running_environment_file = 'environments/' + sys.argv[1] + '.yml'
running_environment_file = 'environments/running.yml'

# Read yaml file
# global running_config
running_config = service_config(running_environment_file)


def get_db_connect():
    _db_connect = psycopg2.connect(
        host=running_config['postgresql']['host'],
        database=running_config['postgresql']['database'],
        port = running_config['postgresql']['port'],
        user=running_config['postgresql']['username'],
        password=running_config['postgresql']['password']
    )
    return _db_connect

def insert_cur(sql, table, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute("INSERT INTO {0}({1})VALUES({2})".format(table, sql[0], sql[1]))
        db_connect.commit()
        db_cur.close()
        db_connect.close()
        return "Added"
    except Exception as e:
        print(e)
        return "Error"


def insert_cur_v2(sql, table, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute("INSERT INTO {0}({1}) VALUES({2})".format(table, sql[0], sql[1]))
        db_connect.commit()
        db_cur.close()
        db_connect.close()
        return {
            'rc': 200,
            'cur_result': 'successful'
        }
    except Exception as e:
        return {
            'rc': 500,
            'cur_result': e
        }


def insert_cur_row(sql, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute(sql)
        db_connect.commit()
        db_cur.close()
        db_connect.close()
        return "Added"
    except error.UniqueViolation as e:
        return str(e)
    except error.ForeignKeyViolation as e:
        return str(e)


'''
insert_cur_cert_manager - dedicated for cert_manager module
'''


def insert_cur_cert_manager(values, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute("""INSERT INTO ssl_certificates("common_name", "certificates") VALUES (%s, %s)""",values)
        db_connect.commit()
        db_cur.close()
        db_connect.close()
        # print("Added: ", values)
    except Exception as e:
        return e


# def delete_cur(sql, table):
#     pass
#
#
def select_cur(sql, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute(sql)
        results = db_cur.fetchall()
        db_cur.close()
        db_connect.close()
        return results
    except Exception as e:
        return e


def dict_select_cur(sql, db_connect):
    try:
        db_cur = db_connect.cursor(cursor_factory=extras.RealDictCursor)
        db_cur.execute(sql)
        results = db_cur.fetchone()
        db_cur.close()
        db_connect.close()
        return results
    except Exception as e:
        return e


def update_cur(sql, db_connect):
    try:
        db_cur = db_connect.cursor()
        db_cur.execute(sql)
        db_connect.commit()
        db_cur.close()
        db_connect.close()
        return "Updated"
    except error.UniqueViolation as e:
        return str(e)
