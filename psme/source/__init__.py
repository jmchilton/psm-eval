from .mzid import MzIdLoader
from .pepxml import PepXmlLoader
from .protein_pilot import ProteinPilotPeptideReportLoader
from .tpp_derived_report import TppDerivedReportLoader


DEFAULT_PSMS_TYPES = 'mzid'

PSM_LOADERS = {
    'mzid': MzIdLoader,
    'pepxml': PepXmlLoader,  # Not yet implemented.
    'proteinpilot_peptide_report': ProteinPilotPeptideReportLoader,
    'tpp_derived_report': TppDerivedReportLoader,
}


def load_psms(settings, scan_source_manager, source_statistic_names):
    psms_type = settings.get('psms_type', DEFAULT_PSMS_TYPES)
    psms_file = settings.get('psms')
    with open(psms_file, 'r') as f:
        return PSM_LOADERS[psms_type](settings, scan_source_manager).load(f, source_statistic_names)
