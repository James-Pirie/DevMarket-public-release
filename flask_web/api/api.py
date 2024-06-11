from flask import Blueprint, current_app, request
import flask_web.api.services as services


# Configure browse blueprint
api_blueprint = Blueprint("api_bp", __name__, url_prefix='/api')


@api_blueprint.route("/listings")
def listings():
    # arguments for listing, eg /api/listing?id=123 or api/listing?region=Wellington
    listing_id = request.args.get('id')
    region = request.args.get('region')
    company = request.args.get('company')

    session = current_app.config['SESSION']

    # listing_id can only possibly return one item
    # therefore if listing_id is entered, it excludes other arguments
    if listing_id:
        return services.get_listings_from_id(session, listing_id)

    elif region:
        return services.get_listings_from_region(session, region)

    elif company:
        return services.get_listings_from_company(session, company)

    elif region and company:
        return services.get_listings_from_company_region(session, company, region)

    return services.get_all_listings(session)

