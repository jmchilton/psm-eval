from os.path import exists
from os import remove
from tempfile import NamedTemporaryFile
from StringIO import StringIO

from psme.driver import evaluate
from psme.output import OutputFormatter

from util import PsmeTestCase


class PeakListTestCase(PsmeTestCase):

    def test_driver_to_file(self):
        self.__test_driver(to_file=True)

    def test_driver_to_stdout(self):
        self.__test_driver(to_file=False)

    def __test_driver(self, to_file=True):
        column1 = {"type": "scan_id"}
        columns = [column1]

        input_path = self._test_data_path('test2.mzML')
        input_psms = self._test_data_path('test2.mzid')

        tf = NamedTemporaryFile(delete=False)
        output_path = tf.name
        remove(output_path)

        standard_output = StringIO()

        settings = {"peak_lists": [input_path],
                    "psms": input_psms,
                    "psms_type": "mzid",
                    "columns": columns,
                   }

        evaluate_kwds = {}
        if to_file:
            settings["output"] = output_path
        else:
            evaluate_kwds["output_formatter"] = lambda settings: OutputFormatter(settings, stdout=standard_output)

        self.assertFalse(exists(output_path))
        assert not standard_output.getvalue()

        evaluate(settings, **evaluate_kwds)

        if to_file:
            assert not standard_output.getvalue()
            self.assertTrue(exists(output_path))
            remove(output_path)
        else:
            assert standard_output.getvalue()
            self.assertFalse(exists(output_path))
