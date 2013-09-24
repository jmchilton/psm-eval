from unittest import TestCase

from psme.ion import get_ions
from psme.peptide import Peptide


class IonTestCase(TestCase):

    def test_main_series_ions(self):
        peptide = Peptide("SAMPLER")

        second_ion_masses = {"a1": 131.0815, "b1": 159.0764, "c1": 176.1030,
                             "x1": 330.1408, "y1": 304.1615, "z1": 288.1428}
        for ion_series, second_mz in second_ion_masses.iteritems():
            ions = self._get_ion_series(peptide, ion_series)
            calculated_mz = ions[1].get_mz()
            self.assertAlmostEquals(second_mz, calculated_mz, 4)

        fourth_ion_masses = {"b1": 387.1697, "y1": 514.2984}
        for ion_series, fourth_mz in fourth_ion_masses.iteritems():
            ions = self._get_ion_series(peptide, ion_series)
            calculated_mz = ions[3].get_mz()
            self.assertAlmostEquals(fourth_mz, calculated_mz, 4)

    def test_internal_combos(self):
        peptide = Peptide("SAMAMR")
        labels = self._internal_ion_labels(peptide)
        self.assertEquals(1, labels.count("AM"), labels)

        peptide = Peptide("SAMAMR", modifications=[{"position": 1, "mod_mass": 8.0}])
        labels = self._internal_ion_labels(peptide)
        self.assertEquals(1, labels.count("AM"), labels)
        self.assertEquals(1, labels.count("A[8.0]M"), labels)

    def _internal_ion_labels(self, peptide):
        internal_ions = self._get_ion_series(peptide, 'internal')
        return [ion.peptide_context.labeled_sequence for ion in internal_ions]

    def _get_ion_series(self, peptide, series, losses=[]):
        return get_ions(peptide, series=[series], losses=losses)
