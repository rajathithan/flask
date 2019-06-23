from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START order model]
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    orderno = db.Column(db.Integer)
    amount = db.Column(db.Float(precision=2))
    status = db.Column(db.String(10))

    def __repr__(self):
        return "<Order(orderno='%s', status=%s)" % (self.orderno, self.status)
# [END order model]


# [START giftcard model]
class Giftcard(db.Model):
    __tablename__ = 'giftcards'

    id = db.Column(db.Integer, primary_key=True)
    gcno = db.Column(db.Integer)
    amount = db.Column(db.Float(precision=2))

    def __repr__(self):
        return "<Giftcard(gcno='%s', amount=%s)" % (self.gcno, self.amount)
# [END giftcard model]


# [START order list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Order.query
             .order_by(Order.orderno)
             .limit(limit)
             .offset(cursor))
    orders = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(orders) == limit else None
    return (orders, next_page)
# [END order list]


# [START giftcard list]
def gclist(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Giftcard.query
             .order_by(Giftcard.gcno)
             .limit(limit)
             .offset(cursor))
    gcs = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(gcs) == limit else None
    return (gcs, next_page)
# [END giftcard list]


# [START order id read]
def read(id):
    result = Order.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END order id read]


# [START giftcard id read]
def gcread(id):
    result = Giftcard.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END order id read]


# [START all orders read]
def readall():
    orders = builtin_list(map(from_sql, Order.query.all()))
    return orders
# [END all orders read]


# [START all giftcards read]
def gcreadall():
    gcs = builtin_list(map(from_sql, Giftcard.query.all()))
    return gcs
# [END all giftcards read]


# [START order no. read]
def find_by_orderno(orderno):
    order = from_sql(Order.query.filter_by(orderno=int(orderno)).first())
    return order
# [END order no. read]


# [START giftcard no. read]
def find_by_gcno(gcno):
    gc = from_sql(Giftcard.query.filter_by(gcno=int(gcno)).first())
    return gc
# [END giftcard no. read]


# [START order create]
def create(data):
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return from_sql(order)
# [END order create]


# [START order create]
def gccreate(data):
    gc = Giftcard(**data)
    db.session.add(gc)
    db.session.commit()
    return from_sql(gc)
# [END order create]


# [START order update]
def update(data, id):
    order = Order.query.get(id)
    for k, v in data.items():
        setattr(order, k, v)
    db.session.commit()
    return from_sql(order)
# [END order update]


# [START giftcard update]
def gcupdate(data, id):
    gc = Giftcard.query.get(id)
    for k, v in data.items():
        setattr(gc, k, v)
    db.session.commit()
    return from_sql(gc)
# [END giftcard update]


# [START order delete]
def delete(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
# [END order delete]


# [START giftcard delete]
def gcdelete(id):
    Giftcard.query.filter_by(id=id).delete()
    db.session.commit()
# [END giftcard delete]


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
