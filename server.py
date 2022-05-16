import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template(
        'welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    allowedToBook = 12
    placesAvailable = int(competition['numberOfPlaces'])
    placesRequired = int(request.form['places'])
    # Bug #3 fixed - the max number of places to book, is either 12 or,
    # if smaller, the available places left!
    if placesRequired <= allowedToBook:
        if placesRequired <= placesAvailable:
            competition['numberOfPlaces'] = placesAvailable - placesRequired
            flash('Great-booking complete!')
            return render_template(
                'welcome.html', club=club, competitions=competitions)
        flash(f'{competition["name"]} has only {placesAvailable} places left.')
        return render_template(
            'booking.html', club=club, competition=competition)
    flash(f'Sorry, its not allowed to book more than {allowedToBook} places.')
    return render_template(
            'booking.html', club=club, competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
