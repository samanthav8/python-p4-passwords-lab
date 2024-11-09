#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from config import app, db, api, bcrypt
from models import User

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204

class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session and session['user_id'] is not None:
            user = db.session.get(User, session['user_id'])
            if user:
                return user.to_dict(), 200
        return {}, 204



class Login(Resource):
    def post(self):
        json = request.get_json()
        # Get user by username
        user = User.query.filter(User.username == json['username']).first()

        if user and user.authenticate(json['password']):
            # User authenticated successfully, set session
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        # Clear the user session
        session['user_id'] = None
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
