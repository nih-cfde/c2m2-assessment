import re
import csv
from c2m2_assessment.ontology.parser.ontology import Ontology

class EDAMOntology(Ontology):
  def _parse(self, source):
    with open(source, 'r') as fr:
      reader = csv.DictReader(fr, delimiter='\t')
      for record in reader:
        yield {
          'id': re.sub(r'^http://edamontology\.org/([^_]+)_(.+)$', r'\1:\2', record['Class ID']),
          'name': record['Preferred Label'],
          'obsolete': record['Obsolete'] == 'TRUE',
          'synonyms': {
            synonym
            for synonym in record['Synonyms'].split('|')
            if synonym
          },
        }
