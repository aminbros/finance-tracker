
from . import *
import ft
from time import time

def delete_entry(Id):
  try:
    amount = int(Id)
  except ValueError:
    raise AssertionError("Id is not an integer!")
  params = ( Id, )
  cur = ft.dbconn.cursor()
  cur.execute("""DELETE FROM ft_entry where id = ?""", params)
  ft.dbconn.commit()
  cur.close()

commands = {}
default_command = delete_entry

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
