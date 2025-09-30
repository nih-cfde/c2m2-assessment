import pandas as pd
import urllib.parse
import traceback
import requests
import logging
from c2m2_assessment.resolvers.CFDE_totals import (
  total_files,
)
from c2m2_assessment.fairshake.metric import Metric

def try_parse_url(url):
  if not url: return
  try:
    try: return urllib.parse.urlparse(url)
    except Exception as e:
      raise AssertionError(f"Failed to parse URI") from e
  except:
    logging.debug(traceback.format_exc())

def valid_drs_format(access_url_parsed):
  try:
    assert access_url_parsed.scheme == 'drs'
    assert access_url_parsed.hostname, "Expected hostname"
    assert access_url_parsed.path.count('/') == 1, f"Expected opaque id, received path {access_url_parsed.path[1:]}"
  except:
    logging.debug(traceback.format_exc())
    return False
  return True

def test_http(access_url):
  try:
    req = requests.head(access_url)
    req.raise_for_status()
  except:
    logging.warning(traceback.format_exc())
    return False
  return True

def test_drs(access_url_parsed):
  try:
    req = requests.get(f"https://{access_url_parsed.hostname}/ga4gh/drs/v1/objects/{access_url_parsed.path[1:]}")
    req.raise_for_status()
    res = req.json()
    # there should be at least one typed access methods
    assert res['access_methods'][0]['type']
    # the access method minimally needs access_id or access_url
    assert res['access_methods'][0].keys() & {'access_id', 'access_url'}
    # TODO: deeper DRS test (?)
  except:
    logging.warning(traceback.format_exc())
    return False
  return True

def test_access_url(row):
  if row['parsed'].scheme in {'http', 'https'}: return test_http(row['access_url'])
  elif row['parsed'].scheme == 'drs': return test_drs(row['parsed'])
  else: raise NotImplementedError(row['parsed'].scheme)

@Metric.create({
  '@id': 'cfde_fair:100',
  'name': 'Resolvable Access URLs',
  'description': 'Access URLs (preferrably DRS) are present & valid for the datasets',
  'detail': '''We check that the access_url are present, valid, and a random subset are resolvable''',
  'principle': 'Findable',
})
def metric(CFDE, full=False, **kwargs):
  access_urls = pd.DataFrame([
    dict(
      id_namespace=file['id_namespace'],
      local_id=file['local_id'],
      access_url=file.get('access_url'),
    )
    for file in CFDE.tables['file'].entities()
  ])
  # access_urls should be unique
  access_urls['duplicated'] = access_urls['access_url'].dropna().duplicated(keep=False)
  # try parsing the access urls
  access_urls['parsed'] = access_urls['access_url'].apply(try_parse_url)
  access_urls['scheme'] = access_urls[~pd.isna(access_urls['parsed'])]['parsed'].apply(lambda parsed: parsed.scheme)
  # access urls must follow some scheme
  access_urls['valid_scheme'] = access_urls['scheme'].isin(['drs', 'http', 'https', 's3', 'gs', 'ftp', 'gsiftp', 'globus', 'htsget', 'sftp'])
  # validate drs format
  access_urls['valid_drs'] = access_urls[access_urls['scheme']=='drs']['parsed'].apply(valid_drs_format)
  # test a random sample of at most 100 drs/http urls
  applicable_for_testing = access_urls[access_urls['scheme'].isin(['drs', 'http', 'https'])]
  applicable_for_testing = applicable_for_testing.sample(min(applicable_for_testing.shape[0], 100))
  access_urls['accessible'] = applicable_for_testing.apply(test_access_url, axis=1)
  # incorporate all tests into one "valid" / not
  with pd.option_context('future.no_silent_downcasting', True):
    access_urls['valid'] = (
      (~(access_urls['duplicated'].fillna(False)))
      & access_urls['valid_scheme'].fillna(False)
      & access_urls['valid_drs'].fillna(True)
      & access_urls['accessible'].fillna(True)
    )
  # extrapolate, assuming sampled accessibility ratio applies to all valid urls
  numerator = ((access_urls['accessible'].sum() / access_urls['accessible'].count())) * access_urls['valid'].sum() if access_urls['accessible'].count() > 0 else 0
  value = (numerator / total_files(CFDE)) if total_files(CFDE) else None
  return {
    'value': value,
    'numerator': numerator,
    'denominator': total_files(CFDE),
    'supplement': access_urls.to_dict() if full else pd.concat([
      access_urls.head(5),
      access_urls.tail(5),
    ]).to_dict(),
  }
