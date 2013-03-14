from psme.loss import build_losses

from util import (TEST_PEPTIDE_CONTEXT_AMP,
                  TEST_PEPTIDE_CONTEXT_SAMPLER
                  )


def test_losses():
    losses = build_losses([])
    assert len(losses) == 1  # NO_LOSS

    losses = build_losses(["H2O", "CO"])

    assert losses[0].applicable('b', TEST_PEPTIDE_CONTEXT_AMP)
    # AMP Doesn't contain a 'S', 'T', 'E', or 'D'
    assert not losses[1].applicable('b', TEST_PEPTIDE_CONTEXT_AMP)

    # Contains an S
    assert losses[1].applicable('b', TEST_PEPTIDE_CONTEXT_SAMPLER)

    # CO loss applies only to internal ions
    assert not losses[2].applicable('b', TEST_PEPTIDE_CONTEXT_SAMPLER)
    assert losses[2].applicable('i', TEST_PEPTIDE_CONTEXT_SAMPLER)
