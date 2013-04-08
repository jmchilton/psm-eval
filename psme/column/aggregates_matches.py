AGGREGATE_ION_METHODS = ['count', 'count_longest_stretch', 'percent', 'count_missed', 'percent_missed', 'list_matches', 'list_misses']
AGGREGATE_PEAKS_METHODS = ['count', 'percent', 'count_missed', 'percent_missed']


class AggregatesMatches(object):
    """

    >>> object = AggregatesMatches()
    >>> object._setup_aggregate_by(aggregate_what='ions', aggregate_by='count')
    >>> object._aggregate([True, False, True])
    2
    >>> object._aggregate([False, False, False])
    0
    >>> object._setup_aggregate_by(aggregate_what='ions', aggregate_by='count_longest_stretch')
    >>> object._aggregate([True, False, True, True, True, False, True, True])
    3
    >>> object._aggregate([False, False, False])
    0
    >>> object._aggregate([True, False, False])
    1
    >>> object._aggregate([True, True, True])
    3
    >>> object._setup_aggregate_by(aggregate_what='ions', aggregate_by='percent')
    >>> object._aggregate([False, False])
    0.0
    >>> object._aggregate([True, True])
    1.0
    >>> object._aggregate([True, False])
    0.5
    """
    def _setup_aggregate_by(self, aggregate_what, **kwds):
        # Parse out who to aggregate matches - count, count longest stretch, of compute percent matched.
        aggregate_by = kwds.get('aggregate_by', 'count')
        if aggregate_what == 'ions':
            aggregate_methods = AGGREGATE_ION_METHODS
        else:  # aggregate_what == 'peaks':
            aggregate_methods = AGGREGATE_PEAKS_METHODS
        if aggregate_by not in aggregate_methods:
            self._raise_cannot_aggregate_by(aggregate_by)
        self.aggregate_by = aggregate_by

    def _raise_cannot_aggregate_by(self, aggregate_by):
        raise Exception("Statistic doesn't know how to aggregate by [%s]." % aggregate_by)

    def _divide(self, num, den):
        if float(den) != 0.0:
            return float(num) / float(den)
        else:
            return float('nan')

    def _aggregate(self, matched, ions=None):
        if self.aggregate_by == 'count':
            return self._count_matched(matched)
        elif self.aggregate_by == 'count_missed':
            return self._count_missed(matched)
        elif self.aggregate_by == 'percent':
            num_matched = len(matched)
            return self._divide(self._count_matched(matched), num_matched)
        elif self.aggregate_by == 'percent_missed':
            num_matched = len(matched)
            return self._divide(self._count_missed(matched), num_matched)
        elif self.aggregate_by == 'count_longest_stretch':
            return self._longest_stretch(matched)
        elif self.aggregate_by == 'list_matches':
            return ",".join([ion.label for (was_matched, ion) in zip(matched, ions) if was_matched])
        elif self.aggregate_by == 'list_misses':
            return ",".join([ion.label for (was_matched, ion) in zip(matched, ions) if not was_matched])
        else:
            self._raise_cannot_aggregate_by(self.aggregate_by)

    def _count_matched(self, matched):
        return len([1 for match in matched if match])

    def _count_missed(self, matched):
        return len([1 for match in matched if not match])

    def _longest_stretch(self, values):
        longest_stretch = 0
        current_stretch = 0
        for value in values:
            if value:
                current_stretch += 1
                longest_stretch = max(longest_stretch, current_stretch)
            else:
                current_stretch = 0
        return longest_stretch
