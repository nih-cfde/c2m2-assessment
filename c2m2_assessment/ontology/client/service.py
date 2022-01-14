import time
import shelve
import logging
import traceback
from pathlib import Path

logger = logging.getLogger(__name__)
class Service:
  def __init__(self, service: str, cachedir='.cached'):
    self.dbfile = Path(cachedir)/f"{service}.shelve"
    self.dbfile.parent.mkdir(parents=True, exist_ok=True) 
    self.db = shelve.open(str(self.dbfile))
    self.logger = logger.getChild(service)

  def _lookup(self, key):
    raise NotImplemented

  def __getitem__(self, key):
    value = self.get(key)
    if value is None:
      raise KeyError
    return value

  def get(self, key, default=None):
    if key not in self.db:
      try:
        self.db[key] = value = self._lookup(key)
      except KeyboardInterrupt:
        raise
      except:
        self.logger.warn(f"{key} not found")
        self.logger.debug(traceback.format_exc())
        self.db[key] = value = None
    else:
      value = self.db[key]
    return value if value is not None else default

  def close(self):
    self.db.close()
