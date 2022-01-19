import time
import json
import urllib.request, urllib.parse
from c2m2_assessment.ontology.client.service import Service

class EnsemblClient(Service):
  def __init__(self):
    super().__init__('ensembl')

  def _lookup(self, gene):
    T = json.load(urllib.request.urlopen(urllib.request.Request(
      f"https://rest.ensembl.org/lookup/id/{urllib.parse.quote(gene)}",
      headers={
        'Accept': 'application/json',
      },
    ), timeout=2))
    if 'error' in T:
      raise Exception(T['error'])
    time.sleep(0.1)
    return T
