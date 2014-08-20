from easypc.data import pf_data
from flask import request, redirect, url_for, render_template
from easypc import app
from easypc.models.character import Character
from easypc.login import login_required


@app.route("/pcs")
@login_required
def list():
    return render_template('show/list.html', pcs=Character.list_all())


@app.route("/pc/<name>", methods=["GET", "POST"])
@login_required
def show_pc(name):
    if request.method == "DELETE":
        Character(name).delete()
        return redirect(url_for('list'))


    return render_template("show/show.html", pc=Character(name), pf_data=pf_data)


@app.route("/pc/new")
@login_required
def new():
    return render_template('create/new.html', pf_data=pf_data)


@app.route("/pc/new", methods=['POST'])
@login_required
def create():
    character = Character.create(request.form['name'])
    return redirect(url_for('attributes', name=character.name))


@app.route("/pc/<name>/attributes")
@login_required
def attributes(name):
    return render_template("create/attributes.html", name=name,
                           attributes=pf_data['attributes'])


@app.route("/pc/<name>/attributes", methods=['POST'])
@login_required
def update_attributes(name):
    Character(name).update(request.form)
    return redirect(url_for('race', name=name))


@app.route("/pc/<name>/choose_race")
@login_required
def race(name):
    return render_template(
        "create/choose_race.html",
        name=name,
        races=pf_data['races'],
        attributes=pf_data['attributes']
    )


@app.route("/pc/<name>/choose_race", methods=['POST'])
@login_required
def update_race(name):
    pc = Character(name)

    updates = {
        "race": request.form.get('race'),
        "traits": request.form.getlist("traits")
    }

    race_data = pf_data['races'][request.form.get('race')]

    if "choice" in race_data['modifiers']:
        mod = request.form.get("modifier")
        updates[mod] = int(pc.attributes[mod]) + 2
    else:
        for modifier, value in race_data['modifiers'].iteritems():
            updates[modifier] = int(pc.attributes[modifier]) + int(value)

    pc.update(updates)
    return redirect(url_for('physical_desc', name=name))


@app.route("/pc/<name>/physical_desc", methods=["GET"])
@login_required
def physical_desc(name):
    pc = Character(name)

    return render_template("create/physical_desc.html",
                           name=name,
                           race=pf_data['races'][pc.race],
                           int_modifier=pc.get_modifier("intelligence"),
                           alignments=pf_data['alignments'])


@app.route("/pc/<name>/physical_desc", methods=["POST"])
@login_required
def update_physical_desc(name):

    pc = Character(name)

    pc.update({
        "weight": request.form.get('weight'),
        "height": "%s\" %s'" % divmod(int(request.form.get('height')), 12),
        "gender": request.form.get('gender'),
        "age": request.form.get('age'),
        "alignment": request.form.get('alignment'),
        "eyes": request.form.get('eyes'),
        "hair": request.form.get('hair'),
        "languages": request.form.getlist("languages")
    })
    return redirect(url_for('show_pc', name=name))
