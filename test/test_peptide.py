import unittest

from psme.peptide import Peptide


UNMODIFIED_TEST_PEPTIDE = Peptide("AGCDE", [])


class PeptideTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_seq_mass_no_mods(self):
        peptide = UNMODIFIED_TEST_PEPTIDE
        mass1 = peptide.get_seq_mass_mono(1, "n")
        self.assertAlmostEqual(mass1, 71.037113805)
        mass2 = peptide.get_seq_mass_avg(3, "c")
        self.assertAlmostEqual(mass2, 115.0874 + 129.11398)

    def test_neutral_loss(self):
        pass
        #from pyteomics.mass import calculate_mass
        #assert False, calculate_mass(parsed_sequence='SLEDLDKEMADYFE', charge=1, ion_type='b')
