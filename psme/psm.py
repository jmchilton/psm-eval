

class Psm(object):

    def __init__(self, scan_reference, peptide, source_statistics={}, rt=None):
        self.scan_reference = scan_reference
        self.source_statistics = source_statistics
        self.peptide = peptide
        self.rt = rt

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
        mapper = None

        for psm in psms:
            if mapper == None:
                if psm.scan_reference:
                    mapper = ScanPsmMapper()
                elif psm.rt:
                    mapper = RtPsmMapper()
                else:
                    raise Exception("PSM must specify scan_reference or RT.")
            mapper.add(psm)
        self.mapper = mapper

    def psms_for_scan(self, scan):
        return self.mapper.get(scan)


class ScanPsmMapper(object):

    def __init__(self):
        self.scans_references_by_source = {}
        pass

    def add(self, psm):
        scan_reference = psm.scan_reference
        scan_source = scan_reference.source
        if not scan_source in self.scans_references_by_source:
            self.scans_references_by_source[scan_source] = []
        self.scans_references_by_source[scan_source].append(psm)

    def get(self, scan):
        scan_source = scan.source
        possible_psms = self.scans_references_by_source.get(scan_source, [])
        psms = []
        for possible_psm in possible_psms:
            if possible_psm.scan_reference.matches_scan_from_same_source(scan):
                psms.append(possible_psm)
        return psms


class RtPsmMapper(object):

    def __init__(self):
        self.psms_by_rt = {}

    def add(self, psm):
        rt = psm.rt
        if rt in self.psms_by_rt:
            raise Exception("Found two PSMs with same RT - %f" % rt)
        self.psms_by_rt[rt] = psm

    def get(self, scan):
        rt = scan.rt
        return self.psms_by_rt[rt]
