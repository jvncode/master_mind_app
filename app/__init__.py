from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from config import ConfigEnv, APP_ENV, PORT, COLORS
from random import randint
from db import executions, setup
from datetime import datetime
from db import queries

def create_app():
    app = Flask(__name__)
    setup.setup_db('delete')
    setup.setup_db('create')

    # Logs Config
    logging.basicConfig(filename='logs/mmind.log',
                        format='%(levelname)s %(asctime)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=ConfigEnv())


    @app.route('/', methods=['GET', 'POST'])
    def game():
        if request.method == 'GET':
            if request.args.get('mode', None) == 'in_progress':
                data_game = executions.exec_db(queries.get_data)
                print("DATA:", data_game)
                return render_template('home.html', round=2)
            else:
                setup.setup_db('delete')
                code = []
                try:
                    for ix in range(0, 4):
                        code.append(COLORS[randint(0, 3)])
                    logging.info("Secret code generated: {}".format(code))

                    date = datetime.now()
                    round_game = 1
                    data = ("".join(code), '', 0, 0, round_game, 0, date)
                    data_game = executions.exec_db(queries.insert_data, data=data)
                    print("INITIAL DATA GAME: ", data_game)

                except Exception as e:
                    logging.warning("Error generating secret code: {}".format(e))

                return render_template('home.html', round=round_game, date=date, mode='in_progress')

        if request.method == 'POST':
            if request.form['btn'] == 'new_game':
                return redirect(url_for('game', mode='new'))
            if request.form['btn'] == 'check':
                bet = request.form.getlist('bet')
                if '0' in bet:
                    return redirect(url_for('new_bet', alert="Error"))
                print("BET:", bet)
                return redirect(url_for('new_bet', bet="".join(bet), round_game=request.form.get('number_round')))

    @app.route('/new_bet', methods=['GET', 'POST'])
    def new_bet():
        if request.method == 'GET':
            bet = request.args.get('bet', None)
            round_game = request.args.get('round_game', None)
            black_tokens = 0
            white_tokens = 0
            status = 0
            # TODO Function that returns how many successes there are
            executions.exec_db(queries.update_data, data=(1, bet, black_tokens, white_tokens, status, round_game))

            return redirect(url_for('game', mode='in_progress'))


    @app.route('/status', methods=['GET'])
    def status():
        pass




    debug = True
    if APP_ENV == 'PROD':
        debug = False
    app.run(host='0.0.0.0',
            port=PORT,
            debug=debug)
