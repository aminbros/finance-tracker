
def cursor_fetch_all_dict(cur):
    cols = map(lambda a: a[0], cur.description)
    table = []
    row = cur.fetchone()
    while row is not None:
      rowD = {}
      for ci in range(len(cols)):
        col = cols[ci]
        rowD[col] = row[ci]
      table.append(rowD)
      row = cur.fetchone()
    return table


def add_to_stmt_str(stmt, *a):
  ql = 0
  for i in range(len(a)):
    item = a[i]
    if item is not None:
      if type(item) is str:
        stmt = stmt + " " + item
      else:
        stmt = stmt + " " + ("" if ql == 0 else item[0]) + item[1]
      ql += 1
  return stmt

def add_to_stmt_args(args, *a):
  args = list(args)
  for item in a:
    if item is not None:
      if type(item) is not tuple and type(item) is not list:
        args.append(item)
      else:
        args.append(item[2])
  return tuple(args)

def clause(clause_id, sep, *pieces):
  pieces = filter_pieces(pieces)
  if len(pieces) == 0:
    return ""
  return clause_id + " " + sep.join(map(lambda p: p.pquery, pieces))

def cond(lop, *pieces):
  pieces = filter_pieces(pieces)
  if len(pieces) == 0:
    return None
  return Piece("(" + (" "+lop+" ").join(map(lambda p: p.pquery, pieces)) + ")",
               sum(map(lambda p: [] if p.params is None else \
                       list(p.params), pieces), []))

def filter_pieces(pieces):
  npieces = []
  for piece in pieces:
    if piece is not None:
      npieces.append(piece)
  return npieces

def execute_params(*paramss):
  nparams = []
  for params in paramss:
    if params is not None:
      if isinstance(params, Piece):
        # params is a Piece
        params = [] if params.params is None else list(params.params)
        nparams = nparams + params
      else:
        nparams.append(params)
  return nparams

class Piece(object):
  """ Piece class contains a piece of execution 
  namely query piece and optional parameters """
  def __init__(self, pquery, params=None):
    self.pquery = pquery
    if params is not None and \
       type(params) is not list and type(params) is not tuple:
      params = [params]
    self.params = params

  def __str__(self):
    return self.pquery


def init_edit_dict(entries):
  def parse_string(entry):
    return entry['value']
  def parse_number(entry):
    try:
      value = entry["value"]
      if value is not None:
        value = float(value)
      return value
    except ValueError:
      raise AssertionError("%s is not a number!" % name)
  type_parser = {"string": parse_string, "number": parse_number }
  edit_dict = {}
  for entry in entries:
    try:
      v = type_parser[entry["type"]](entry)
      if v is not None:
        edit_dict[entry['name']] = v
    except KeyError:
      raise Exception("Unkown type!")
  return edit_dict

def query_update_table(dbconn, tablename, edit_dict, where_cond):
  cur = dbconn.cursor()
  edit_pieces = []
  for key in edit_dict:
    edit_pieces.append(Piece(key+"=?", edit_dict[key]))
  if len(edit_pieces) == 0:
    return
  cur.execute("UPDATE %s %s %s" % 
              (tablename, clause("SET", ",", *edit_pieces), 
               clause("WHERE", " ", where_cond)), 
              execute_params(*(edit_pieces + [where_cond])))
  dbconn.commit()
  cur.close()
