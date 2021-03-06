#!/usr/bin/env python
from psme.driver import evaluate
from psme.settings import load_settings


def main(evaluator=evaluate, settings_loader=load_settings):
    """
    Main entry point for command-line program. Loads settings and
    passes them along to `psme.driver:evaluate`.

    >>> settings_loader = lambda: {"test": "value"}
    >>> def evaluator(settings): assert settings["test"] == "value"
    >>> main(evaluator, settings_loader)
    """
    settings = settings_loader()
    evaluator(settings)

if __name__ == '__main__':
    main()
