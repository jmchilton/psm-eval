from .source import load_psms
from .psm import PsmManager
from .column import build_column_providers
from .peak_list import ScanSourceManager
from .output import OutputFormatter

# Not using this function now so can change to whatever needed to accommodate galaxy
def evaluate(settings, output_formatter=OutputFormatter):
    """
    Collect statistics about each PSM and write out to file
    based on output_formatter.
    """
    collected_statistics = collect_statistics(settings)
    with output_formatter(settings) as output:
        output.write_row(columns)


def collect_statistics(settings):
    """
    Build data structure describing statistics for each PSM.
    """
    columns = build_column_providers(settings)
    source_statistic_names = __find_referenced_source_statistics(columns)
    scan_source_manager = ScanSourceManager(settings)
    psms = load_psms(settings, scan_source_manager, source_statistic_names)
    psm_manager = PsmManager(psms) 
    return __collect_statistics(scan_source_manager, psm_manager, columns) 


def __find_referenced_source_statistics(columns):
    source_statistic_names = set()
    for column in columns:
        source_statistic_name = getattr(column, 'source_statistic_name', None)
        if source_statistic_name:
            source_statistic_names.add(source_statistic_name)
    return list(source_statistic_names)


def __collect_statistics(scan_source_manager, psm_manager, statistics):
    psms_statistics = []
    for scan in scan_source_manager.get_scans():
        for psm in psm_manager.psms_for_scan(scan):
            psm_statistics = __psm_statistics(scan, psm, statistics)
            psms_statistics.append(psm_statistics)
    return psms_statistics


def __psm_statistics(scan, psm, statistics):
    return [statistic.calculate(scan, psm) for statistic in statistics]
