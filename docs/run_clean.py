#!/usr/bin/env python3

"""Remove temporary documentation files"""

import time

from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.parse_args()

  to_clean = ['_build', '_static', '_spelling']
  for i in to_clean:
    d_abs = script_dir / i
    if not d_abs.exists():
      print(f'Not found: {d_abs}')
      continue
    print(f'Removing directory: {d_abs}')
    rmtree(d_abs)
    assert not d_abs.exists()

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
