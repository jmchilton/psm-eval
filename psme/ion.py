
from .loss import NO_LOSS, build_losses
from .peptide import PeptideContext

ION_TYPE_N_TERM = "n"
ION_TYPE_C_TERM = "c"
ION_TYPE_WHOLE = "w"
ION_TYPE_INTERNAL = "i"

ION_TYPES = {
    'a': ION_TYPE_N_TERM,
    'b': ION_TYPE_N_TERM,
    'c': ION_TYPE_N_TERM,
    'x': ION_TYPE_C_TERM,
    'y': ION_TYPE_C_TERM,
    'z': ION_TYPE_C_TERM,
    'internal': ION_TYPE_INTERNAL,
    'm': ION_TYPE_WHOLE,
}


class MainSeriesIterator(object):

    def __init__(self, peptide, ion_type):
        self.peptide = peptide
        self.ion_type = ion_type
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.peptide.sequence) - 1:
            raise StopIteration()
        self.index += 1
        context = PeptideContext(peptide=self.peptide, start=None, stop=self.index, term=self.ion_type)
        index = str(self.index + 1)
        return (context, index)


class InternalIonIterator(object):

    def __init__(self, peptide):
        self.peptide = peptide

    def __iter__(self):
        return self.__build_internal_contexts().__iter__()

    def __build_internal_contexts(self):
        # TODO: Test redundant filtering
        contexts = []
        labeled_sequences = set()
        for i in range(len(self.peptide.sequence) - 1):
            for j in range(i + 2, len(self.peptide.sequence)):
                context = PeptideContext(peptide=self.peptide, start=i, stop=j, term=None)
                labeled_sequence = context.labeled_sequence
                if not labeled_sequence in labeled_sequences:
                    contexts.append(context)
                    labeled_sequences.add(labeled_sequence)
        return [(context, "_%s" % context.sequence) for context in contexts]


class WholeIonIterator(object):

    def __init__(self, peptide):
        self.peptide = peptide

    def __iter__(self):
        context = PeptideContext(peptide=self.peptide, start=0, stop=len(self.peptide.sequence), term=None)
        return [(context, "")].__iter__()


class Ion(object):

    def __init__(self, peptide_context, type, index="", charge=1, loss=NO_LOSS, **calc_kwds):
        self.type = type
        self.peptide_context = peptide_context
        ion_type = calc_kwds["ion_type"]
        self.charge = charge
        self.label = "%s%s%s%s" % (ion_type, index, "+" * self.charge, loss.label)
        ion_type = "%s%s" % (ion_type, loss.label)
        calc_kwds["ion_type"] = ion_type
        self.calc_kwds = calc_kwds

    def get_mz(self):
        mass = self.peptide_context.calc_mass(**self.calc_kwds)
        charge = self.charge
        return (mass + charge * 1.00727646677) / charge


class IonBuilder(object):

    def __init__(self, type, charge=1, **calc_kwds):
        self.type = type
        self.charge = charge
        self.calc_kwds = calc_kwds

    def get(self, peptide_context, loss=NO_LOSS, index="", **calc_kwds):
        ion = Ion(peptide_context, type=self.type, charge=self.charge, loss=loss, index=index, **self.calc_kwds)
        ion.calc_kwds.update(**calc_kwds)
        return ion


class AIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(AIonBuilder, self).__init__(type=ION_TYPE_N_TERM, charge=charge, ion_type="a")


class BIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(BIonBuilder, self).__init__(type=ION_TYPE_N_TERM, charge=charge, ion_type="b")


class CIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(CIonBuilder, self).__init__(type=ION_TYPE_N_TERM, charge=charge, ion_type="c")


class XIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(XIonBuilder, self).__init__(type=ION_TYPE_C_TERM, charge=charge, ion_type="x")


class YIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(YIonBuilder, self).__init__(type=ION_TYPE_C_TERM, charge=charge, ion_type="y")


class ZIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(ZIonBuilder, self).__init__(type=ION_TYPE_C_TERM, charge=charge, ion_type="z")


class InternalIonBuilder(IonBuilder):

    def __init__(self):
        super(InternalIonBuilder, self).__init__(type=ION_TYPE_INTERNAL, charge=1, ion_type="M")


class WholeIonBuilder(IonBuilder):

    def __init__(self, charge=1):
        super(WholeIonBuilder, self).__init__(type=ION_TYPE_WHOLE, charge=charge, ion_type="M")


ION_SERIES = {
    'a1': AIonBuilder(1),
    'a2': AIonBuilder(2),
    'a3': AIonBuilder(3),
    'b1': BIonBuilder(1),
    'b2': BIonBuilder(2),
    'b3': BIonBuilder(3),
    'c1': CIonBuilder(1),
    'c2': CIonBuilder(2),
    'c3': CIonBuilder(3),
    'x1': XIonBuilder(1),
    'x2': XIonBuilder(2),
    'x3': XIonBuilder(3),
    'y1': YIonBuilder(1),
    'y2': YIonBuilder(2),
    'y3': YIonBuilder(3),
    'z1': ZIonBuilder(1),
    'z2': ZIonBuilder(2),
    'z3': ZIonBuilder(3),
    'internal': InternalIonBuilder(),
    'm1': WholeIonBuilder(1),
    'm2': WholeIonBuilder(2)
}


def get_ions(peptide, calc_args={}, **options):
    series_list = options.get("series", [])
    losses = build_losses(options.get("losses", []))
    ions = []
    for series in series_list:
        ion_builder = ION_SERIES[series]
        ion_type = ion_builder.type
        if ion_type in [ION_TYPE_N_TERM, ION_TYPE_C_TERM]:
            peptide_iter = MainSeriesIterator(peptide, ion_type)
        elif ion_type == ION_TYPE_INTERNAL:
            peptide_iter = InternalIonIterator(peptide)
        elif ion_type == ION_TYPE_WHOLE:
            peptide_iter = WholeIonIterator(peptide)
        else:
            raise NotImplementedError("ions of type [%s] not implemented." % ion_type)
        series_ions = []
        for peptide_context, index in peptide_iter:
            for loss in losses:
                if loss.applicable(ion_type, peptide_context):
                    series_ions.append(ion_builder.get(peptide_context, loss, index=index, **calc_args))
        if ion_type == ION_TYPE_C_TERM:
            series_ions.reverse()
        ions.extend(series_ions)
    return ions
