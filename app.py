# This exercise guides you in creating a web-based game engine for a text adventure game.
# You'll refactor existing code from a exercise 43, combining it with concepts from
# exercise 47 – Automated testing to build a game structure. The first step involves
# copying and organizing code into specific files. Then, you'll refactor the map to include
# all necessary rooms and transitions. Additionally, you'll create automated tests to
# ensure the functionality of the map. Next, you'll develop a game engine using Flask,
# which will handle game sessions, user input, and navigation through the game's rooms.
# Finally, you'll create HTML templates for displaying the game's rooms and handling game
# over scenarios. Throughout the process, you'll run tests and debug to ensure everything
# works correctly.

from flask import Flask, session, redirect, url_for, request
from markupsafe import escape
from flask import render_template
from gothonweb import planisphere


app = Flask(__name__)


@app.route("/")
def index():
    # This is used to "setup" the session with starting values
    session['room_name'] = planisphere.START
    return redirect(url_for("game"))


terminating_rooms = ['The End', 'The End Winner']


@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')
    terminate = False
    if room_name in terminating_rooms:
        terminate = True

    if request.method == "GET":
        if room_name != "Death":
            room = planisphere.load_room(room_name)
            return render_template("show_room.html", room=room, done=terminate)
        else:
            # why is there here? do you need it?
            return render_template("you_died.html")
    else:
        action = request.form.get('action')

        if room_name and action:
            room = planisphere.load_room(room_name)
            next_room = room.go(action)

            if not next_room:
                # If the input is not valid, repeat current room.
                session['room_name'] = planisphere.name_room(room)
            else:
                # If the input is valid, go on to next room.
                session['room_name'] = planisphere.name_room(next_room)

        return redirect(url_for("game"))


# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
