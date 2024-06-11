from flask import Blueprint, render_template

# Configure browse blueprint
home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route("/")
def index():
    return render_template('home.html')



