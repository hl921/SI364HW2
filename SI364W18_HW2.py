## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests
import json

#####################
##### APP SETUP #####
#####################


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug = True


####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def search_artist():
    return render_template('artistform.html')


### Part 1 (500 points)


@app.route('/artistinfo')
def artist_info():
    artist = request.args.get('artist')
    baseurl = "https://itunes.apple.com/search"
    artist_name = str(artist)
    artist_param = {"term":artist_name, "entity":"song"}
    response = requests.get(baseurl, params = artist_param)
    response_dict = json.loads(response.text)
    trackName = response_dict['results']
    return render_template('artist_info.html', artist=artist, objects=trackName)

@app.route('/artistlinks')
def artist_link():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_song(artist_name):
    baseurl = "https://itunes.apple.com/search"
    artistname = str(artist_name)
    artist_param = {"term":artistname, "entity":"song"}
    response = requests.get(baseurl, params = artist_param)
    response_dict = json.loads(response.text)
    results = response_dict['results']
    return render_template('specific_artist.html', results=results)



### Part 2 (300 points)


class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album:', validators=[Required()])

    rating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')], validators=[Required()])

    submit = SubmitField('Submit')


@app.route('/album_entry', methods = ['GET', 'POST'])
def album_entry():
    form = AlbumEntryForm()
    return render_template('album_entry.html',form=form)



@app.route('/album_result', methods = ['GET', 'POST'])
def result():
    form = AlbumEntryForm()
    if form.validate_on_submit():

        album = form.album.data
        rating = form.rating.data
    return render_template('album_data.html', album=album, rating=rating)
    flash(form.errors)
    return redirect(url_for('album_entry'))






if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
