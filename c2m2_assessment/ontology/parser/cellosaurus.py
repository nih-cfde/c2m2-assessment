import xml.etree.ElementTree as ET
from c2m2_assessment.ontology.parser.ontology import Ontology

class CellosaurusOntology(Ontology):
  def _parse(self, source):
    root = ET.parse(source).getroot()
    for cell_line in root.find('cell-line-list').iterfind('cell-line'):
      for accession in cell_line.find('accession-list').iterfind('accession'):
        yield {
          'id': accession.text.replace('_', ':'),
          'name': cell_line.find('name-list').find("name[@type='identifier']").text,
          'synonyms': {
            synonym.text
            for synonym in cell_line.find('name-list').iterfind("name[@type='synonym']")
          }
        }
