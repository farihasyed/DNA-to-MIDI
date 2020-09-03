from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FormField
from wtforms.validators import InputRequired

GENOMES = [("", "Select a Genome"), ("SARS-CoV", "SARS_CoV"), ("SARS-CoV-2", "SARS-CoV-2 (COVID-19)"), ("Influenza-A", "Influenza A (flu)"),
           ("Rhinovirus-A", "Rhinovirus A (common cold)"), ("MERS-CoV", "MERS-CoV"), ("random", "Surprise me!")]
KEYS = [('', 'Key'), ('C', 'C'), ('C#', 'C#'), ('D', 'D'), ('Eb', 'Eb'), ('E', 'E'), ('F', 'F'), ('F#', 'F#'),
        ('G', 'G'), ('G#', 'G#'), ('A', 'A'), ('Bb', 'Bb'), ('B', 'B')]
SCALE = [('', 'Scale'), ('major', 'Major'), ('minor', 'Minor')]
# eventually, add functionality for tempo


class ScaleForm(FlaskForm):
    key = SelectField('Key', choices=KEYS)
    scale = SelectField('Scale', choices=SCALE)


class Music(FlaskForm):
    play = SubmitField()
    genome = SelectField('Genome', choices=GENOMES, validators=[InputRequired()])
    key_scale = FormField(ScaleForm)



