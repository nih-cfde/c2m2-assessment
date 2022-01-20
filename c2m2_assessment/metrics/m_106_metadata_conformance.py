import pandas as pd
from c2m2_assessment.fairshake.metric import Metric

@Metric.create({
  # standardized metadata format (107), machine readable metadata (106)
  # metadata license (117) (c2m2 ?)
  '@id': 106,
  'name': 'Metadata conformance',
  'description': 'The metadata properly conforms with the CFDE perscribed metadata model specification',
  'detail': '''The average metadata coverage of all tables''',
  'principle': 'Findable',
})
def metric(CFDE, full=False, **kwargs):
  def count_empty(val):
    ''' Attempt to catch some actual null values that aren't really null.
    '''
    return sum(
      1
      for v in val
      if v is not None and (
        type(v) != str or v.strip().lower() not in {
          '-', '-666', '', 'empty', 'n/a', 'na',
          'nan', 'nil', 'none', 'not defined', 'null',
          'undef', 'undefined',
        }
      )
    )
  coverage = pd.DataFrame(
    dict(
      table=table_name,
      coverage=count_empty(entity.values()) / len(table.column_definitions.keys()),
    )
    for table_name, table in CFDE.tables.items()
    for entity in table.entities()
  ).groupby('table')['coverage'].describe().fillna(0).sort_values('mean')
  value = coverage['mean'].mean()
  return {
    'value': value,
    'comment': f'See metadata coverage for more info',
    'supplement': coverage.to_dict(),
  }
