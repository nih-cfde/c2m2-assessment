def one(it):
  ''' Take one and only one value from an iterator
  '''
  it = iter(it)
  first = next(it)
  try:
    next(it)
  except StopIteration:
    return first
  else:
    raise Exception('Expected one, got multiple')
