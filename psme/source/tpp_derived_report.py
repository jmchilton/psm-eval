from .tabular import TabularLoader
from psme.psm import Psm
from psme.peak_list import ScanReference
from psme.peptide import Peptide


class TppDerivedReportLoader(TabularLoader):

    def __init__(self, settings, scan_source_manager):
        super(TppDerivedReportLoader, self).__init__(settings)
        self.scan_source_manager = scan_source_manager

        def set_index(name):
            setattr(self, name, int(settings[name]))

        set_index('scan_id_column_index')
        set_index('scan_source_column_index')
        set_index('peptide_column_index')

    def _get_row_parser(self, source_statistic_names):
        return RowParser(self, source_statistic_names)


class RowParser(object):

    def __init__(self, report_loader, source_statistic_names):
        self.report_loader = report_loader
        self.source_statistic_names = source_statistic_names

    def get_psm(self, row):
        return self.__get_psm(row)

    def __get_psm(self, row):
        peptide_string = row[self.report_loader.peptide_column_index]
        scan_source_name = row[self.report_loader.scan_source_column_index]
        scan_source = self.report_loader.scan_source_manager.match_by_name(scan_source_name)
        scan_id = row[self.report_loader.scan_id_column_index]
        scan_reference = ScanReference(id=scan_id, source=scan_source)

        source_statistics = {}
        for source_statistic_name in self.source_statistic_names:
            try:
                source_statistics[source_statistic_name] = \
                    row[int(source_statistic_name)]
            except KeyError:
                pass

        peptide = Peptide.from_tpp_peptide_string(peptide_string)
        psm = Psm(peptide=peptide,
                  scan_reference=scan_reference,
                  source_statistics=source_statistics
                  )

        return psm
