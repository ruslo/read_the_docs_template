#!/usr/bin/env python3

"""Create new release"""

import os
import re
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
  res = subprocess.run(args, check=True, text=True, capture_output=True)
  assert res.stderr == ''
  return res.stdout.splitlines()

def find_uv():
  """Find uv executable"""
  uv = shutil.which('uv')
  if uv is not None:
    return Path(uv)
  sys.exit(
      'uv is not installed. See '
      'https://docs.astral.sh/uv/getting-started/installation/'
  )

def check_clean():
  """Check the current Git repository is clean"""
  output = run(['git', 'status', '--porcelain'])
  if len(output) == 0:
    return
  print('Repository is not clean:')
  for i in output:
    print(f'  {i}')
  sys.exit(1)

def patch_conf_py(conf_py, version):
  """Set new version to conf.py"""
  print(f'Patching configuration file: {conf_py}')

  new_lines = []

  with open(conf_py, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    match_found = False
    for i in lines:
      if re.match(r'release\s*=', i) is None:
        new_lines.append(i)
      else:
        assert not match_found
        match_found = True
        new_version = f"release = '{version}'\n"
        assert i != new_version
        new_lines.append(new_version)
    assert match_found

  with open(conf_py, 'w', encoding='utf-8') as file:
    for i in new_lines:
      file.write(i)

def patch_pyproject_toml(pyproject_toml, version):
  """Set new version to pyproject.toml"""
  print(f'Patching project file: {pyproject_toml}')

  new_lines = []

  with open(pyproject_toml, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    match_found = False
    for i in lines:
      if re.match(r'version\s*=', i) is None:
        new_lines.append(i)
      else:
        assert not match_found
        match_found = True
        new_version = f'version = "{version}"\n'
        assert i != new_version
        new_lines.append(new_version)
    assert match_found

  with open(pyproject_toml, 'w', encoding='utf-8') as file:
    for i in new_lines:
      file.write(i)

def run_main():
  """Wrapper for main"""
  this_script = Path(__file__)
  assert this_script.exists()

  script_dir = this_script.parent
  assert script_dir.is_dir()

  parser = ArgumentParser(description=__doc__)
  parser.add_argument('-v', required=True,
      help='Specify version, e.g. 2.3.4-rc.1')
  parser.add_argument('-S', action='store_true',
      help='Sign tag with GPG key')
  args = parser.parse_args()

  os.chdir(script_dir)

  print(f'Current working directory: {Path.cwd()}')
  version = args.v
  assert version is not None
  git_tag = f'v{version}'
  print(f'Creating release {version} with Git tag {git_tag}')

  gpg_sign = args.S
  assert gpg_sign is not None
  print(f'Use GPG sign? {gpg_sign}')

  check_clean()

  conf_py = Path('conf.py')
  conf_py = conf_py.absolute()
  patch_conf_py(conf_py, version)

  pyproject_toml = Path('pyproject.toml')
  pyproject_toml = pyproject_toml.absolute()
  patch_pyproject_toml(pyproject_toml, version)

  uv = find_uv()
  print(f'uv executable: {uv}')
  assert uv.exists()

  uv_lock = Path('uv.lock')
  print(f'Update {uv_lock} file')
  run([str(uv), 'sync', '--quiet'])

  run(['git', 'add', str(conf_py), str(pyproject_toml), str(uv_lock)])

  message = f'Release {version}'

  cmd_args = ['git', 'commit']
  if gpg_sign:
    cmd_args.append('-S')
  cmd_args += ['-m', message]
  run(cmd_args)

  cmd_args = ['git', 'tag', '-m', message]
  if gpg_sign:
    cmd_args.append('-s')
  cmd_args.append(git_tag)
  run(cmd_args)

if __name__ == '__main__':
  start = time.time()
  run_main()
  elapsed = time.time() - start
  print(f'Done in {elapsed:.3f} sec')
