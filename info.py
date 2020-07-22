class Info():
    def __init__(self, str):
        self.str = str

    def out_start(self):
        print(format('-', '-^160s'))
        print(format(self.str + ' started...', '^160'))
        print(format('-', '-^160s'))

    def out_end(self):
        print(format('-', '-^160s'))
        print(format(self.str + ' completed', '^160'))
        print(format('-', '-^160s'))


if __name__ == '__main__':
    s = Info("scan ip")
    s.out_start()
    s.out_end()