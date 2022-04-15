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
  
  @property
  def value(self):
    if self.answer.get('value') is not None:
      return f"{self.answer['value']*100:.2f}%"
    else:
      return f"NaN"

  @property
  def comment(self):
    if self.answer.get('comment') is not None and self.answer.get('numerator') is not None and self.answer.get('denominator') is not None:
      return f"{self.answer['comment']}: {self.answer['numerator']} / {self.answer['denominator']}"
    elif self.answer.get('comment') is not None:
      return f"{self.answer['comment']}"
    elif self.answer.get('numerator') is not None and self.answer.get('denominator') is not None:
      return f"{self.answer['numerator']} / {self.answer['denominator']}"
    else:
      return None
  
  def __str__(self):
    comment = self.comment
    if comment:
      return f"{self.value} ({comment})"
    else:
      return self.value
