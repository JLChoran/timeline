from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import data

bp = Blueprint("timeline", __name__)


@bp.route("/")
def index():
    category = request.args.get("category", "")
    events = data.get_events(category or None)
    categories = data.get_categories()
    return render_template(
        "index.html",
        events=events,
        categories=categories,
        active_category=category,
    )


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form.get("date", "").strip()
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()

        if not all([date, title, category]):
            flash("Date, title, and category are required.", "error")
            return render_template("add.html", form=request.form)

        data.add_event(date, title, description, category)
        flash(f'"{title}" added to your timeline.', "success")
        return redirect(url_for("timeline.index"))

    return render_template("add.html", form={})


@bp.route("/delete/<event_id>", methods=["POST"])
def delete(event_id):
    data.delete_event(event_id)
    flash("Event deleted.", "success")
    return redirect(url_for("timeline.index"))
