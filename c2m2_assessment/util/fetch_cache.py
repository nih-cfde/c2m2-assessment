
def fetch_cache(url, filename, cachedir='.cached'):
  import time, random, urllib.request
  from pathlib import Path
  cachedir = Path(cachedir)
  cachedir.mkdir(parents=True, exist_ok=True)
  cachefile = cachedir/filename
  lockfile = cachedir/f"{filename}.lock"
  # if a lockfile for this file is present, wait until it's gone
  while lockfile.exists():
    time.sleep(0.5 + random.random())
  # if this file doesn't exists create it
  if not cachefile.exists():
    # lock the file while we create it
    lockfile.open('w').close() # touch
    urllib.request.urlretrieve(url, filename=cachefile)
    # release the lock before returning
    lockfile.unlink()
  return cachefile
