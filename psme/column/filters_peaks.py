from psme.spectra_utils import tic
from numpy import array_split, min, sort


class FiltersPeaks(object):

    def _setup_peak_filters(self, **options):
        filter_options = options.get('peak_filters', []) or []
        peak_filter_factories = []
        for filter_option in filter_options:
            filter_type = filter_option.get('type')
            filter_factory_class = FILTER_FACTORY_CLASSES[filter_type]
            filter_factory = filter_factory_class(**filter_option)
            peak_filter_factories.append(filter_factory)
        self.peak_filter_factories = peak_filter_factories

    def _peaks(self, scan):
        return zip(scan.mz_array, scan.intensity_array)

    def _filtered_peaks(self, scan):
        filters = []
        for peak_filter_factory in self.peak_filter_factories:
            filters.append(peak_filter_factory.get(scan))
        return [peak for peak in self._peaks(scan) if all([filter(peak) for filter in filters])]


class PercentTicFilterFactory(object):

    def __init__(self, **filter_options):
        super(PercentTicFilterFactory, self).__init__()
        self.percent_tic = filter_options.get('percent', 0.0)

    def _get_intensity_threshold(self, scan):
        return tic(scan) * self.percent_tic

    def get(self, scan):
        intensity_threshold = self._get_intensity_threshold(scan)
        return lambda peak: peak[1] > intensity_threshold


class QuantileFilterFactory(PercentTicFilterFactory):

    def __init__(self, **filter_options):
        super(QuantileFilterFactory, self).__init__(**filter_options)
        self.q = filter_options.get("q", 2)
        self.k = filter_options.get("k", 1)  # 1 <= k <= q

    def _get_intensity_threshold(self, scan):
        intensity_array = scan.intensity_array
        intensity_threshold = tic(scan) * self.percent_tic
        intensity_array = intensity_array[intensity_array > intensity_threshold]
        return min(array_split(sort(intensity_array), self.q)[self.q - self.k])


class RangeThresoldFilterFactory(object):

    def __init__(self, **filter_options):
        super(RangeThresoldFilterFactory, self).__init__()
        self.min = filter_options.get('min', None)
        self.max = filter_options.get('max', None)


class MzRangeFilterFactory(RangeThresoldFilterFactory):

    def get(self, scan):
        min = self.min
        max = self.max
        return lambda peak: (min == None or peak[0] >= min) and (max == None or peak[0] < max)


class IntensityRangeFilterFactory(RangeThresoldFilterFactory):

    def get(self, scan):
        min = self.min
        max = self.max
        return lambda peak: (min == None or peak[1] >= min) and (max == None or peak[1] < max)


FILTER_FACTORY_CLASSES = {
    "percent_tic": PercentTicFilterFactory,
    "quantile": QuantileFilterFactory,
    "mz_range": MzRangeFilterFactory,
    "intensity_range": IntensityRangeFilterFactory,
}
