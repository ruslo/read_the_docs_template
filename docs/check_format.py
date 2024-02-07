#!/usr/bin/env python3

"""Check C++ format"""

import difflib
import os
import subprocess
import sys
import time
import tempfile

from argparse import ArgumentParser
from pathlib import Path

def run(args):
  """Print arguments and execute"""
  one_line = ' '.join(args)
  print(f'Executing: {one_line}')
  result = subprocess.run(args, check=True, text=True, capture_output=True)
  assert result.stderr == ''
  return result.stdout

def skip_dir(relative_dir):
  """Directory should be skipped from checking"""
  exclude_dirs = ['_build', '_builds', 'third_party', '_deps', '_venv']
  if not relative_dir.parts:
    return False
  for excluded in exclude_dirs:
    if excluded in relative_dir.parts:
      return True
  return False

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.parse_args()

  cfg = script_dir / '.clang-format'
  print(f'Configuration: {cfg}')
  assert cfg.exists()

  for root, _, files in os.walk(script_dir):
    relative = Path(root).relative_to(script_dir)
    if skip_dir(relative):
      continue
    for i in files:
      if Path(i).suffix not in ['.cpp', '.h']:
        continue
      to_check = Path(root) / i
      with open(to_check, 'r', encoding='utf-8') as file:
        original = file.read()
      formatted = run(['clang-format', '-style=file', str(to_check)])
      if original == formatted:
        continue
      with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp:
        tmp.write(formatted)
      if original.rstrip('\n') == formatted.rstrip('\n'):
        print('\nInconsistent newline(s) at end of file')
      else:
        diff = difflib.unified_diff(original.splitlines(),
            formatted.splitlines(), fromfile=str(to_check), tofile=tmp.name)
        print('\n'.join(diff))
      print(f'\nApply hint:\n  mv {tmp.name} {to_check}')
      sys.exit(1)

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
