import xml.etree.ElementTree as ET
from psme.psm import Psm
from psme.peptide import Peptide


class IdXmlLoader(object):

    def __init__(self, settings, scan_source_manager):
        self.settings = settings
        self.scan_source_manager = scan_source_manager

    def load(self, f, source_statistic_names):
        psms = []
        tree = ET.parse(f)
        peptide_identification_els = tree.getroot().find("IdentificationRun").findall("PeptideIdentification")
        for peptide_identification_el in peptide_identification_els:
            rt = peptide_identification_el.get("RT")
            peptide_hit_els = peptide_identification_el.findall("PeptideHit")
            for peptide_hit_el in peptide_hit_els:
                sequence = peptide_hit_el.get("sequence")
                score = peptide_hit_el.get("score")
                peptide = self._sequence_to_peptide(sequence)
                source_statistics = {"openms": float(score)}
                psm = Psm(scan_reference=None,
                          peptide=peptide,
                          rt=float(rt),
                          source_statistics=source_statistics)
                psms.append(psm)
        return psms

    def _sequence_to_peptide(self, sequence):
        if "(" in sequence:
            assert False, "OpenMS parser does not yet support modifications"
        return Peptide(sequence=sequence)
