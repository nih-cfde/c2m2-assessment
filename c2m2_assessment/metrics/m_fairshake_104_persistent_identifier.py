import pandas as pd
from c2m2_assessment.resolvers.CFDE_totals import (
  total_files,
)
from c2m2_assessment.fairshake.metric import Metric

@Metric.create({
  # Persistent identifier (105)
  '@id': 'fairshake:104',
  'name': 'Persistent identifier',
  'description': 'Globally unique, persistent, and valid identifiers (preferrably DOIs) are present for the dataset',
  'detail': '''We check that the persistent id that are present''',
  'principle': 'Findable',
})
def metric(CFDE, full=False, **kwargs):
  qualified_persistent_ids = pd.Series({
    (file['id_namespace'], file['local_id'], file.get('persistent_id')): 1 if file.get('persistent_id') else 0
    for file in CFDE.tables['file'].entities()
  }).sort_values()
  total_qualified_persistent_ids = float(qualified_persistent_ids.sum())
  value = (total_qualified_persistent_ids / total_files(CFDE)) if total_files(CFDE) else None
  return {
    'value': value,
    'numerator': total_qualified_persistent_ids,
    'denominator': total_files(CFDE),
    'supplement': qualified_persistent_ids.to_dict() if full else pd.concat([
      qualified_persistent_ids.head(5),
      qualified_persistent_ids.tail(5),
    ]).to_dict(),
  }
