from psme.ion import get_ions

from psme.constants import DEFAULT_MASS_TYPE


class UsesIonSeries(object):
    """
    >>> uses_ions = UsesIonSeries()
    >>> uses_ions._setup_ion_series({}, **{"ions": {"series": ["m1"]}})
    >>> from psme.peptide import Peptide
    >>> class TestPsm(): peptide = Peptide("AM")
    >>> psm = TestPsm()
    >>> ion = uses_ions._get_ions(psm)[0]
    >>> round(ion.get_mz(), 4)
    221.0954
    >>> uses_ions._setup_ion_series({"mass_type": "average"}, **{"ions": {"series": ["y1"]}})
    >>> ion = uses_ions._get_ions(psm)[0]
    >>> round(ion.get_mz(), 4)
    150.2206
    """

    def _setup_ion_series(self, settings, **kwds):
        ion_options = kwds.get('ions', {}) or {}
        self.ion_options = ion_options

        if 'mass_type' in kwds:
            mass_type = kwds['mass_type']
        else:
            mass_type = settings.get('mass_type', DEFAULT_MASS_TYPE)
        self.calc_args = {'average': mass_type.lower().startswith('av')}

    def _get_ions(self, psm):
        return get_ions(psm.peptide, self.calc_args, **self.ion_options)
