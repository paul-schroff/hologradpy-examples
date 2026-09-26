# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import importlib.util
import os
import pathlib
import warnings

from sphinx_gallery.sorting import NumberOfCodeLinesSortKey

# ---- Project information -------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "HoloGradPy examples"
copyright = "2026, Paul Schroff, Department of Physics, University of Strathclyde"
author = "Paul Schroff"

# ---- General configuration -----------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinx_copybutton",
]

default_role = "literal"

# ---- Warnings ------------------------------------------------------------------------
# Warnings raised during a render are printed into the committed pages. Their paths are
# shown relative to the installed package, and as a bare file name elsewhere.
_PACKAGE_PARENT = (
    pathlib.Path(importlib.util.find_spec("hologradpy").origin).resolve().parents[1]
)


def _relative_warning(message, category, filename, lineno, line=None):
    path = pathlib.Path(filename)
    try:
        shown = path.resolve().relative_to(_PACKAGE_PARENT).as_posix()
    except ValueError:
        shown = path.name
    return f"{shown}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = _relative_warning

# ---- Cross-references ----------------------------------------------------------------
intersphinx_mapping = {
    "hologradpy": ("https://hologradpy.readthedocs.io/en/latest/", None),
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "torch": ("https://docs.pytorch.org/docs/stable/", None),
}

# ---- Example gallery -----------------------------------------------------------------
# Examples only run when HOLOGRADPY_RUN_EXAMPLES=1 since they take minutes on a GPU.
RUN_EXAMPLES = os.environ.get("HOLOGRADPY_RUN_EXAMPLES") == "1"

# Re-run only selected examples for faster iteration.
EXAMPLE_FILTER = os.environ.get("HOLOGRADPY_EXAMPLES", "")


class WithinSectionOrder(NumberOfCodeLinesSortKey):
    EXPLICIT = (
        "top_hat_beam_shaping.py",
        "gradient_phase_retrieval.py",
        "optimal_transport_phase_guess.py",
        "vortex_annihilation.py",
    )

    def __call__(self, filename: str) -> tuple[int, int]:
        if filename in self.EXPLICIT:
            return (0, self.EXPLICIT.index(filename))
        return (1, super().__call__(filename))


sphinx_gallery_conf = {
    "examples_dirs": [
        "../examples/hardware_interface",
        "../examples/phase_retrieval",
        "../examples/camera_feedback",
        "../examples/calibration",
    ],
    "gallery_dirs": [
        "auto_examples/hardware_interface",
        "auto_examples/phase_retrieval",
        "auto_examples/camera_feedback",
        "auto_examples/calibration",
    ],
    "within_subsection_order": WithinSectionOrder,
    "plot_gallery": RUN_EXAMPLES,
    "filename_pattern": EXAMPLE_FILTER or r".*",
    # A selected example runs even when its source is unchanged, since editing the
    # package leaves every example's md5 untouched.
    "run_stale_examples": bool(EXAMPLE_FILTER),
    "only_warn_on_example_error": True,
    "image_srcset": ["2x"],
    "subsection_order": [
        "../examples/calibration/camera_mapping",
        "../examples/calibration/wavefront_calibration",
        "../examples/calibration/pixel_crosstalk_calibration",
    ],
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# ---- Options for HTML output ---------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "HoloGradPy examples"

html_static_path = ["_static"]
html_css_files = ["custom.css"]
