import datetime
import os
import sys

import toml

with open("../pyproject.toml", "rt") as f:
    metadata = toml.load(f)

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "Twelve Factor"
author = "Daniel Knell"
copyright = "{} {}".format(datetime.datetime.now().year, author)

release = metadata["tool"]["poetry"]["version"]

version = ".".join(release.split(".")[:2])

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "alabaster"

html_sidebars = {
    "index": ["about.html", "extra.html", "searchbox.html", "donate.html"],
    "**": [
        "about.html",
        "localtoc.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ],
}

html_theme_options = {
    "description": metadata["tool"]["poetry"]["description"],
    "github_user": "artisanofcode",
    "github_repo": "python-twelvefactor",
    "show_powered_by": False,
    "show_related": True,
}

html_context = {"pypi_name": metadata["tool"]["poetry"]["name"]}

intersphinx_mapping = {"python": ("https://docs.python.org/dev", None)}
