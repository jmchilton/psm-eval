from re  import match

from .tabular import TabularLoader
from psme.psm import Psm
from psme.peak_list import ScanReference
from psme.peptide import Peptide
from psme.unimod import load_unimod


class ProteinPilotPeptideReportLoader(TabularLoader):

    def __init__(self, settings, scan_source_manager):
        super(ProteinPilotPeptideReportLoader, self).__init__(settings)
        self.scan_source_manager = scan_source_manager
        self.unimod = load_unimod(settings)

    def _get_row_parser(self, source_statistic_names):
        return ProteinPilotRowParser(self, source_statistic_names)


class ProteinPilotRowParser(object):

    def __init__(self, report_loader, source_statistic_names):
        self.source_statistic_names = source_statistic_names
        self.source_column_indices = {}
        self.scan_source_manager = report_loader.scan_source_manager
        self.unimod = report_loader.unimod

    def get_psm(self, row):
        if row[0].strip() == "N":
            return self.__get_header_psm(row)
        else:
            return self.__get_psm(row)

    def __get_header_psm(self, row):
        for i, column in enumerate(row):
            self.source_column_indices[column] = i
        return None

    def __get_psm(self, row):
        sequence = row[self.__get_index('Sequence', 12)]
        modifications_str = row[self.__get_index('Modifications', 13)]
        peptide_mod_args = self.__convert_modifications(modifications_str)
        spectrum_str = row[self.__get_index('Spectrum', 22)]
        scan_id, scan_source_index = self.__split_spectrum(spectrum_str)
        scan_source = self.scan_source_manager.match_by_index(int(scan_source_index) - 1)
        scan_reference = ScanReference(number=int(scan_id), source=scan_source)
        source_statistics = {}
        for source_statistic_name in self.source_statistic_names:
            try:
                source_statistics[source_statistic_name] = row[self.__get_index(source_statistic_name)]
            except KeyError:
                pass
        peptide = Peptide(sequence=sequence, **peptide_mod_args)
        psm = Psm(peptide=peptide,
                  scan_reference=scan_reference,
                  source_statistics=source_statistics
                  )
        return psm

    def __convert_modifications(self, modifications_str):
        modification_strs = [modification_str.strip() for modification_str in modifications_str.split(";")]
        peptide_args = {"modifications": [], "n_term_modifications": [], "c_term_modifications": []}
        for modification_str in modification_strs:
            if not modification_str:
                continue
            (mod, site) = modification_str.rsplit("@", 1)
            mod = mod.strip()
            site = site.strip()
            unimod_entry = self._find_unimod_entry(mod)
            if not unimod_entry:
                raise Exception("Failed to parse unimod entry for %s" % modification_str)
            if site.lower() == "n-term":
                peptide_args["n_term_modifications"].append(unimod_entry)
            elif site.lower() == "c-term":
                peptide_args["c_term_modifications"].append(unimod_entry)
            else:
                peptide_args["modifications"].append({"position": int(site) - 1, "unimod_entry": unimod_entry})
        return peptide_args

    def __split_spectrum(self, spectrum_str):
        spectrum_parts = spectrum_str.split(".")
        return spectrum_parts[3], spectrum_parts[0]

    def __get_index(self, name, default_index=None):
        return self.source_column_indices.get(name, default_index)

    def _find_unimod_entry(self, label):
        entry = self._find_unimod_entry_exact(label)
        if entry:
            return entry

        # No an exact entry, maybe contains amino acid listed at the end
        entryWithAAMatch = match(r'^(.*)\s*\([a-zA-Z]\)\s*$', label)
        if entryWithAAMatch:
            possibleName = entryWithAAMatch.group(1).strip()
            entry = self._find_unimod_entry_exact(possibleName)
            if entry:
                return entry
        return None

    def _find_unimod_entry_exact(self, label):
        entry = self.unimod.by_title(label)
        if entry:
            return entry

        entry = self.unimod.by_name(label)
        if entry:
            return entry

        return None
