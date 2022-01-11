import click
import logging
from pathlib import Path

def assess(CFDE):
  ''' Given a CFDE client, perform the assessment and return a table of results
  '''
  import pandas as pd
  from c2m2_assessment.rubric import rubric
  return pd.merge(
    left=pd.DataFrame.from_records([
      answer.to_dict()
      for answer in rubric.assess([CFDE])
    ]),
    left_on='metric',
    right=pd.DataFrame.from_records([
      metric.to_dict()
      for metric in rubric.metrics.values()
    ]).set_index('@id'),
    right_index=True,
  )

#%%
@click.command(name='assess')
@click.option('-i', '--input', type=click.Path(file_okay=True, path_type=Path), required=True, help='Input datapackage')
@click.option('-o', '--output', type=click.File(mode='w'), default='-', help='Output results')
@click.option('-w', '--work', type=click.Path(), help='Working directory')
@click.option('-v', '--verbose', count=True, help='Increase logging level')
def cli(input=None, output=None, work=None, verbose=0):
  ''' Command line interface to assessment, auto-extract zip files, instantiate CFDE client & perform assessment
  '''
  from c2m2_assessment.util.one import one
  from c2m2_assessment.util.workdir import workdir
  logging.basicConfig(level=max(0, 40 - (1+verbose)*10))
  with workdir(work) as work:
    if input.suffix == '.zip':
      import zipfile
      with zipfile.ZipFile(input, 'r') as zf:
        zf.extractall(work)
      input = one(
        f
        for f in work.glob('**/*datapackage.json')
        # ignore hidden file or directory
        if not any(
          part.startswith('.')
          for part in f.parts
        )
      )
    assert input.suffix == '.json', f'Invalid input, expected .json or .zip, got {input.suffix}'
    from deriva_datapackage import create_offline_client
    CFDE = create_offline_client(str(input), cachedir=str(work))
    assess(CFDE).to_json(output, orient='records')

if __name__ == '__main__':
  cli()
