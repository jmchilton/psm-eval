from os.path import join, dirname, pardir, exists
from pyteomics.mass import Unimod


def load_unimod(settings):
    unimod_path = settings.get("unimod_path", None)
    if not unimod_path:
        local_unimod_path = join(dirname(__file__), pardir, 'unimod.xml')
        if exists(local_unimod_path):
            unimod_path = local_unimod_path

    unimod_opts = {}
    if unimod_path:
        unimod_opts['source'] = "file://%s" % unimod_path

    return Unimod(**unimod_opts)
