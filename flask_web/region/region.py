import math

from flask import Blueprint, render_template, current_app, redirect, url_for
from wtforms.fields.simple import StringField

import flask_web.region.services as services
import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


# Configure browse blueprint
regions_blueprint = Blueprint("region_bp", __name__, url_prefix='/region')


@regions_blueprint.route("/", methods=['GET', 'POST'])
def regions():
    session = current_app.config['SESSION']

    end_date = datetime.date.today()

    start_date = datetime.date(2023, 11, 12)
    # average_salary, biggest_employer, current_listings
    current_region = 'auckland'
    average_salary = services.get_average_salary(session, current_region)
    biggest_employer = services.get_biggest_employer(session, start_date, end_date, current_region)[0][0]
    current_listings = services.get_number_of_active_listings(session, start_date, end_date, current_region)
    graph_data, graph_labels = services.get_weekly_listings(session, current_region, start_date, end_date)
    total_listings = services.get_number_of_listings(session, current_region, start_date, end_date)
    days_timeframe = (end_date - start_date).days
    top_frameworks = services.get_top_frameworks(session, current_region)
    top_suburb = services.get_top_location(session, current_region)
    top_languages = services.get_top_languages(session, current_region)
    choose_region_form = RegionForm()

    if choose_region_form.validate_on_submit():
        selected_region = choose_region_form.dropdown.data
        current_region = selected_region
        average_salary = services.get_average_salary(session, current_region)
        biggest_employer = services.get_biggest_employer(session, start_date, end_date, current_region)[0][0]
        current_listings = services.get_number_of_active_listings(session, start_date, end_date, current_region)
        graph_data, graph_labels = services.get_weekly_listings(session, current_region, start_date, end_date)
        total_listings = services.get_number_of_listings(session, current_region, start_date, end_date)
        days_timeframe = (end_date - start_date).days
        top_frameworks = services.get_top_frameworks(session, current_region)
        top_suburb = services.get_top_location(session, current_region)
        top_languages = services.get_top_languages(session, current_region)

        return render_template('region.html',
                               region=selected_region,
                               choose_region_form=choose_region_form,
                               average_salary=average_salary,
                               biggest_employer=biggest_employer,
                               current_listings=current_listings,
                               total_listings=total_listings,
                               weekly_average=int(sum(graph_data) / len(graph_data)),
                               listing_low=min(graph_data),
                               listing_high=max(graph_data),
                               data=graph_data,
                               labels=graph_labels,
                               top_frameworks=top_frameworks,
                               top_suburb=top_suburb,
                               top_languages=top_languages)

    return render_template('region.html',
                           region=current_region,
                           choose_region_form=choose_region_form,
                           average_salary=average_salary,
                           biggest_employer=biggest_employer,
                           current_listings=current_listings,
                           total_listings=total_listings,
                           weekly_average=int(sum(graph_data) / len(graph_data)),
                           listing_low=min(graph_data),
                           listing_high=max(graph_data),
                           data=graph_data,
                           labels=graph_labels,
                           top_frameworks=top_frameworks,
                           top_suburb=top_suburb,
                           top_languages=top_languages)


class RegionForm(FlaskForm):
    dropdown = SelectField(choices=[('auckland', 'Auckland'),
                                    ('wellington', 'Wellington'),
                                    ('canterbury', 'Canterbury'),
                                    ('waikato', 'Waikato'),
                                    ('otago', 'Otago'),
                                    ('bay of plenty', 'Bay of Plenty'),
                                    ('hawkes bay', 'Hawkes Bay'),
                                    ('manawatu', 'Manawatu'),
                                    ('taranaki', 'Taranaki'),
                                    ('northland', 'Northland'),
                                    ('southland', 'Southland'),
                                    ('tasman', 'Tasman')])
