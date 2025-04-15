from flask import request
from user.audioProcessing import AudioProceesing
from user.kural import kural
from user.models import User
from app import app, login_required

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/practice_thirukkural',  methods=["POST"])
def practice():
    return AudioProceesing().practice()

@app.route('/filter_adhigaram',  methods=["POST"])
def fetchKural():
    return kural().fetchKural()

@app.route('/selected_game', methods=['POST'])
def selected_game():
    return kural().selected_game()

@app.route('/learn_thirukkural', methods=["GET"])
@login_required
def learn_thirukkural():
    return kural().learn_thirukkural()

@app.route('/drag_drop_game', methods=["GET"])
@login_required
def drag_drop_game():
    return kural().drag_drop_game()

@app.route('/evaluate_drag_game',  methods=["POST"])
def evaluate_drag_game():
    return kural().evaluate_drag_game()

@app.route('/fillups_game', methods=["GET"])
@login_required
def fillups_game():
    return kural().fillups_game()

@app.route('/evaluate_fillups_game',  methods=["POST"])
def evaluate_fillups_game():
    return kural().evaluate_fillups_game()

@app.route("/transaltee", methods=['POST', 'GET'])
def transaltee():
    return AudioProceesing().compareKural()
