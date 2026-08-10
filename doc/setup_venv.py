#!/usr/bin/env python3

"""Setup virtual environment"""

import shutil
import subprocess
import sys
import time

from argparse import ArgumentParser
from pathlib import Path

# Avoid using non-standard modules here since the script itself should be used
# to install dependencies

def run(args):
  """Print arguments and execute"""
  one_line = ' '.join(args)
  print(f'Executing: {one_line}')
  subprocess.run(args, check=True)

def find_uv():
  """Find uv executable"""
  uv = shutil.which('uv')
  if uv is not None:
    return Path(uv)
  sys.exit(
      'uv is not installed. See '
      'https://docs.astral.sh/uv/getting-started/installation/'
  )

def uv_pip_install(uv, venv_dir, requirements):
  """Run uv pip install"""
  print('Install required packages')

  # Workaround for missing exponential backoff
  # - https://stackoverflow.com/a/60781298
  n_attempts = 10
  wait_time = 1
  multiplier = 2
  max_wait_time = 60

  for i in range(n_attempts):
    try:
      if i != 0:
        print(f'Retry {i}/{n_attempts}')
      run([str(uv), 'pip', 'install', '--python', str(venv_dir),
          '--requirement', str(requirements)])
      return
    except subprocess.CalledProcessError as exc:
      print(f'Exception caught, waiting {wait_time} seconds: {exc}')
      time.sleep(wait_time)
      wait_time = min(wait_time * multiplier, max_wait_time)
  sys.exit('Failed')

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.parse_args()

  uv = find_uv()
  print(f'uv executable: {uv}')
  assert uv.exists()

  venv_dir = script_dir / '_venv'
  print(f'venv directory: {venv_dir}')

  print('Create virtual environment')
  run([str(uv), 'venv', '--allow-existing', '--python', sys.executable,
      str(venv_dir)])
  assert venv_dir.is_dir()

  requirements = script_dir / 'requirements.txt'
  assert requirements.exists()

  uv_pip_install(uv, venv_dir, requirements)

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
