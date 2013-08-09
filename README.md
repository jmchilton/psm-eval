PSM Evaluator GUI

Dependencies:
1. Install core dependencies (listed in requirements.txt)
2. Install mMass

Setting up mMass as a library:

1. Download and install mMass (refer to mMass user guide)
2. Put mMass folder in site-packages (Python library folder) and add __init__.py (an empty file) in mMass folder.
3. *This is not needed if got rid of sequence functions
-in mmass.gui.sequence.py change last two lines of import to:
	 from panel_match import panelMatch
	 from panel_monomer_library import panelMonomerLibrary
 (remove gui.)

Usage:
in psm-eval folder: python -m gui.main_frame

Current Known Issues:
1. Sometimes ions don't get labelled correctly. This is perhaps due to not returning the correct ion_peak pairs in matches_ion.py.