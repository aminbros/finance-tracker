

def print_array_table(table):
  colsCLen = array_table_cols_len(table)
  for row in table:
    for ci in range(len(row)):
      col = str(row[ci])
      print(col + repeat_str(" ", colsCLen[ci] - len(col)))
    print "" # new line

def array_table_cols_len(table):
  colsCLen = []
  for row in table:
    for ci in range(len(row)):
      col = row[ci]
      try:
        colsCLen[ci] = max(colsCLen[ci], len(line))
      except IndexError:
        colsCLen.append(len(line))
  return colsCLen

def repeat_str(s, l):
  r = ""
  for i in range(l):
    r += s
  return r


def log_2dem_array(table):
  for ri in range(len(table)):
    row = table[ri]
    print "row:", str(ri)
    for ci in row if type(row) is dict else range(len(row)):
      col = str(row[ci])
      print repeat_str(" ", 2), "col:", str(ci)
      for line in col.split("\n"):
        print repeat_str(" ", 4), line
