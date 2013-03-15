from __future__ import print_function
from sys import stdout as sys_stdout


class OutputFormatter(object):

    def __init__(self, settings, stdout=sys_stdout):
        self.output = settings.get('output', None)
        output_format = settings.get('output_format', 'tsv')
        self.output_formatter = FORMATTERS[output_format](settings)
        self.stdout = stdout

    def __enter__(self):
        output = self.output
        if output:
            self.file = open(output, "w")
            self.close = True
        else:
            self.file = self.stdout
            self.close = False
        self.__write(self.output_formatter.start_table())
        return self

    def __exit__(self, type, value, traceback):
        self.__write(self.output_formatter.end_table())
        if self.close:
            self.file.close()

    def write_row(self, values):
        line = self.output_formatter.format_row(values)
        self.__write(line)
        self.__write("\n")

    def __write(self, content):
        self.file.write(content)


class TabularFormatter(object):

    def __init__(self, settings):
        pass

    def start_table(self):
        return ""

    def end_table(self):
        return ""

    def format_row(self, values):
        formatted_values = map(self._format_value, values)
        return self._combine_formatted_values(formatted_values)

    def _combine_formatted_values(self, formatted_values):
        return "\t".join(formatted_values)

    def _format_value(self, value):
        value_type = getattr(value, 'value_type', 'str')
        if value_type == 'link':
            return value.url
        else:
            return str(value)


class HtmlFormatter(TabularFormatter):

    def __init__(self, settings):
        super(HtmlFormatter, self).__init__(settings)

    def start_table(self):
        return "<table>"

    def end_table(self):
        return "</table>"

    def _combine_formatted_values(self, formatted_values):
        cells = "".join(map(lambda value: "<td>%s</td>" % value, formatted_values))
        return '''<tr>%s</tr>''' % cells

    def _format_value(self, value):
        value_type = getattr(value, 'value_type', 'str')
        if value_type == 'link':
            return '''<a href="%s">%s</a>''' % (value.url, value.label)
        else:
            return str(value)


FORMATTERS = {
    'tsv': TabularFormatter,
    'html': HtmlFormatter,
}