# Simple interface to MeshPy / TetGen in Blender

## Installation

Tested with Blender `2.79`.

We need the `MeshPy` python module. The best method is: (1) identify the Python version Blender is using, (2) install MeshPy for that version in a separate virtual environment Python (see [here](https://blender.stackexchange.com/questions/41258/install-python-module-for-blender)), (3) copy over the module.

1. Identify Python version: Navigate to the directory - on a Mac it is probably `/Applications/Blender/blender.app/Contents/Resources/2.79/python/bin/`. Check the exact version with `./python3.5m --version` - here it is `3.5.3`.

2. Install MeshPy for that version (see [here](https://blender.stackexchange.com/questions/41258/install-python-module-for-blender)). Using `conda` (from any directory):
  * Create the virtual environment: `conda create --name conda-python-blender python=3.5.3`.
  * Activate: `source activate conda-python-blender`.
  * Install MeshPy: `pip install MeshPy`. Probably you will also be prompted to install `pip install pybind11`.
  * Find the directory for the module: `echo "import sys; print(sys.path)" | python`. It should be something like: `~/anaconda3/envs/conda-python-blender/lib/python3.5.3/site-packages`.
  * Copy over the module: `cp -r ~/anaconda3/envs/conda-python-blender/lib/python3.5.3/site-packages/MeshPy* /Applications/Blender/blender.app/Contents/Resources/2.79/python/lib/python3.5/site-packages/`.
