"""Configuration file for the Sphinx documentation builder"""

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import packaging

# on_rtd is whether we are on readthedocs.org
# this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Read the Docs template'
author = 'Ruslan Baratov'
project_copyright = f'2025, {author}'

github_url = 'https://github.com/ruslo/read_the_docs_template'

# The full version, including alpha/beta/rc tags
release = '1.0.2'

# The short X.Y version
version = packaging.version.parse(release)
version = f'{version.major}.{version.minor}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

extensions.append('sphinx_immaterial.kbd_keys')

if not on_rtd:
  extensions.append('sphinxcontrib.spelling')
  spelling_show_suggestions = True
  spelling_word_list_filename = 'spelling.txt'

templates_path = ['templates']

exclude_patterns = ['_build', '_venv', 'readme.rst', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['static']

# https://github.com/jbms/sphinx-immaterial/issues/322
html_css_files = [ 'kbd_background.css' ]

# https://github.com/jbms/sphinx-immaterial
extensions.append('sphinx_immaterial')
html_theme = 'sphinx_immaterial'

sphinx_immaterial_custom_admonitions = [
    {
        'name': 'wikipedia',
        'icon': 'fontawesome/brands/wikipedia-w'
    },
    {
        'name': 'stackoverflow',
        'color': (244, 128, 35),
        'icon': 'fontawesome/brands/stack-overflow',
    },
    {
        'name': 'github',
        'icon': 'fontawesome/brands/github',
    },
    {
        'name': 'cmake',
        'color': (0, 82, 155),
        'icon': 'fontawesome/solid/book',
    },
]

html_theme_options = {
    'icon': {
        'repo': 'fontawesome/brands/github',
        'edit': 'material/file-edit-outline',
    },
    'repo_url': github_url,
    'edit_uri': 'blob/master/docs',
    'globaltoc_collapse': True,
    'features': [
        'navigation.expand',
        'navigation.sections',
        'navigation.top',
        'navigation.footer',
        'search.highlight',
        'search.share',
        'search.suggest',
        'toc.follow',
        'toc.sticky',
        'content.code.copy',
        'content.tabs.link',
        'content.action.edit',
        'content.action.view',
        'content.tooltips',
        'announce.dismiss',
    ],
    'palette': [
        {
            'media': '(prefers-color-scheme: light)',
            'scheme': 'default',
            'primary': 'light-green',
            'accent': 'light-blue',
            'toggle': {
                'icon': 'material/lightbulb-outline',
                'name': 'Switch to dark mode',
            },
        },
        {
            'media': '(prefers-color-scheme: dark)',
            'scheme': 'slate',
            'primary': 'deep-orange',
            'accent': 'lime',
            'toggle': {
                'icon': 'material/lightbulb',
                'name': 'Switch to light mode',
            },
        },
    ],
    'toc_title_is_page_title': True,
    'social': [
        {
            'icon': 'fontawesome/brands/github',
            'link': github_url,
            'name': 'Source on GitHub',
        }
    ],
}
