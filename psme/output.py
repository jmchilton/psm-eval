from __future__ import print_function
from sys import stdout as sys_stdout


class OutputFormatter(object):

    def __init__(self, settings, stdout=sys_stdout):
        self.output = settings.get('output', None)
        self.stdout = stdout

    def __enter__(self):
        output = self.output
        if output:
            self.file = open(output, "w")
            self.close = True
        else:
            self.file = self.stdout
            self.close = False
        return self

    def __exit__(self, type, value, traceback):
        if self.close:
            self.file.close()

    def write_line(self, values):
        line = "\t".join(map(str, values))
        print(line, file=self.file)
