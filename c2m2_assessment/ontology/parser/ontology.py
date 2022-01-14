''' pronto has proven very inconsistent for our needs,
so here's our own ontology parsers.

All parsers construct a dictionary of the form:

{
  'ONTOID:id': {
    id: 'ONTOID:id',
    synonyms: [synonym1, synonym2, ...],
    ... # ontology specific
  },
  ...
}
'''

import shelve
import hashlib
from pathlib import Path

CHUNK_SIZE = 8192

def sha256_io(fr):
  h = hashlib.sha256()
  while True:
    buf = fr.read(CHUNK_SIZE)
    if not buf: break
    h.update(buf)
  return h.hexdigest()

class Ontology:
  def __init__(self, source: Path, cachedir='.cached', parse=None):
    source = Path(source)
    assert source.exists()
    with source.open('rb') as fr:
      self.dbfile = Path(cachedir)/f"{source.stem}.{sha256_io(fr)}.shelve"
    self.dbfile.parent.mkdir(parents=True, exist_ok=True)
    if not self.dbfile.exists():
      self.db = shelve.open(str(self.dbfile), 'n')
      for item in self._parse(source):
        self.db[item['id']] = item
      self.db.close()
    self.db = shelve.open(str(self.dbfile), 'r')

  def _parse(self, source):
    raise NotImplemented

  def __contains__(self, key):
    return key in self.db
  def __getitem__(self, key):
    return self.db[key]
  def get(self, key, default=None):
    return self.db.get(key, default=default)
  def keys(self):
    return self.db.keys()
  def values(self):
    return self.db.values()
  def items(self):
    return self.db.items()
  def __iter__(self):
    return iter(self.db)

  def close(self):
    self.db.close()
