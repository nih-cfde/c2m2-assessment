import time
import yaml
import urllib.request, urllib.parse
from c2m2_assessment.ontology.client.service import Service

class EnsemblClient(Service):
  def _lookup(self, gene):
    T = yaml.safe_load(urllib.request.urlopen(
      f"https://rest.ensembl.org/lookup/id/{urllib.parse.quote(gene)}"
    ))
    if 'error' in T:
      raise Exception(T['error'])
    time.sleep(0.1)
    return T
