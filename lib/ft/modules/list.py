
from . import *
import ft
import sqlitehelper
from time import time, ctime

def print_entries(entries):
  for entry in entries:
    print "%8.1f %3.1f %s %s %d" % (entry[1], entry[2], entry[0], \
                                    ctime(entry[3]), entry[4])

def print_reminder_entries(entries):
  for entry in entries:
    print "%8.1f %s %s %d" % (entry[1], entry[0], ctime(entry[2]), entry[3])

def list_reminder_entries(cat = None, limit = 10):
  cur = ft.dbconn.cursor()
  cat_t = None if cat is None else \
          sqlitehelper.Piece("ifnull(cat,'None')=?", cat)
  cond1 = sqlitehelper.cond("AND", cat_t)
  cur.execute("""SELECT name, amount, date, id FROM ft_reminder_entry 
                        %s order by `date` desc limit ?""" % \
                        (sqlitehelper.clause("WHERE", " ", cond1)), 
              sqlitehelper.execute_params( cond1, limit ))
  print_reminder_entries(cur.fetchall())
  cur.close()

def list_entries(cat = None, limit = 10):
  cur = ft.dbconn.cursor()
  cat_t = None if cat is None else \
          sqlitehelper.Piece("ifnull(cat,'None')=?", cat)
  cond1 = sqlitehelper.cond("AND", cat_t)
  cur.execute("""SELECT name, amount, weight, date, id FROM ft_entry 
                        %s order by `date` desc limit ?""" % \
                        (sqlitehelper.clause("WHERE", " ", cond1)), 
              sqlitehelper.execute_params( cond1, limit ))
  print_entries(cur.fetchall())
  cur.close()

commands = {"reminder": list_reminder_entries}
default_command = list_entries

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
