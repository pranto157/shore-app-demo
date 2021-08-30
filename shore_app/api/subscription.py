import json
from flask import request, jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from shore_app.extensions import db
from shore_app.models import Subscription, User
from shore_app.utils import commit_or_rollback


class SubscriptionItem(Resource):

    def _get_subscription(self, sub_id):
        sub = Subscription.query.get(sub_id)
        if not sub:
            abort(404, "Subscription not found for id -  %s" % sub_id)
        return sub

    def get(self, sub_id):
        sub = self._get_subscription(sub_id)
        sub = sub.serialize()
        return jsonify(sub)

    def delete(self, sub_id):
        sub = self._get_subscription(sub_id)
        db.session.delete(sub)
        commit_or_rollback(db.session)
        jsonify({'message': 'Subscription id %s succsesfully removed' % sub_id})

    def put(self, sub_id):
        sub_json = request.get_json(force=True)
        sub = Subscription.query.get(sub_id)
        sub = _set_attributes(sub, sub_json)

        if not sub.user_id:
            abort(400, 'User is requried!')

        try:
            sub.interval = int(sub.interval)
        except ValueError:
            abort(400, 'Interval must be an integer value')

        try:
            db.session.add(sub)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])

        sub = sub.serialize()
        return jsonify(sub)


class SubscriptionItems(Resource):

    def get(self):
        user_id = request.args.get('user_id')
        query = Subscription.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        subs = query.all()
        response = [{x: d[x] for x in d if x != 'user'}
                    for d in Subscription.serialize_list(subs)]
        return jsonify(response)

    def post(self):
        sub_json = request.get_json(force=True)
        sub = Subscription()
        sub = _set_attributes(sub, sub_json)

        if not sub.user_id:
            abort(400, 'User is requried!')

        try:
            sub.interval = int(sub.interval)
        except ValueError:
            abort(400, 'Interval must be an integer value')

        user = User.query.get(sub.user_id)
        if not user:
            abort(404, "User not found for id -  %s" % sub.user_id)

        try:
            user.subscriptions.append(sub)
            db.session.add(sub)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])

        sub = sub.serialize()
        return jsonify(sub)


def _set_attributes(user, sub_json):
    for attr in ['user_id', 'phrases', 'interval', 'active']:
        if sub_json.get(attr):
            try:
                setattr(user, attr, sub_json[attr])
            except ValueError as e:
                abort(400, str(e))
    return user
