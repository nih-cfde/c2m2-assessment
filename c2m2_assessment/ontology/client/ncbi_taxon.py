import time
import xml.etree.ElementTree
import urllib.request, urllib.parse
from c2m2_assessment.ontology.client.service import Service

class NCBITaxonClient(Service):
  def __init__(self):
    super().__init__('ncbitaxon')

  def _lookup(self, id):
    T = xml.etree.ElementTree.parse(
      urllib.request.urlopen(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={urllib.parse.quote(id)}"
      )
    )
    t = T.find('Taxon')
    time.sleep(0.5)
    return {
      'taxid': t.find('TaxId').text,
      'name': t.find('ScientificName').text,
      'rank': t.find('Rank').text,
    }
