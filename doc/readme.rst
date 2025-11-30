- ``setup_venv.py`` Setup Python virtual environment with dependencies from ``requirements.txt``
- ``run_build.py`` Build Sphinx documentation
- ``run_clean.py`` Remove temporary documentation files
- ``make_release.py`` Update ``release`` in ``conf.py`` and create Git tag

Dependencies
------------

Required system packages:

.. code-block:: none

  $ apt -y install python3-venv
  $ apt -y install python3-enchant
  $ apt -y install git

Pylint
------

.. code-block:: none

  $ pylint setup_venv.py
  $ pylint run_build.py
  $ pylint run_clean.py
  $ pylint make_release.py
  $ pylint check_format.py
  $ pylint --const-naming-style=snake_case conf.py
