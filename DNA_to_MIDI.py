import pandas as pd
from midiutil import MIDIFile
import more_itertools as mit
from random import randrange
from forms import GENOMES

SIXTEENTH_NOTE = 0.25
SIXTEENTH_NOTES_IN_MEASURE = 16
AMINO_ACIDS = 20
OCTAVE_RANGE = 5
NOTES_IN_SCALE = 7
NOTES_IN_OCTAVE = 12
VOLUME = 200
MIDI_FILE_PREFIX = "static/"
GENOME_FILE_PREFIX = "genomes/"
FREQUENCY = 44100    # audio CD quality
BITSIZE = -16   # unsigned 16 bit
CHANNELS = 2    # 1 is mono, 2 is stereo
BUFFER = 1024    # number of samples
SCALES = ['Major', 'Minor']


def codon_dataframe():
    codon_df = pd.read_csv('codon_table.csv', header=None, names=['Codon', 'Abv', 'Code', 'Name'])
    codon_df['Code'].replace({'Stop': 'Z'}, inplace=True)
    return codon_df


CODON_DF = codon_dataframe()
TRANSCRIPTION_DICTIONARY = dict(zip(CODON_DF["Codon"], CODON_DF["Code"]))
TRANSLATION_DICTIONARY = {"C": "G", "G": "C", "T": "A", "A": "U"}
KEYS_DICTIONARY = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6,
                   "G": 7, "G#": 8, "A": 9, "Bb": 10, "B": 11}


def genome_preprocessing(dna):
    dna = ''.join(dna.split('\n'))
    remainder = len(dna) % 3
    if remainder == 0:
        return dna.upper()
    else:
        return dna[:(-remainder)].upper()


def translation(dna):
    rna = dna.translate(dna.maketrans(TRANSLATION_DICTIONARY))
    rna_codons = [rna[i:i + 3] for i in range(0, len(rna), 3)]
    return rna_codons


def transcription(rna):
    protein = [TRANSCRIPTION_DICTIONARY[i] for i in rna]
    return protein


def get_note(triplet, key, scale):
    note_properties = [ord(i) for i in triplet]
    duration = (note_properties[0] % AMINO_ACIDS) * SIXTEENTH_NOTE
    octave = note_properties[1] % OCTAVE_RANGE + 3
    degree = note_properties[2] % NOTES_IN_SCALE
    key_translation = KEYS_DICTIONARY[key]
    pitch = get_major_pitch(degree, key_translation) if scale == "major" else get_minor_pitch(degree, key_translation)
    pitch += octave * NOTES_IN_OCTAVE
    return duration, pitch


def get_major_pitch(degree, key):
    half_steps = 0 if 0 < degree < 3 else 1
    note = key + 2 * (degree - half_steps) + half_steps
    return note


def get_minor_pitch(degree, key):
    if 0 < degree < 2:
        half_steps = 0
    elif 2 < degree < 5:
        half_steps = 1
    else:
        half_steps = 2
    note = key + 2 * (degree - half_steps) + half_steps
    return note


def create_note_sequence(protein, key, scale):
    codon_index = 0
    note_sequence = []
    while codon_index < len(protein):
        if codon_index + 3 < len(protein):
            note_ = get_note(protein[codon_index:codon_index + 3], key, scale)
            note = {'duration': note_[0], 'pitch': note_[1]}
            note_sequence.append(note)
        codon_index += 1
    return note_sequence


def track_preprocessing(tempo=160, channel=0, tracks=6, time=0):
    midi = MIDIFile(tracks, deinterleave=False)
    for track in range(tracks):
        midi.addTempo(track, time, tempo)
    return midi, channel, tracks


def create_midi(genome, note_sequence, key, scale):
    midi, channel, tracks = track_preprocessing()
    track = 0
    partitions = [list(note) for note in mit.divide(tracks, note_sequence)]
    for partition in partitions:
        time = 0
        for note in partition:
            midi.addNote(track, channel, note['pitch'], time, note['duration'], VOLUME)
            time += note['duration']
        track += 1
    file_name = MIDI_FILE_PREFIX + '-'.join([genome, key, scale]) + ".mid"
    with open(file_name, "wb") as file:
        midi.writeFile(file)
    file.close()
    return file_name


def read_genome(genome):
    file_name = GENOME_FILE_PREFIX + genome + ".txt"
    with open(file_name, "r") as file:
        dna = file.read()
    file.close()
    return genome_preprocessing(dna)


def get_protein(dna):
    rna = translation(dna)
    protein = transcription(rna)
    return protein


def start(genome, key, scale):
    dna = read_genome(genome)
    protein = get_protein(dna)
    note_sequence = create_note_sequence(protein, key, scale)
    return create_midi(genome, note_sequence, key, scale)


def surprise_me():
    genome = randrange(1, len(GENOMES) - 1, 1)
    key = randrange(0, len(KEYS_DICTIONARY) - 1, 1)
    scale = randrange(0, len(SCALES) - 1, 1)
    return GENOMES[genome][0], list(KEYS_DICTIONARY.keys())[key], SCALES[scale]




