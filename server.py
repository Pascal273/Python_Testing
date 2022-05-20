import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


MAX_ALLOWED_TO_BOOK = 12


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
    # Issue #1 fixed - the error is caught and handled,
    # an error message is will be displayed.
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template(
            'welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("Sorry, that email wasn't found!")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    # Bug #4 fixed - places in past competitions can't be booked,
    # error-message will be displayed instead of the booking page.
    competition_date_obj = datetime.strptime(
        foundCompetition["date"], '%Y-%m-%d %H:%M:%S').date()
    today_date_obj = datetime.today().date()

    if today_date_obj <= competition_date_obj:
        if foundClub and foundCompetition:
            return render_template(
                'booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template(
                'welcome.html', club=foundClub, competitions=competitions)
    flash('Sorry, but you cant book places on past competitions.')
    return render_template(
        'welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    placesAvailable = int(competition['numberOfPlaces'])

    # Bug #3 fixed - the max number of places to book, is either 12,
    if placesRequired <= MAX_ALLOWED_TO_BOOK:
        # or if smaller, the available places left.
        if placesRequired <= placesAvailable:
            # Bug #2 fixed - max number of points to use to book places
            # equals the available points of the club
            if int(club['points']) >= placesRequired:
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces']) - placesRequired
                # deduct redeemed points after successful booking of places
                club['points'] = int(club['points']) - placesRequired
                flash('Great-booking complete!')
                return render_template(
                    'welcome.html', club=club, competitions=competitions)
            flash("Your club doesn't have enough points")
            return render_template(
                'booking.html', club=club, competition=competition)
        flash(f'{competition["name"]} has only {placesAvailable} places left.')
        return render_template(
            'booking.html', club=club, competition=competition)
    flash(f'Sorry, its not allowed to book more than {MAX_ALLOWED_TO_BOOK} places.')
    return render_template(
            'booking.html', club=club, competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
