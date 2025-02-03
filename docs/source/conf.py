# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Указывает на корень проекта
sys.path.insert(0, os.path.abspath('../..'))  # Указывает на корень проекта

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Stream'
copyright = '2025, Andrey Sobolev'
author = 'Андрей Соболев'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Для извлечения docstrings
    'sphinx.ext.viewcode',  # Для добавления ссылок на исходный код
    'sphinx.ext.napoleon',  # Для поддержки Google- или NumPy-стиля docstrings
]

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'test*.py',       # Исключает файлы, начинающиеся с test
    '**/test*.py',    # Исключает такие файлы во всех поддиректориях
]


language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
# html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
