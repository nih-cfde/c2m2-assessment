import re
from c2m2_assessment.ontology.parser.ontology import Ontology

def ensure_list(L):
  if type(L) == list: return L
  else: return [L]

class OBOOntology(Ontology):
  def _parse(self, source):
    with open(source, 'r') as fr:
      for block in OBOOntology._walk_obo(fr):
        if block['_type'] == 'Term':
          yield dict(block, synonyms=set(ensure_list(block.get('synonym', []))))

  _section_re = re.compile(r'^\[([^\]]+)\]$')
  _kv_re = re.compile(r'^([^:]+):\s*(.+)$')

  @staticmethod
  def _walk_obo(fr):
    _type = None
    buf = []
    blocks = []
    for line in map(str.strip, fr):
      if not line: continue
      if line.startswith('!'): continue
      m = OBOOntology._section_re.match(line)
      if m is None:
        try:
          k, v = OBOOntology._kv_re.match(line).groups()
          buf.append((k, v))
        except:
          print(line)
          raise
        continue
      else:
        yield OBOOntology._prepare_block(_type, buf)
        buf = []
        _type = m.group(1)
    if buf: yield OBOOntology._prepare_block(_type, buf)

  @staticmethod
  def _prepare_block(_type, block_buf):
    # we've buffered a bunch of parsed lines and hit a new section
    # create a jsonld-style dictionary, add the section type, and add the block
    as_dict = {}
    for k, v in block_buf:
      if k not in as_dict: as_dict[k] = [v]
      else: as_dict[k].append(v)
    for k in list(as_dict.keys()):
      if len(as_dict[k]) == 1: as_dict[k] = as_dict[k][0]
    return dict(as_dict, _type=_type)
