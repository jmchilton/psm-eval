

class Psm(object):

    def __init__(self, scan_reference, peptide, source_statistics={}):
        self.scan_reference = scan_reference
        self.source_statistics = source_statistics
        self.peptide = peptide

    @property
    def sequence(self):
        return self.peptide.sequence

    @property
    def mods(self):
        return self.peptide.modifications

    def get_source_statistic(self, name, default=None):
        return self.source_statistics.get(name, default)


class PsmManager(object):

    def __init__(self, psms):
        scans_references_by_source = {}

        for psm in psms:
            scan_reference = psm.scan_reference
            scan_source = scan_reference.source
            if not scan_source in scans_references_by_source:
                scans_references_by_source[scan_source] = []
            scans_references_by_source[scan_source].append(psm)

        self.scans_references_by_source = scans_references_by_source

    def psms_for_scan(self, scan):
        scan_source = scan.source
        possible_psms = self.scans_references_by_source[scan_source]
        psms = []
        for possible_psm in possible_psms:
            if possible_psm.scan_reference.matches_scan_from_same_source(scan):
                psms.append(possible_psm)
        return psms
