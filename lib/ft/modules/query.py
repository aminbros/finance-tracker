
from . import *
import ft
import cli
import sqlitehelper
from time import time
import sqlite3

def sqlite_query(args):
  query = " ".join(args)
  try:
    cur = ft.dbconn.cursor()
    cur.execute(query)
    try:
      table = sqlitehelper.cursor_fetch_all_dict(cur)
    except:
      table = cur.fetchall()
    if table != None:
      cli.log_2dem_array(table)
    if cur.rowcount > 0:
      print "affected rows: %d" % cur.rowcount
    if cur.lastrowid != None:
      print "lastrowid: " + str(cur.lastrowid)
    ft.dbconn.commit()
    cur.close()
  except sqlite3.Error as e:
    raise AssertionError(e.args[0])

commands = {}
default_command = sqlite_query

def main(args, config):
  init_module(args, config)
  sqlite_query(args)
