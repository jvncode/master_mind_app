from flask import Flask, render_template, request, redirect, url_for
import logging
from config import ConfigEnv, APP_ENV, PORT, COLORS
from random import randint

def create_app():
    app = Flask(__name__)

    # Logs Config
    logging.basicConfig(filename='logs/mmind.log',
                        format='%(levelname)s %(asctime)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=ConfigEnv())


    @app.route('/', methods=['GET', 'POST'])
    def new_game():
        if request.method == 'GET':
            code = []
            try:
                for ix in range(0, 4):
                    code.append(COLORS[randint(0, 3)])
                logging.info("Secret code generated: {}".format(code))
            except Exception as e:
                logging.warning("Error generating secret code: {}".format(e))

            #TODO Insert data - DB

            return render_template('home.html', code=code)

        if request.method == 'POST':
            if request.form['btnNewGame']:
                return redirect(url_for('new_game'))

    @app.route('/status', methods=['GET'])
    def status():
        pass

    @app.route('/new_bet', methods=['POST'])
    def new_bet():
        pass



    debug = True
    if APP_ENV == 'PROD':
        debug = False
    app.run(host='0.0.0.0',
            port=PORT,
            debug=debug)
