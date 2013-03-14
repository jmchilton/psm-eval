
ALL_RESIDUES = object()
ALL_TYPES = object()


class Loss(object):

    def __init__(self, label="", residues=ALL_RESIDUES, types=ALL_TYPES):
        self.label = label
        self.residues = residues
        self.types = types

    def _contains_residues(self, peptide_context):
        applicable = True
        residues = self.residues
        if residues != ALL_RESIDUES:
            applicable = False
            sequence = peptide_context.sequence
            for residue in residues:
                if residue in sequence:
                    applicable = True
                    break
        return applicable

    def _applicable_ion_type(self, ion_type):
        return True if self.types == ALL_TYPES else (ion_type in self.types)

    def applicable(self, ion_type, peptide_context):
        return self._applicable_ion_type(ion_type) and self._contains_residues(peptide_context)


def build_losses(loss_options):
    losses = [NO_LOSS]
    loss_types = {'H2O': H2O_LOSS, 'NH3': NH3_LOSS, 'CO': CO_LOSS}
    for key, value in loss_types.iteritems():
        if key in loss_options:
            losses.append(value)
    return losses


NO_LOSS = Loss()
CO_LOSS = Loss("-CO", ALL_RESIDUES, ["i"])
NH3_LOSS = Loss("-NH3", ['R', 'K', 'Q', 'N'], ALL_TYPES)
H2O_LOSS = Loss("-H2O", ['S', 'T', 'E', 'D'], ALL_TYPES)

LOSSES = [NO_LOSS, CO_LOSS, NH3_LOSS, H2O_LOSS]
