
from . import *
import ft
from time import time, ctime
from sqlitehelper import *

def balance_for_entry_x(colname, value, for_last=None):
  cur = ft.dbconn.cursor()
  date = None
  if for_last != None:
    try:
      for_last = int(eval(for_last, {}))
      date = ( " and ", "date > ?", time() - for_last * 24 * 3600)
    except TypeError:
      raise AssertionError("for_last option should be a number")
  cur.execute(add_to_stmt_str("""SELECT sum(amount), sum(weight) 
                                  FROM ft_entry where """, \
                              "ifnull(%s,'None')=?" % colname, date), 
              add_to_stmt_args( (value,), date))
  row = cur.fetchone()
  print "balance:", str(0 if row[0] is None else row[0])
  print "total weight:", str(0 if row[0] is None else row[1])
  cur.close()

def balance_for_reminder_entry_x(name, value):
  cur = ft.dbconn.cursor()
  cur.execute("SELECT sum(amount) FROM ft_entry where "+
              "ifnull(%s,'None')=?" % name, (value,))
  row = cur.fetchone()
  amount = 0 if row[0] is None else row[0]
  cur.execute("SELECT sum(amount) FROM ft_reminder_entry where "+
              "ifnull(%s,'None')=?" % name, \
              (value,))
  row = cur.fetchone()
  reminder_amount = 0 if row[0] is None else row[0]
  print "reminder balance:", str(reminder_amount + amount)
  cur.close()

def balance_for_entry_cat(cat, for_last=None):
  balance_for_entry_x("cat", cat, for_last)

def balance_for_entry_name(name=None, for_last=None):
  if name is None:
    raise RerunCommand(({}, balance_sum))
  balance_for_entry_x("name", name, for_last)

def balance_sum(for_last=None):
  cur = ft.dbconn.cursor()
  date = None
  if for_last != None:
    try:
      for_last = int(eval(for_last, {}))
      date = ( " and ", "date > ?", time() - for_last * 24 * 3600)
    except TypeError:
      raise AssertionError("for_last option should be a number")
  cur.execute(add_to_stmt_str(
    """SELECT sum(amount), 
          sum(CASE WHEN amount > 0 THEN amount ELSE 0 END) as amount_in,
          sum(CASE WHEN amount < 0 THEN amount ELSE 0 END) as amount_out
       FROM ft_entry %s""" % ("" if date is None else "where "), date), 
              add_to_stmt_args( (), date))
  row = cur.fetchone()
  print "balance:", str(0 if row[0] is None else row[0])
  print "in: ", str(0 if row[1] is None else row[1])
  print "out: ", str(0 if row[2] is None else row[2] * -1)
  cur.close()

def balance_reminder_for_name(name):
  balance_for_reminder_entry_x("name", name)

def balance_reminder_for_cat(cat):
  balance_for_reminder_entry_x("cat", cat)


commands = { "cat": balance_for_entry_cat, \
             "reminder": balance_reminder_for_name, \
             "reminder-cat": balance_reminder_for_cat}
default_command = balance_for_entry_name

def main(args, config):
  init_module(args, config)
  cmds = commands
  df_cmd = default_command
  while True:
    try:
      eval_command_type_a(cmds, df_cmd, args, config)
      break
    except RerunCommand as exp:
      cmds = exp.value[0]
      df_cmd = exp.value[1]
