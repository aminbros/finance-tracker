
from . import *
import ft
from time import time

def retrieve_cat(cat = None):
  return (None if 'cat' not in ft.ENV else ft.ENV['cat']) if cat is None \
    else cat

def add_reminder_entry(name, amount, cat=None):
  try:
    amount = float(eval(amount, {}))
  except ValueError:
    raise AssertionError("amount is not a number!")
  entry = ( name, amount, int(time()), retrieve_cat(cat) )
  cur = ft.dbconn.cursor()
  cur.execute("""INSERT INTO ft_reminder_entry (name, amount, date, cat) 
                              VALUES (?, ?, ?, ?)""", entry)
  print "id: " + str(cur.lastrowid)
  ft.dbconn.commit()
  cur.close()
  

def add_entry(name, amount, weight="1", cat=None):
  try:
    amount = float(eval(amount, {}))
  except ValueError:
    raise AssertionError("amount is not a number!")
  try:
    weight = float(eval(weight, {}))
  except ValueError:
    raise AssertionError("weight is not a number!")
  entry = ( name, amount, weight, int(time()), retrieve_cat() )
  cur = ft.dbconn.cursor()
  cur.execute("""INSERT INTO ft_entry (name, amount, weight, date, cat) 
                              VALUES (?, ?, ?, ?, ?)""", entry)
  print "id: " + str(cur.lastrowid)
  ft.dbconn.commit()
  cur.close()

commands = { "reminder": add_reminder_entry }
default_command = add_entry

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
