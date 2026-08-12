#!/usr/bin/env python3

"""Build documentation"""

import os
import shutil
import subprocess
import sys
import time

from argparse import ArgumentParser
from pathlib import Path

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

def do_clean(clean: bool, directory: Path):
  """Perform optional clean-up"""
  if clean and directory.exists():
    print(f'Removing directory: {directory}')
    shutil.rmtree(directory)
    assert not directory.exists()

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  os.chdir(script_dir)
  print(f'Working directory: {Path.cwd()}')

  parser = ArgumentParser(description=__doc__)
  parser.add_argument('--clean', action='store_true',
      help='Clean temporary files before build')
  args = parser.parse_args()

  clean = args.clean
  assert clean is not None

  uv = find_uv()
  print(f'uv executable: {uv}')
  assert uv.exists()

  print('Check dependencies')
  run([str(uv), 'sync', '--locked'])

  print('Build documentation')
  build_dir = script_dir / '_build'
  do_clean(clean, build_dir)
  static_dir = script_dir / 'static'
  static_dir.mkdir(exist_ok=True)
  run([str(uv), 'run', 'sphinx-build',
      '-v', # verbose
      '-W', # warnings as errors
      str(script_dir), str(build_dir)])

  print('Run spell check')
  spell_dir = script_dir / '_spelling'
  do_clean(clean, spell_dir)
  run([str(uv), 'run', 'sphinx-build', '-b', 'spelling', '-W', str(script_dir),
      str(spell_dir)])

  index_html= build_dir / 'index.html'
  assert index_html.exists()
  print(f'Index HTML: {index_html}')

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
