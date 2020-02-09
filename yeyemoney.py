import numpy as np
from microphone import record_audio
from microphone import play_audio
import matplotlib.pyplot as plt
from bisect import bisect_left

freq_to_note = {
    220: "A3",
    233: "B3f",
    247: "B3",
    262: "C4",
    277: "C4s",
    294: "D4",
    311: "E4f",
    330: "E4",
    349: "F4",
    370: "F4s",
    392: "G4",
    415: "A4f",
    440: "A4",
    466: "B4f",
    494: "B4",
    523: "C5",
    554: "C5s",
    587: "D5",
    622: "E5f",
    659: "E5",
    698: "F5",
    740: "F5s",
    784: "G5",
    831: "A5f",
    880: "A5",
    932: "B5f",
    988: "B5",
    1047: "C6",
    1109: "C6s",
    1175: "D6",
    1245: "E6f",
    1319: "E6",
    1397: "F6",
    1480: "F6s",
    1568: "G6",
    1661: "A6f",
    1760: "A6"
}


class CustomRound:
    def __init__(self, values):
        self.compare = sorted(values)

    def __call__(self, x):
        compare = self.compare
        ndata = len(compare)
        idx = bisect_left(compare, x)
        if idx <= 0:
            return compare[0]
        elif idx >= ndata:
            return compare[ndata - 1]
        x0 = compare[idx - 1]
        x1 = compare[idx]
        if abs(x - x0) < abs(x - x1):
            return x0
        return x1


class Note:
    def __init__(self, freq):
        self.frequency = freq
        self.note = freq_to_note[cr_notes(freq)]
        self.letter = self.note[0]
        self.octave = self.note[1]
        if len(self.note) == 3:
            self.fs = self.note[2]


cr_notes = CustomRound(freq_to_note.keys())


def find_note(freq):
    return freq_to_note[cr_notes(freq)]


def record(duration, readings_per_second, num_notes):
    frames, sample_rate = record_audio(duration)
    # print(frames)
    audio_data = np.hstack([np.frombuffer(i, np.int16) for i in frames])

    audio_data = audio_data[:(duration * readings_per_second * (len(audio_data) // (duration * readings_per_second)))]
    audio_split = audio_data.reshape(duration * readings_per_second,
                                     len(audio_data) // (duration * readings_per_second))

    frequencies = np.zeros((duration * readings_per_second, num_notes))
    freq_to_amp = {}

    for idx, item in enumerate(audio_split):
        c = np.abs(np.fft.rfft(item))

        c_sort = np.sort(c)
        threshhold = c_sort[-num_notes]
        c_new = np.copy(c)
        c_new[c_new < threshhold] = 0

        T = 1 / readings_per_second
        N = len(item)
        k = np.arange(N // 2 + 1)
        f = k / T

        fig, ax = plt.subplots()
        ax.plot(f, c, c_new)
        ax.set_xlim(0, 1000)
        ax.set_ylabel(r"$| c_{k} |$")
        ax.set_xlabel("Frequency (Hz)")

        top = np.zeros(num_notes)
        count = 0
        for index, item in enumerate(c_new):
            if item > 0:
                freq_to_amp[f[index]] = item
                top[count] = f[index]
                count += 1

        frequencies[idx] = top
    return frequencies, freq_to_amp


def clst(arr, ThreshL, ThreshR):
    arr = sorted(arr)
    res = np.array([])
    prev = np.array(arr[0], dtype=np.double)
    for i in range(len(arr) - 1):
        i += 1
        if ThreshL < arr[i] / arr[i - 1] < ThreshR:
            prev = np.append(prev, arr[i])
        else:
            res = np.append(res, np.mean(prev))
            prev = np.array(arr[i], dtype=np.double)
    res = np.append(res, np.mean(prev))
    return [np.mean(i) for i in res]


def convList(entry):
    out = []
    for reading in entry:
        chord = []
        for freq in reading:
            temp = Note(freq)
            if temp.note != "A3":
                chord.append(temp.note)
        out.append(chord)
    return out


def main():
    t = 15
    freqs, freq_to_amp = record(t, 2, 10)
    readings = list()
    for reading in freqs:
        cr_reading = CustomRound(reading)
        temp = clst(reading, 0.98, 1.02)
        temp.sort(key=lambda elem: freq_to_amp[cr_reading(elem)])
        temp2 = temp[-3:]
        temp2.sort()
        readings.append(temp2[-3:])

    print(convList(readings))


# if __name__ == '__main__':
#     main()
