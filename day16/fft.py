class FFT:
    def __init__(self, input_signal, length=None):
        self.input_signal = [int(c) for c in input_signal]
        self.memo = dict()
        if length is None:
            self.length = len(self.input_signal)
        else:
            self.length = length
        self.calls = 0
        self.calcs = 0

    def calculate_digit(self, phase, n):
        if phase == 0:
            index = n % len(self.input_signal)
            return self.input_signal[index]

        self.calls += 1
        if (phase, n) in self.memo:
            return self.memo[(phase, n)]

        step = (n + 1) * 4
        total = 0
        for offset in range(n+1):
            index = n + offset
            while index < self.length:
                total += self.calculate_digit(phase-1, index)
                index += step
            index = 3 * n + 2 + offset
            while index < self.length:
                total -= self.calculate_digit(phase-1, index)
                index += step
        total = abs(total) % 10
        self.memo[(phase, n)] = total

        self.calcs += 1
        return total

    def stats(self, fh):
        print >> fh, "{} for {}".format(self.calcs, self.calls)
