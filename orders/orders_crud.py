from orders import get_model
from flask import Blueprint, redirect, render_template, request, url_for


orders_crud = Blueprint('orders_crud', __name__)


builtin_list = list



# [START list]
@orders_crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    orders, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        orders=orders,
        next_page_token=next_page_token)
# [END list]


@orders_crud.route('/<id>')
def view(id):
    order = get_model().read(id)
    return render_template("view.html", order=order)


# [START add]
@orders_crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().create(data)

        return redirect(url_for('.view', id=order['id']))

    return render_template("form.html", action="Add", order={})
# [END add]


@orders_crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    order = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().update(data, id)

        return redirect(url_for('.view', id=order['id']))

    return render_template("form.html", action="Edit", order=order)


@orders_crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
