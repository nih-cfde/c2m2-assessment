_memo = {}
def memo(cb):
  ''' Ensure a function is memoised, assuming purity and hash uniqueness
  '''
  import functools
  global _memo
  _memo[cb] = {}
  @functools.wraps(cb)
  def wrapper(*args):
    global _memo
    _h = hash(tuple(id(arg) for arg in args))
    if _h not in _memo[cb]:
      _memo[cb][_h] = cb(*args)
    return _memo[cb][_h]
  return wrapper
