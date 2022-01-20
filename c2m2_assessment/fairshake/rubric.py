''' Object decorators for FAIRshake-style objects
'''
from c2m2_assessment.fairshake.metric import Metric
from c2m2_assessment.fairshake.answer import Answer

import traceback
import logging
logger = logging.getLogger(__name__)

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
    if isinstance(props, str):
      import importlib
      modpath, modimport = props.rsplit('.', maxsplit=1)
      metric = getattr(importlib.import_module(modpath), modimport, None)
      assert isinstance(metric, Metric)
      self.metrics[metric.id] = metric
      return metric
    elif isinstance(props, Metric):
      metric = props
      self.metrics[metric.id] = metric
      return metric
    else:
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
