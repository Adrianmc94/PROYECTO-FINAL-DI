import os
import sys

# Engadimos tanto a raíz do proxecto como a carpeta src ao camiño de busca
# Isto soluciona o erro "No module named 'src'"
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
project = 'Xestor Eventos'
copyright = '2026, AdrianMc'
author = 'AdrianMc'

# -- General configuration ---------------------------------------------------
# Engadimos as extensións necesarias para ler o código e os docstrings
extensions = [
    'sphinx.ext.autodoc',      # Extrae a documentación dos comentarios
    'sphinx.ext.napoleon',     # Soporta estilos de comentarios Google/NumPy
    'sphinx.ext.viewcode',     # Engade enlaces ao código fonte na web
    'sphinx.ext.intersphinx',  # Enlaza con outras documentacións se fose necesario
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Idioma da documentación (pon 'es' ou 'gl' se prefires a interface nese idioma)
language = 'es'

# -- Options for HTML output -------------------------------------------------
# O tema 'alabaster' é o por defecto, podes cambialo por 'sphinx_rtd_theme' se o tes instalado
html_theme = 'alabaster'
html_static_path = ['_static']

# Forzamos a que autodoc non falle se hai dependencias de sistema (como Gtk)
# Isto evita os erros de importación ao xerar a doc en entornos sen a UI instalada
autodoc_mock_imports = ["gi"]