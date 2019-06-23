from orders import get_model
from flask import Blueprint, redirect, render_template, request, url_for


giftcards_crud = Blueprint('giftcards_crud', __name__)


builtin_list = list


# [START list]
@giftcards_crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    gcs, next_page_token = get_model().gclist(cursor=token)

    return render_template(
        "gclist.html",
        gcs=gcs,
        next_page_token=next_page_token)
# [END list]


# [START view]
@giftcards_crud.route('/<id>')
def view(id):
    gc = get_model().gcread(id)
    return render_template("gcview.html", gc=gc)
# [START view]


# [START create]
@giftcards_crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        gc = get_model().gccreate(data)

        return redirect(url_for('.view', id=gc['id']))

    return render_template("gcform.html", action="Add", gc={})
# [END create]


# [START edit]
@giftcards_crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    gc = get_model().gcread(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        gc = get_model().gcupdate(data, id)

        return redirect(url_for('.view', id=gc['id']))

    return render_template("gcform.html", action="Edit", gc=gc)
# [END edit]


# [START delete]
@giftcards_crud.route('/<id>/delete')
def delete(id):
    get_model().gcdelete(id)
    return redirect(url_for('.list'))
# [END delete]