from pyteomics.mass import calculate_mass, Composition


def mass_diff(amino_acid, mass):
    """

    >>> round(mass_diff("M", 147.04), 2)
    16.0
    """
    unmodified_mass = calculate_mass(composition=Composition(parsed_sequence=[amino_acid]))
    return mass - unmodified_mass
