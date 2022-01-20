class Metric:
  ''' A metric paired with the code used to evaluate it
  '''
  def __init__(self, props, func):
    self.id = props['@id']
    self.props = props
    self.func = func
  
  @staticmethod
  def create(props):
    def decorator(func):
      return Metric(props, func)
    return decorator

  def to_dict(self):
    return self.props

  def __call__(self, *args, **kwargs):
    return self.func(*args, **kwargs)

  def __str__(self):
    return self.props['name']
