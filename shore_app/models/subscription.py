from sqlalchemy import Column
from sqlalchemy_utils.types.choice import ChoiceType

from shore_app.extensions import db
from shore_app.utils import get_current_time, Serializer
from shore_app.constants import STRING_LEN, ALERT_INTERVAL


class Subscription(db.Model, Serializer):

    __tablename__ = 'subscriptions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'),
                     nullable=False)
    phrases = Column(db.String(STRING_LEN), nullable=False)
    interval = Column(ChoiceType(ALERT_INTERVAL, impl=db.Integer()))
    last_email_sent = db.Column(db.DateTime, index=True)
    active = Column(db.Boolean, default=True, nullable=False)
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime, onupdate=get_current_time)

    def serialize(self):
        return Serializer.serialize(self)
