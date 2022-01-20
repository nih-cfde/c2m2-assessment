import math

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
    return f"{self.answer['value']*100:.2f}{'%' if not math.isnan(self.answer['value']) else ''} ({self.answer['comment']})"
