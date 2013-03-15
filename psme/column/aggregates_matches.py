AGGREGATE_ION_METHODS = ['count', 'count_longest_stretch', 'percent', 'count_missed', 'percent_missed']
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

    def _aggregate(self, matched):
        if self.aggregate_by == 'count':
            return self._count_matched(matched)
        elif self.aggregate_by == 'count_missed':
            return self._count_missed(matched)
        elif self.aggregate_by == 'percent':
            return self._count_matched(matched) / (1.0 * len(matched))
        elif self.aggregate_by == 'percent_missed':
            return self._count_missed(matched) / (1.0 * len(matched))
        elif self.aggregate_by == 'count_longest_stretch':
            return self._longest_stretch(matched)
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
