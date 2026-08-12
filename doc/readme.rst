- ``run_build.py`` Build Sphinx documentation
- ``make_release.py`` Update version in ``conf.py``/``pyproject.toml`` and create Git tag

Dependencies
------------

Required system packages:

.. code-block:: none

  $ apt -y install python3-enchant
  $ apt -y install git

Install ``uv``:

.. code-block:: none

  $ curl -LsSf https://astral.sh/uv/install.sh | sh

Pylint
------

Configuration is in ``pyproject.toml``

.. code-block:: none

  $ uv run pylint run_build.py
  $ uv run pylint make_release.py
  $ uv run pylint check_format.py
  $ uv run pylint --const-naming-style=snake_case --allow-global-unused-variables=yes conf.py

Ruff
----

Configuration is in ``pyproject.toml``

.. code-block:: none

  $ uv run ruff check --show-files .

Sphinx Lint
-----------

.. code-block:: none

  $ uv run sphinx-lint --ignore .venv/ .
