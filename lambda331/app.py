from flask import Flask, render_template, request
import json
from data_model import DB
from twitter import upsert_user
from os import path
from ml import predict_most_likely_author


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'lambda331/sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def landing():
        if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
            DB.create_all()
            DB.session.commit()
            pass
        with open('templates/landing.json') as f:
            args = json.load(f)
        return render_template('base.html', **args)

    @app.route('/add_user', methods=['GET'])
    def add_user():
        twitter_handle = request.args['twitter_handle']
        upsert_user(twitter_handle)
        return 'insert successful'

    @app.route('/predict_author', methods=['GET'])
    def predict_author():
        tweet_to_classify = request.args['tweet_to_classify']
        return predict_most_likely_author(tweet_to_classify, ['adam3us', 'VitalikButerin'])

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1,user2 = sorted([request.values['user1'],
                              request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a uer to themselves!'
        else:
            prediction = predict_userr(user1, user2,
                                       request.values['tweet_text'])
            message = '"{}" is more likely to be said by @{} than @{}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1
            )
            return  render_template('predict.html', title='Prediction',
                                    message=message)

    return app



