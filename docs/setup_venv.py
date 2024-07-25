#!/usr/bin/env python3

"""Setup virtual environment"""

import subprocess
import time

from argparse import ArgumentParser
from pathlib import Path
from venv import EnvBuilder
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from tenacity import wait_random_exponential

import urllib3

def run(args):
  """Print arguments and execute"""
  one_line = ' '.join(args)
  print(f'Executing: {one_line}')
  subprocess.run(args, check=True)

# Workaround for missing exponential backoff
# - https://stackoverflow.com/a/60781298
@retry(retry=retry_if_exception_type(urllib3.exceptions.ReadTimeoutError),
    stop=stop_after_attempt(10),
    wait=wait_random_exponential(multiplier=1, max=60))
def pip_install(venv_python, requirements):
  """Run pip install"""
  print('Install required packages')
  run([str(venv_python), '-m', 'pip', 'install',
      '--requirement', str(requirements)])

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.parse_args()

  venv_dir = script_dir / '_venv'
  print(f'venv directory: {venv_dir}')
  venv_builder = EnvBuilder()
  venv_builder.create(venv_dir)
  context = venv_builder.ensure_directories(venv_dir)

  venv_python = Path(context.env_exec_cmd)
  assert venv_python.exists()
  print(f'Python executable: {venv_python}')

  print('Ensure pip')
  run([str(venv_python), '-m', 'ensurepip', '--upgrade'])

  print('Upgrade pip')
  run([str(venv_python), '-m', 'pip', 'install', '-U', 'pip'])

  requirements = script_dir / 'requirements.txt'
  assert requirements.exists()

  pip_install(venv_python, requirements)

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
