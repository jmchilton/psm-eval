from util import PsmeTestCase

from psme.peak_list import ScanSourceManager


class PeakListTestCase(PsmeTestCase):

    def test_get_scans(self):
        path = self._test_data_path('test2.mzML')
        first = True
        scan_source_manager = ScanSourceManager({"peak_lists": [path]})
        for scan in scan_source_manager.get_scans():
            print scan
            if first:
                assert scan.id == \
                    "controllerType=0 controllerNumber=1 scan=2"
            first = False
