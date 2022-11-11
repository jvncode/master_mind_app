create_table = '''
                CREATE TABLE IF NOT EXISTS plays(
                    id INTEGER PRIMARY KEY NOT NULL,
                    secret_code VARCHAR(5) NOT NULL,
                    bets VARCHAR(4000),
                    black_tokens INTEGER DEFAULT 0,
                    white_tokens INTEGER DEFAULT 0,
                    rounds INTEGER DEFAULT 0,
                    status INTEGER DEFAULT 0,
                    play_date DATE);

                '''

delete_table = '''DELETE FROM plays;'''



insert_data = '''
            INSERT INTO plays (secret_code, bets, black_tokens, white_tokens, rounds, status, play_date)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            '''

get_data = ''' SELECT * FROM plays; '''

update_data = ''' UPDATE plays
                SET id = ?, bets = ?, black_tokens = ?, white_tokens = ?, status = ?
                WHERE rounds == ?; '''
