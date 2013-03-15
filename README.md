# PSM Evaluator

Typically proteomic search engines produce a single number used to
rank each peptide-spectrum-match. The purpose of this tool is to allow
re-evaluation of these matches using any number of flexiable criteria
chosen by the user in a search engine independent manner.

The goal to reduce a large number of PSMs to a smaller number of PSMs
the researcher is more confident about, perhaps as a precursor to
manual visual validation or additional experimentation.

## Dependencies

The python dependencies for PSM Evaluator are listed in
`requiements.txt`. 

### Linux and MacOS

1. Install [virtualenv]:

        pip install virtualenv

2. Create a new Python environment:

        virtualenv -q --no-site-packages .venv

3. Activate environment:

        . .venv/bin/activate

4. Install required dependencies into this virtual environment:

        pip install -r requirements.txt

For this to work you may have to install some native packages such as
`libxml2-dev` and `libyaml-dev`.

### Windows

You will likely want to use [these instructions][install_pyteomics] to
install [Pyteomics][pyteomics] and its dependencies and then download
and install the [pyyaml library][pyyaml_install].

## Usage (Command-line)

Using `settings_example.yaml` as an example build a settings file
(lets call it `settings.yaml`). Then execute the main driver program
as follows:

    python psme/main.py --settings settings.yaml

## Development

Fork [this project][fork] on [github][github]. Modify and run tests.:

    pip install nosetests  # only need to do this first time.
    nosetests


[virtualenv]: http://www.virtualenv.org/en/latest/#installation
[pyteomics_install]: http://pythonhosted.org/pyteomics/installation.html
[pyyaml_install]: http://pyyaml.org/wiki/PyYAML
[pyteomics]: http://pythonhosted.org/pyteomics/intro.html
[fork]: https://github.com/jmchilton/psm-eval/fork
[github]: https://github.com
