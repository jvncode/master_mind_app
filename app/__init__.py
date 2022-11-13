from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from config import ConfigEnv, APP_ENV, PORT, COLORS
from random import randint
from db import executions, setup
from datetime import datetime
from db import queries
from helper import check_hits


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
                try:
                    round_game = int(request.args.get('round_game', None))
                    status = request.args.get('status', 'ready')
                    if round_game == 10:
                        status = 'game_over'
                    if status == 'ready':
                        executions.exec_db(queries.update_round, data=(round_game+1, round_game+1))
                        data_game = executions.exec_db(queries.get_data)
                        new_row = (data_game[0][1],
                                '',
                                None,
                                None,
                                round_game+1,
                                data_game[0][6],
                                data_game[0][7])
                        executions.exec_db(queries.insert_data, data=new_row)
                    data_game = executions.exec_db(queries.get_data)
                    logging.info("Data Game in func game(): {}".format(data_game))
                except Exception as e:
                    logging.error("Error : {}".format(code))
                finally:
                    return render_template('home.html', data_game=data_game, status=status)
            else:
                setup.setup_db('delete')
                code = []
                try:
                    for ix in range(0, 4):
                        code.append(COLORS[randint(0, 3)])
                    logging.info("Secret code generated: {}".format(code))
                    date = datetime.now()
                    round_game = 1
                    data = ("".join(code), '', None, None, round_game, 0, date)
                    executions.exec_db(queries.insert_data, data=data)
                    data_game = executions.exec_db(queries.get_data)
                    logging.info("Data Game in func game(): {}".format(data_game))
                except Exception as e:
                    logging.error("Error generating secret code: {}".format(e))
                finally:
                    return render_template('home.html', data_game=data_game, mode='in_progress', status='ready')

        if request.method == 'POST':
            if request.form['btn'] == 'new_game':
                return redirect(url_for('game', mode='new'))
            if request.form['btn'] == 'check':
                try:
                    bet = request.form.getlist('bet')
                    round_game = request.form.get('round_game')
                    if '0' in bet:
                        data_game = executions.exec_db(queries.get_data)
                        return render_template('home.html', error_alert=True, mode='in_progress', data_game=data_game, status='ready')
                    return redirect(url_for('new_bet', bet="".join(bet), round_game=round_game))
                except Exception as e:
                    logging.error("Error in POST func game(): {}".format(e))
            if request.form['btn'] == 'json':
                return redirect(url_for('status'))


    @app.route('/new_bet', methods=['GET', 'POST'])
    def new_bet():
        if request.method == 'GET':
            try:
                bet = request.args.get('bet', None)
                round_game = request.args.get('round_game', None)
                data_game = executions.exec_db(queries.get_data)
                black_tokens, white_tokens = check_hits(data_game[0][1], bet)
                if black_tokens == 4:
                    executions.exec_db(queries.update_data, data=(bet, black_tokens, white_tokens, 1, round_game))
                    logging.info("Validation tokens - {} Blacks & {} Whites".format(black_tokens, white_tokens))
                    return redirect(url_for('game', mode='in_progress', round_game=round_game, status='win'))
                else:
                    executions.exec_db(queries.update_data, data=(
                        bet, black_tokens, white_tokens, 0, int(round_game)))
                    logging.info(
                        "Validation tokens - {} Blacks & {} Whites".format(black_tokens, white_tokens))
                    return redirect(url_for('game', mode='in_progress', round_game=round_game))
            except Exception as e:
                logging.error("Error in func new_bet() and validation bet: {}".format(e))


    @app.route('/status', methods=['GET'])
    def status():
        try:
            data_game = executions.exec_db(queries.get_data)
            dict_game = {}
            for ix, plays in enumerate(data_game):
                dict_game[ix] = plays
        except Exception as e:
            logging.error(
                "Error in func status() and response JSON: {}".format(e))
        finally:
            return jsonify({'game_status': dict_game})


    debug = True
    if APP_ENV == 'PROD':
        debug = False
    app.run(host='0.0.0.0',
            port=PORT,
            debug=debug)
