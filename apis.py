from flask import request, json
from helpers import Crypt, Auth
from flask.views import MethodView
from models import db, User, Category, Person, Transaction, TransactionItem


class UserAPI(MethodView):
    def get(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            return json.jsonify(user.as_dict())
        return json.jsonify({})

    def post(self):
        supposed_user = request.get_json(force=True)
        if supposed_user:
            user = User()
            user.name = supposed_user['name']
            user.login = supposed_user['login']
            user.password = Crypt.hash_sha256(supposed_user['password'])
            user.auth_key = Auth.get_new_key()
            db.session.add(user)
            db.session.commit()
            if user.user_id:
                return json.jsonify(user.as_dict())
        return json.jsonify({})

    def put(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_user = request.get_json(force=True)
            user.name = new_user['name']
            user.login = new_user['login']
            user.password = Crypt.hash_sha256(new_user['password'])
            db.session.commit()
            return json.jsonify(user.as_dict())
        return json.jsonify({})

    def delete(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            db.session.delete(user)
            db.session.commit()
            return json.jsonify(user.as_dict())
        return json.jsonify({})


class LoginAPI(MethodView):
    def post(self):
        supposed_user = request.get_json(force=True)
        user = User.query.filter_by(login=supposed_user['login']).first_or_404()
        if user and user.password == Crypt.hash_sha256(supposed_user['password']):
            return json.jsonify(user.as_dict())
        return json.jsonify({})


class CategoryAPI(MethodView):
    def get(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            if category_id:
                return json.jsonify(user.categories.filter_by(category_id=category_id).first_or_404().as_dict())
            return json.jsonify({'categories': [category.as_dict() for category in user.categories]})
        return json.jsonify({})

    def post(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            supposed_category = request.get_json(force=True)
            category = Category()
            category.user_id = user_id
            category.name = supposed_category['name']
            category.icon_id = supposed_category['icon_id']
            db.session.add(category)
            db.session.commit()
            if category.category_id:
                return json.jsonify(category.as_dict())
        return json.jsonify({})

    def put(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_category = request.get_json(force=True)
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            category.name = new_category['name']
            category.icon_id = new_category['icon_id']
            db.session.commit()
            return json.jsonify(category.as_dict())
        return json.jsonify({})

    def delete(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            if category:
                db.session.delete(category)
                db.session.commit()
                return json.jsonify(category.as_dict())
        return json.jsonify({})


class PersonAPI(MethodView):
    def get(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            if person_id:
                return json.jsonify(user.people.filter_by(person_id=person_id).first_or_404().as_dict())
            return json.jsonify({'people': [person.as_dict() for person in user.people]})
        return json.jsonify({})

    def post(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            supposed_person = request.get_json(force=True)
            person = Person()
            person.user_id = user_id
            person.name = supposed_person['name']
            db.session.add(person)
            db.session.commit()
            if person.person_id:
                return json.jsonify(person.as_dict())
        return json.jsonify({})

    def put(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_person = request.get_json(force=True)
            person = user.people.filter_by(person_id=person_id).first_or_404()
            person.name = new_person['name']
            db.session.commit()
            return json.jsonify(person.as_dict())
        return json.jsonify({})

    def delete(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            person = user.people.filter_by(person_id=person_id).first_or_404()
            if person:
                db.session.delete(person)
                db.session.commit()
                return json.jsonify(person.as_dict())
        return json.jsonify({})