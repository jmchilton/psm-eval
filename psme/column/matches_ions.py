from .uses_ion_series import UsesIonSeries

from psme.constants import DEFAULT_MASS_TOLERANCE


class MatchesIons(UsesIonSeries):
    ## TODO: Optimize

    def _setup_ion_matcher(self, settings, **options):
        mass_tolerance = DEFAULT_MASS_TOLERANCE
        # Could be defined for this column provider or whole evaluation
        # process.
        if 'mass_tolerance' in options:
            mass_tolerance = float(options['mass_tolerance'])
        elif 'mass_tolerance' in settings:
            mass_tolerance = float(settings['mass_tolerance'])
        self.ion_matcher = \
            lambda ion, peak: abs(peak[0] - ion.get_mz()) < mass_tolerance

    def _ions_matched(self, ions, peaks):
        ion_matcher = self.ion_matcher
        return [any([ion_matcher(ion, peak) for peak in peaks]) for ion in ions]

    def _peaks_matched(self, ions, peaks):
        # Probably not expected behavior
        ion_matcher = self.ion_matcher
        return [any([ion_matcher(ion, peak) for ion in ions]) for peak in peaks]
