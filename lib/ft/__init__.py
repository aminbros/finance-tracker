
import sqlite3
import os.path
import json

ENV_PATH = None
ENV = {}
dbconn = None
__dir__ = os.path.dirname(__file__)

def set_env_path(path):
  global ENV_PATH
  ENV_PATH = path

def save_env():
  global ENV_PATH, ENV
  f = open(ENV_PATH, 'w')
  f.write(json.dumps(ENV, indent=2))
  f.close()

def load_env():
  global ENV_PATH, ENV
  try:
    f = open(ENV_PATH, 'r')
    ENV = json.load(f)
    f.close
  except IOError:
    pass

def load_config(configPath):
  try:
    f = open(configPath, 'r')
    config = json.load(f)
    config['__file__'] = configPath
    config['__dir__'] = os.path.dirname(configPath)
    return config
  except IOError:
    return None

def create_sqlite_database(conn):
  scriptpath = os.path.join(__dir__, "create_sqlite.sql")
  script = open(scriptpath, "r").read()
  cur = conn.cursor()
  cur.executescript(script)
  conn.commit()
  cur.close()
  

def init_sqlite_database(dbfn):
  if not os.path.isfile(dbfn):
    conn = sqlite3.connect(dbfn)
    create_sqlite_database(conn)
  conn = sqlite3.connect(dbfn)
  return conn


def init_ft(args, config):
  global dbconn
  assert config != None, "Could not locate config file!"
  try:
    dbconn = init_sqlite_database(os.path.join(config['__dir__'], 
                                               config['database']))
  except KeyError:
    raise AssertionError("database filename is not defined!")
  load_env()

