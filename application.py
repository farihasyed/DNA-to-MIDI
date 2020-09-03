from flask import Flask, render_template, request, flash, url_for, redirect, session, make_response
from forms import Music
from DNA_to_MIDI import start, surprise_me
import os


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ["SECRET_KEY"])
    return app


app = create_app()
if __name__ == "__main__":
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Music()
    if request.method == 'POST':
        genome = form.genome.data
        if genome == "random":
            genome, key, scale = surprise_me()
        else:
            key = form.key_scale.key.data
            scale = form.key_scale.scale.data
        flash(' '.join(["Now playing", genome, "in", key, scale]))
        audio = start(genome, key, scale)
        return render_template('index.html', form=form, audio=audio)
    return render_template('index.html', form=form)



