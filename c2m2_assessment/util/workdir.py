import contextlib
from pathlib import Path

@contextlib.contextmanager
def workdir(work=None):
  ''' Prepare a temporary work directory or use one provided
  '''
  if work is None:
    import tempfile
    work_dir = Path(tempfile.mkdtemp())
  else:
    work_dir = Path(work)
  try:
    yield work_dir
  finally:
    if work is None:
      import shutil
      shutil.rmtree(work_dir)
