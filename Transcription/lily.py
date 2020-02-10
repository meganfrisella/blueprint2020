import abjad
import yeyemoney as y


def convert(note):
    new_note = note[0].lower()
    if len(note) == 3:
        new_note += note[-1]
    for i in range(int(note[1]) - 3):
        new_note += "'"
    return new_note


def show_chord(pitch, duration, c):
    for i in range(int(duration / 4)):
        chord = abjad.Chord()
        chord.written_pitches = tuple([convert(i) for i in pitch])
        chord.written_duration = abjad.Duration(int(duration / 4), 4)
        c.extend([chord])
    if duration % 4 != 0:
        chord = abjad.Chord()
        chord.written_pitches = tuple([convert(i) for i in pitch])
        chord.written_duration = abjad.Duration(duration % 4, 4)
        c.extend([chord])


def main():
    freqs, freq_to_amp = y.record(5, 2, 10)
    readings = list()
    for reading in freqs:
        cr_reading = y.CustomRound(reading)
        temp = y.clst(reading, 0.98, 1.02)
        temp.sort(key=lambda elem: freq_to_amp[cr_reading(elem)])
        temp2 = temp[-3:]
        temp2.sort()
        readings.append(temp2[-3:])
    chords = y.convList(readings)

    c = abjad.Container()
    time = 1
    prev = chords[0]
    for i in range(len(chords) - 1):
        i += 1
        a = chords[i]
        if prev != a:
            show_chord(prev, time, c)
            prev = a
            time = 1
        else:
            time += 1
    show_chord(chords[-1], time, c)
    abjad.show(c)


if __name__ == '__main__':
    main()

