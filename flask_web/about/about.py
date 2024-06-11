from flask import Blueprint, render_template

# Configure browse blueprint
about_blueprint = Blueprint("about_bp", __name__)


@about_blueprint.route("/about")
def about():
    return render_template('about.html')

