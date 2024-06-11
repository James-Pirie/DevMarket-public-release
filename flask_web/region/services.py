from datetime import timedelta
import re

import flask_web.datareader.SQLAlchemyAdapter as Adapter
from flask import jsonify

from flask_web.api.services import listings_to_json
from flask_web.database.models import Listing


def get_average_salary(session, region):
    salary_query = Adapter.get_active_salaries(session, region)  # adapter queries database
    salaries_filtered = []
    for wage in salary_query:
        salary_calculated = 0
        try:
            selected_salary = wage[0]
            selected_salary_filtered = ''.join(
                char for char in selected_salary if char.isdigit() or char.lower() == 'k'
                or char.lower() == '-')

            if '-' in selected_salary_filtered and 'k' in selected_salary_filtered:
                salary_range = selected_salary_filtered.split('-')
                # convert the items into ints
                salary_range_int = [int(item.replace('k', '')) for item in salary_range]
                salary_range_int[0] = salary_range[0] * 1000
                salary_range_int[1] = salary_range[1] * 1000
                average_of_range = (salary_range_int[0] + salary_range_int[1]) / 2
                salary_calculated = average_of_range

            elif 'k' in selected_salary_filtered:
                selected_salary_filtered = int(
                    re.sub(r'\D', '', selected_salary_filtered))  # removes all letters and turns into numbers
                salary_calculated = selected_salary_filtered * 1000

            elif '-' in selected_salary_filtered:
                salary_range_int = list(map(int, selected_salary_filtered.split('-')))
                average_of_range = (salary_range_int[0] + salary_range_int[1]) / 2
                salary_calculated = average_of_range

            if 70000 < salary_calculated < 400000:
                salaries_filtered.append(salary_calculated)

            sum_of_salaries = 0
            for individual_salary in salaries_filtered:
                sum_of_salaries += individual_salary

            result = int(sum_of_salaries / len(salaries_filtered))
            result_string = str(result)
            return f"{result_string[:-3]},{result_string[-3:]} NZD"

        except Exception as e:
            print(f"{e} for {wage}")

    return "Not Enough Data"


def get_weekly_listings(session, region, start_date, end_date):
    values = []

    x_axis_dates = []

    listings_from_region = Adapter.get_listings_by_date(session, start_date, region)

    starting_date = start_date
    ending_date = end_date

    count = 0

    for listing in listings_from_region:
        if listing.listingDate > ending_date:
            return values

        if listing.listingDate <= starting_date + timedelta(weeks=1):
            count += 1

        elif listing.listingDate > starting_date + timedelta(weeks=1):
            values.append(count)
            x_axis_dates.append(starting_date.strftime('%Y-%m-%d'))
            count = 1
            starting_date = starting_date + timedelta(weeks=1)

            while listing.listingDate > starting_date + timedelta(weeks=1):
                starting_date = starting_date + timedelta(weeks=1)
                x_axis_dates.append(starting_date.strftime('%Y-%m-%d'))
                values.append(0)

    values.append(count)
    x_axis_dates.append(starting_date.strftime('%Y-%m-%d'))
    return values, x_axis_dates


def get_top_location(session, region):

    top_suburb = Adapter.get_top_location(session, region)
    return top_suburb


def get_biggest_employer(session, start_date, end_date, region):
    try:
        top_employer = Adapter.get_top_employer(session, start_date, end_date, region)
        return top_employer
    except Exception as e:
        print(e)
        return ['Not Enough Data']


def get_top_frameworks(session, region):
    top_frameworks = Adapter.get_top_frameworks(session, region)
    return [framework.name for framework in top_frameworks]


def get_top_languages(session, region):
    top_languages = Adapter.get_top_languages(session, region)
    return [language.name for language in top_languages]


def get_number_of_active_listings(session, start_date, end_date, region):
    number_of_active_listings = Adapter.get_number_of_active_listings(session, start_date, end_date, region)
    return number_of_active_listings


def get_number_of_listings(session, region, start_date, end_date):
    number_of_active_listings = Adapter.get_number_of_listings(session,start_date, end_date, region)
    return number_of_active_listings


