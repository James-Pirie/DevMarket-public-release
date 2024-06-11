import flask_web.datareader.SQLAlchemyAdapter as Adapter
from flask import jsonify
from flask_web.database.models import Listing


def listings_to_json(listings):
    listings_data = {}

    index = 0

    for listing in listings:
        listing_dict = {
            'ListingID': listing.ListingID,
            'region': listing.region,
            'suburb': listing.suburb,
            'salary': listing.salary,
            'jobType': listing.jobType,
            'company': listing.company,
            'listingDate': str(listing.listingDate),
            'isActive': listing.isActive,
            'languages': [language.name for language in listing.languages],
            'frameworks': [framework.name for framework in listing.frameworks]
        }
        index += 1
        listings_data[f"Listing_{index}:"] = listing_dict

    return listings_data


def get_all_listings(session):
    all_listings = Adapter.get_all_listings(session)  # adapter queries database
    return listings_to_json(all_listings)


def get_listings_from_id(session, listing_id):
    listing = Adapter.get_listings_from_id(session, listing_id)  # adapter queries database
    return listings_to_json(listing)




def get_listings_from_company(session, company):
    listings = Adapter.get_listings_from_company(session, company)  # adapter queries database
    return listings_to_json(listings)


def get_listings_from_company_region(session, company, region):
    # get listing in a region from a specific company
    listings = Adapter.get_listings_from_company_region(session, company, region)
    return listings_to_json(listings)



