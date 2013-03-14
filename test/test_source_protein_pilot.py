from util import PsmeTestCase, get_b1_ions
from psme.source.protein_pilot import ProteinPilotPeptideReportLoader


class ProteinPilotSourceTestCase(PsmeTestCase):

    def test_read(self):
        psms = self._load_test_psms(ProteinPilotPeptideReportLoader, 'test_proteinpilot1.tsv', source_statistics=['Conf'])
        psm1 = psms[0]
        self.assertEquals('SETGSGEGGVALKK', psm1.sequence)
        self.assertEquals(1808, psm1.scan_reference.number)
        self.assertEquals('99.00000095', psm1.source_statistics['Conf'])
        first_b1_ion = get_b1_ions(psm1.peptide)[0]
        self.assertAlmostEquals(232.1414, first_b1_ion.get_mz(), 4)
