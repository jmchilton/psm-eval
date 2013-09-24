import unittest

from psme.peptide import Peptide


UNMODIFIED_TEST_PEPTIDE = Peptide("AGCDE", [])


class PeptideTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_seq_mass_no_mods_mono(self):
        peptide = UNMODIFIED_TEST_PEPTIDE
        mass1 = peptide.get_seq_mass(None, 1, "n", ion_type='b')
        self.assertAlmostEqual(mass1, 71.037113805)

    @unittest.skip("Average doesn't work")
    def test_get_seq_mass_no_mods_avg(self):
        peptide = UNMODIFIED_TEST_PEPTIDE
        mass = peptide.get_seq_mass(None, 3, "c", ion_type='b')
        self.assertAlmostEqual(mass, 115.0874 + 129.11398)

    def test_neutral_loss(self):
        pass
        #from pyteomics.mass import calculate_mass
        #assert False, calculate_mass(parsed_sequence='SLEDLDKEMADYFE', charge=1, ion_type='b')

    def test_tpp_plain(self):
        peptide = self.from_tpp("K.AGCDE.R")
        assert peptide.sequence == "AGCDE"

    def test_tpp_modified(self):
        peptide = self.from_tpp("R.M[147.04]HSM[147.04]LDFTLGAK.A")
        assert peptide.sequence == "MHSMLDFTLGAK"

        self.assertAlmostEquals(peptide.get_seq_mass(None, 1, "n", ion_type='b'), 147.04)

    def test_n_term_modified(self):
        peptide = self.from_tpp("-.n[43.02]M[147.04]AAACVSDDHADM.A")
        assert peptide.sequence == "MAAACVSDDHADM"

        self.assertAlmostEqual(peptide.n_term_modifications[0], 43.02)

    def test_c_term_modified(self):
        peptide = self.from_tpp("-.M[147.04]AAACVSDDHADMc[143.02].A")
        assert peptide.sequence == "MAAACVSDDHADM"

        self.assertAlmostEqual(peptide.c_term_modifications[0], 143.02)

    def from_tpp(self, peptide_string):
        return Peptide.from_tpp_peptide_string(peptide_string)
