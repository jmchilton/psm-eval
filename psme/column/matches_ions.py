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
        '''
        print [any([ion_matcher(ion, peak) for peak in peaks]) for ion in ions]
        print "Peaks: ===================================" 
        print peaks
        print "Ions: =================================="
        print [ion.peptide_context for ion in ions]
        print [ion.label for ion in ions] 
        '''
        def find_most_intense_peak(ion):
            all_matching_peaks = [peak for peak in peaks if ion_matcher(ion, peak)]
            if not all_matching_peaks:
                return None
            return map(float, max(all_matching_peaks, key=lambda x: x[1]))[0]
        ion_peak_pairs = filter(lambda peak_ion_pair: peak_ion_pair[0], zip(map(find_most_intense_peak, ions), ions))
        return [x[1] for x in ion_peak_pairs], [(x[0], x[1].label) for x in ion_peak_pairs]

    def _peaks_matched(self, ions, peaks):
        # Probably not expected behavior
        ion_matcher = self.ion_matcher
        return [any([ion_matcher(ion, peak) for ion in ions]) for peak in peaks]
