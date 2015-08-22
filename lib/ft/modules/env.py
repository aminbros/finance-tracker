
from . import *
import ft

# getter and setter for ft envirnoment

def env_set(var_name, value):
  ft.ENV[var_name] = value
  ft.save_env()

def env_unset(var_name):
  del ft.ENV[var_name]
  ft.save_env()

def env_print(var_name=None):
  def print_var(name, value):
    print "%s = %s" % (name, value)
  if var_name == None:
    for name in ft.ENV:
      print_var(name, ft.ENV[name])
  else:
    try:
      print_var(var_name, ft.ENV[var_name])
    except KeyError:
      print "No such key!"

commands = { 'set': env_set, 'unset': env_unset }
default_command = env_print

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
