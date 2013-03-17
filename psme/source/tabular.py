from csv import reader

CSV_OPT_NAMES = ['delimiter', 'escapechar', 'skipinitialspace']


class TabularLoader(object):

    def __init__(self, settings):
        self.__init_csv_opts(settings)

    def __init_csv_opts(self, settings):
        csv_opts = {'delimiter': '\t'}
        for csv_opt_name in CSV_OPT_NAMES:
            if csv_opt_name in settings:
                csv_opts[csv_opt_name] = settings[csv_opt_name]
        self.csv_opts = csv_opts

    def load(self, f, source_statistic_names):
        psms = []
        row_parser = self._get_row_parser(source_statistic_names)
        for row in reader(f, **self.csv_opts):
            if not row:
                continue
            psm = row_parser.get_psm(row)
            if psm:
                psms.append(psm)
        return psms

    def _get_row_parser(self, source_statistic_names):
        raise NotImplementedError()
