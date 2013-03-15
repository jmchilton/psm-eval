from util import PsmeTestCase
from psme.source.mzid import MzIdLoader


class MzIdSourceTestCase(PsmeTestCase):

    def test_read(self):
        psms = self._load_test_psms(MzIdLoader, 'test2.mzid')
        assert len(psms[1].peptide.modifications[0]) == 0
        mods = psms[2].peptide.modifications
        assert mods[0][0]["mod_mass"] == 16.0
        assert psms[0].sequence == 'FFTALK'
        assert psms[0].scan_reference.id == 'controllerType=0 controllerNumber=1 scan=2'
