#!/usr/bin/env python3

"""Build documentation"""

import subprocess
import sys
import time

from argparse import ArgumentParser
from pathlib import Path
from venv import EnvBuilder

def run(args):
  """Print arguments and execute"""
  one_line = ' '.join(args)
  print(f'Executing: {one_line}')
  subprocess.run(args, check=True)

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.add_argument('--novenv', action='store_true',
      help='Do not create local virtualenv')
  args = parser.parse_args()

  novenv = args.novenv
  assert not novenv is None

  if novenv:
    python_path = Path(sys.executable)
  else:
    venv_dir = script_dir / '_venv'
    print(f'venv directory: {venv_dir}')
    assert venv_dir.is_dir()
    venv_builder = EnvBuilder()
    context = venv_builder.ensure_directories(venv_dir)
    python_path = Path(context.env_exec_cmd)

  assert python_path.exists()
  print(f'Python executable: {python_path}')

  if sys.platform == 'win32':
    exe_suffix = '.exe'
  else:
    exe_suffix = ''

  sphinx_build = python_path.parent / f'sphinx-build{exe_suffix}'
  print(f'Sphinx build executable: {sphinx_build}')
  assert sphinx_build.exists()

  print('Build documentation')
  build_dir = script_dir / '_build'
  static_dir = script_dir / 'static'
  static_dir.mkdir(exist_ok=True)
  run([str(sphinx_build),
      '-v', # verbose
      '-W', # warnings as errors
      str(script_dir), str(build_dir)])

  print('Run spell check')
  spell_dir = script_dir / '_spelling'
  run([str(sphinx_build), '-b', 'spelling', '-W', str(script_dir),
      str(spell_dir)])

  index_html= build_dir / 'index.html'
  assert index_html.exists()
  print(f'Index HTML: {index_html}')

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
