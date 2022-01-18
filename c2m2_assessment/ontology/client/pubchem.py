import time
import json
import urllib.request, urllib.parse
from c2m2_assessment.ontology.client.service import Service

class PubChemCompoundCIDClient(Service):
  def __init__(self):
    super().__init__('pubchem_compound_cid')

  def _lookup(self, cid):
    T = json.load(urllib.request.urlopen(
      f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{urllib.parse.quote(cid)}/dates/json",
      timeout=2,
    ))
    if 'Fault' in T:
      raise Exception(T['Fault']['Message'])
    time.sleep(0.5)
    return { 'CID': cid }

class PubChemSubstanceSIDClient(Service):
  def __init__(self):
    super().__init__('pubchem_substance_sid')

  def _lookup(self, sid):
    T = json.load(urllib.request.urlopen(
      f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/{urllib.parse.quote(sid)}/dates/json",
      timeout=2,
    ))
    if 'Fault' in T:
      raise Exception(T['Fault']['Message'])
    time.sleep(0.5)
    return { 'SID': sid }
