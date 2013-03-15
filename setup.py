from distutils.core import setup

VERSION='0.1.0'

CLASSIFIERS=\
"""
Development Status :: 4 - Beta
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
Intended Audience :: End Users/Desktop
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
Operating System :: POSIX :: Linux
"""

SHORT_DESCRIPTION="A stand-alone application and Python library for re-evaluating identified peptide-spectrum-matches (PSMs)."

# TODO:
LONG_DESCRIPTION=\
"""
"""

setup(
  name='psm-eval',
  version=VERSION,
  description=SHORT_DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  classifiers=[x for x in CLASSIFIERS.split("\n") if x],
  author='John Chilton',
  author_email='jmchilton at gmail dot com',
  maintainer='John Chilton',
  maintainer_email='jmchilton at gmail dot com',
  url='https://github.com/jmchilton/psm-eval',
  packages=['psme'],
  requires=['pyteomics (>=2.1.3)', 'pyyaml'],
)
