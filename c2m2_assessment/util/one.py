def one(iterable):
  ''' Take one and only one value from an iterator
  '''
  iterator = iter(iterable)
  try:
    first = next(iterator)
    try:
      next(iterator)
    except StopIteration:
      return first
    else:
      raise Exception('Expected one, got multiple')
  except:
    raise Exception('Expected one, got none')
