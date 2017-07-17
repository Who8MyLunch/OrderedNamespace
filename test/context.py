"""
Great idea from kennethreitz.org for allowing test module to import the package without having to
actually install it.
"""

import os
import sys

# path_work = os.path.abspath(os.path.join('..', '..'))
path_work = os.path.abspath('..')
sys.path.insert(0, path_work)
