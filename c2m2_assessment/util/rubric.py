''' Object decorators for FAIRshake-style objects
'''

import traceback
import logging
logger = logging.getLogger(__name__)

class Answer:
  ''' An answer for a given metric evaluated against a target
  '''
  def __init__(self, target, metric, answer):
    self.target = target
    self.metric = metric
    self.answer = answer
  
  def to_dict(self):
    return dict(**self.answer, metric=self.metric.id)
  
  def __str__(self):
    return f"{self.answer['value']*100:.2f}% ({self.answer['comment']})"

class Metric:
  ''' A metric paired with the code used to evaluate it
  '''
  def __init__(self, props, func):
    self.id = props['@id']
    self.props = props
    self.func = func

  def to_dict(self):
    return self.props

  def __call__(self, *args, **kwargs):
    return self.func(*args, **kwargs)

  def __str__(self):
    return self.props['name']

class Rubric:
  ''' A rubric made up of a set of metrics, usage:
  ```python
  rubric = Rubric()

  @rubric.metric({
    "my": "metric_def"
  })
  def _(target):
    pass # My metric impl
  ```
  '''
  def __init__(self) -> None:
    self.metrics = {}

  def metric(self, props):
    ''' A decorator for instantiating and registering a metric for this rubric
    '''
    def decorator(func):
      metric = Metric(props, func)
      assert metric.id not in self.metrics, 'Duplicate metric id'
      self.metrics[metric.id] = metric
      return metric
    return decorator

  def assess(self, targets, metrics=None, **kwargs):
    ''' Assess the given targets against the entire rubric
    '''
    if metrics is None:
      metrics = self.metrics.values()
    for target in targets:
      logger.info(f"Target: {target}")
      for metric in metrics:
        logger.info(f"Metric: {metric}")
        try:
          answer = metric(target, **kwargs)
        except Exception as e:
          logger.error(traceback.format_exc())
          answer = {
            'value': float('nan'),
            'comment': f"An error occurred: {e}",
          }
        answer = Answer(target, metric, answer)
        logger.info(f"Answer: {answer}")
        yield answer
