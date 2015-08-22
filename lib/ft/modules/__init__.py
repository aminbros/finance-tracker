
from ft import *
import __future__
import inspect

__list = __future__.__builtins__["list"]

FT_INITIALIZED = False

def init_module(args, config):
  global FT_INITIALIZED
  if not FT_INITIALIZED:
      init_ft(args, config)
      FT_INITIALIZED = True

def eval_command_type_a(commands, default_command, args, config):
  def call_func(func, args):
    argsSpec = inspect.getargspec(func)
    min_alen = len(argsSpec.args) - \
          (0 if argsSpec.defaults == None else len(argsSpec.defaults))
    max_alen = len(argsSpec.args)
    try:
      opts = read_args_opt(args[min_alen:])
      assert len(args) >= min_alen, "Incorrect number of arguments!"
      arg_names = argsSpec.args[min_alen:]
      nargs = args[:min_alen] + ([] if argsSpec.defaults is None else \
                                            __list(argsSpec.defaults))
      for key in opts:
        try:
          nargs[arg_names.index(key) + min_alen] = opts[key]
        except ValueError:
          raise AssertionError("Unexpected option: %s!" % key)
      func(*nargs)
    except ValueError:
      assert len(args) >= min_alen and len(args) <= max_alen, \
                   "Incorrect number of arguments!"
      func(*args)
  try:
    func = commands[args[0]]
    call_func(func, args[1:])
  except (KeyError, IndexError):
    call_func(default_command, args)

def read_args_opt(args):
  i = 0
  l = len(args)
  ret = {}
  while i < l:
    arg = args[i]
    if arg.index("--") != 0:
      raise AssertionError("Argument option is expected but %s given" % arg)
    try:
      ret[arg[2:]] = args[i + 1]
    except IndexError:
      ret[arg[2:]] = True
    i += 2
  return ret

class RerunCommand(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
