from .aggregates_matches import AggregatesMatches
from .filters_peaks import FiltersPeaks
from .matches_ions import MatchesIons
from .link import find_link_builder
from psme.spectra_utils import tic


def build_column_providers(settings):
    columns = []
    for column_options in settings.get("columns"):
        column_type = column_options["type"]
        column = build_column_provider(settings, column_type, column_options)
        columns.append(column)
    
    # build scan number column
    scancol = build_column_provider(settings, 'scan_number', column_options)
    columns.append(scancol)

    # build matched pairs column
    for column_options in settings.get("columns"):
        if column_type == column_options["type"]:
            matched = build_column_provider(settings, 'matched_pairs', column_options)
            columns.append(matched)
    
    return columns


def build_column_provider(settings, column_type, options={}):
    column_provider_class = COLUMN_PROVIDER_CLASSES[column_type]
    options.update({'settings': settings})
    column_provider = column_provider_class(**options)
    return column_provider

COLUMN_PROVIDER_CLASSES = {}


class ColumnProvider(object):
    """ Base class for simple statistics to collect. """

    def __init__(self, **kwds):
        pass

    def calculate(self, spectra, psm):
        """ Return list of pairs or dictionary of statics
        collected for this PSM."""
        return []


def register_column_provider(name):
    def register(cls):
        COLUMN_PROVIDER_CLASSES[name] = cls
        cls.column_provider_name = name
        return cls
    return register


@register_column_provider(name="peptide")
class PeptideColumnProvider(ColumnProvider):

    def __init__(self, **kwds):
        super(PeptideColumnProvider, self).__init__(**kwds)

    def calculate(self, spectra, psm):
        return psm.peptide.sequence


@register_column_provider(name="scan_id")
class ScanIdColumnProvider(ColumnProvider):

    def __init__(self, **kwds):
        super(ScanIdColumnProvider, self).__init__(**kwds)

    def calculate(self, scan, psm):
        return scan.id


@register_column_provider(name="scan_number")
class ScanNumberColumnProvider(ColumnProvider):

    def __init__(self, **kwds):
        super(ScanNumberColumnProvider, self).__init__(**kwds)

    def calculate(self, scan, psm):
        return scan.number


@register_column_provider(name="scan_index")
class ScanIndexColumnProvider(ColumnProvider):

    def __init__(self, **kwds):
        super(ScanIndexColumnProvider, self).__init__(**kwds)

    def calculate(self, scan, psm):
        return scan.index


@register_column_provider(name="scan_source")
class ScanSourceColumnProvider(ColumnProvider):

    def __init__(self, **kwds):
        super(ScanSourceColumnProvider, self).__init__(**kwds)

    def calculate(self, scan, psm):
        return scan.source.name


@register_column_provider(name="ions_matched")
class IonsMatched(ColumnProvider, AggregatesMatches, FiltersPeaks, MatchesIons):

    def __init__(self, settings, **kwds):
        super(IonsMatched, self).__init__(**kwds)
        self._setup_aggregate_by(aggregate_what='ions', **kwds)
        self._setup_peak_filters(**kwds)
        self._setup_ion_series(settings, **kwds)
        self._setup_ion_matcher(settings, **kwds)

    def calculate(self, spectra, psm):
        filtered_peaks = self._filtered_peaks(spectra)
        ions = self._get_ions(psm)
        matched, pairings = self._ions_matched(ions, filtered_peaks)
        return self._aggregate(matched, ions)


@register_column_provider(name="matched_pairs")
class MatchedPairs(ColumnProvider, AggregatesMatches, FiltersPeaks, MatchesIons):

    def __init__(self, settings, **kwds):
        super(MatchedPairs, self).__init__(**kwds)
        self._setup_aggregate_by(aggregate_what='ions', **kwds)
        self._setup_peak_filters(**kwds)
        self._setup_ion_series(settings, **kwds)
        self._setup_ion_matcher(settings, **kwds)

    def calculate(self, spectra, psm):
        filtered_peaks = self._filtered_peaks(spectra)
        ions = self._get_ions(psm)
	# return also matched peak, ion pairs        
	matched, pairings = self._ions_matched(ions, filtered_peaks)
	return pairings


@register_column_provider(name="num_peaks")
class NumPeaks(ColumnProvider, FiltersPeaks):

    def __init__(self, **kwds):
        super(NumPeaks, self).__init__(**kwds)
        self._setup_peak_filters(**kwds)

    def calculate(self, spectra, psm):
        filtered_peaks = self._filtered_peaks(spectra)
        return len(filtered_peaks)


@register_column_provider(name="peaks_matched")
class PeaksMatched(NumPeaks, MatchesIons, AggregatesMatches):

    def __init__(self, settings, **kwds):
        super(PeaksMatched, self).__init__(**kwds)
        self._setup_aggregate_by(aggregate_what='peaks', **kwds)
        self._setup_ion_series(settings, **kwds)
        self._setup_ion_matcher(settings, **kwds)

    def calculate(self, spectra, psm):
        filtered_peaks = self._filtered_peaks(spectra)
        ions = self._get_ions(psm)
        peaks_matched = self._peaks_matched(ions, filtered_peaks)
        return self._aggregate(peaks_matched)


@register_column_provider(name="total_ion_current")
class TotalIonCurrent(ColumnProvider):

    def __init__(self, settings, **kwds):
        super(TotalIonCurrent, self).__init__(**kwds)

    def calculate(self, spectra, psm):
        return tic(spectra)


@register_column_provider(name="source_statistic")
class SourceStatistic(ColumnProvider):

    def __init__(self, **kwds):
        super(SourceStatistic, self).__init__(**kwds)
        self.source_statistic_name = kwds['statistic_name']

    def calculate(self, spectra, psm):
        return psm.get_source_statistic(self.source_statistic_name, "")


@register_column_provider(name="link")
class Link(ColumnProvider):

    def __init__(self, settings, **kwds):
        super(Link, self).__init__(**kwds)
        self.link_builder = find_link_builder(**kwds)

    def calculate(self, scan, psm):
        return self.link_builder.get_link(scan, psm)


__all__ = [build_column_providers, build_column_provider]
