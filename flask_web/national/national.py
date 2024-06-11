import math

from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_web.region import services as region_services
from wtforms.fields.simple import StringField

import flask_web.national.services as services
import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


# Configure browse blueprint
national_blueprint = Blueprint("national_bp", __name__, url_prefix='/national')


@national_blueprint.route("/")
def national():
    session = current_app.config['SESSION']

    end_date = datetime.date.today()

    start_date = datetime.date(2023, 11, 12)
    # average_salary, biggest_employer, current_listings

    region = 'New Zealand'

    average_salary = region_services.get_average_salary(session, None)

    biggest_employer = region_services.get_biggest_employer(session, start_date, end_date, None)[0][0]

    current_listings = region_services.get_number_of_active_listings(session, start_date, end_date, None)

    graph_data, graph_labels = region_services.get_weekly_listings(session, None, start_date, end_date)

    total_listings = region_services.get_number_of_listings(session, None, start_date, end_date)

    days_timeframe = (end_date - start_date).days

    active_listings = services.get_number_of_listings_by_region(session, start_date, end_date, True)
    non_active_listings = services.get_number_of_listings_by_region(session, start_date, end_date, False)
    active_listings_by_language = services.get_number_of_listings_by_languages(session, start_date, end_date, True)
    total_listings_by_language = services.get_number_of_listings_by_languages(session, start_date, end_date, False)
    return render_template('national.html',
                           region=region,
                           average_salary=average_salary,
                           biggest_employer=biggest_employer,
                           current_listings=current_listings,
                           total_listings=total_listings,
                           weekly_average=int(sum(graph_data) / len(graph_data)),
                           listing_low=min(graph_data),
                           listing_high=max(graph_data),
                           data=graph_data,
                           labels=graph_labels,
                           active_listings=active_listings,
                           non_active_listings=non_active_listings,
                           chart_data=active_listings,
                           total_listings_by_language=total_listings_by_language,
                           active_listings_by_language=active_listings_by_language)
