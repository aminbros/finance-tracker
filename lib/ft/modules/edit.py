
from . import *
import ft
from sqlitehelper import *
from time import time

def edit_reminder_entry(Id, name=None, amount=None, cat=None):
  edit_dict = init_edit_dict([
    {
      "name": "name",
      "value": name,
      "type": "string"
    },
    {
      "name": "cat",
      "value": cat,
      "type": "string"
    },
    {
      "name": "amount",
      "value": None if amount is None else eval(amount),
      "type": "number"
    }
  ])
  query_update_table(ft.dbconn, "ft_reminder_entry", edit_dict, 
                     cond("AND", Piece("id=?", Id)))

def edit_entry(Id, name=None, amount=None, weight=None, cat=None):
  edit_dict = init_edit_dict([
    {
      "name": "name",
      "value": name,
      "type": "string"
    },
    {
      "name": "cat",
      "value": cat,
      "type": "string"
    },
    {
      "name": "amount",
      "value": None if amount is None else eval(amount),
      "type": "number"
    },
    {
      "name": "weight",
      "value": None if weight is None else eval(weight),
      "type": "number"
    },
  ])
  query_update_table(ft.dbconn, "ft_entry", edit_dict, 
                     cond("AND", Piece("id=?", Id)))

commands = {"reminder": edit_reminder_entry}
default_command = edit_entry

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
