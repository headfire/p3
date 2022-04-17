import sys


class Env:
    def __init__(self):
        self.envParams = {}
        for param in sys.argv:
            key, sep, val = param.partition('=')
            if val != '':
                try:
                    self.envParams[key] = int(val)
                except ValueError:
                    print('Non int param')

    def env(self, paramName, defaultValue):
        if paramName in self.envParams:
            return self.envParams[paramName]
        else:
            return defaultValue
