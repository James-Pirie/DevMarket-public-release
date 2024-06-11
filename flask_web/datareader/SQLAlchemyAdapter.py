from flask import Blueprint
from sqlalchemy import func, desc, asc, and_
from flask_web.database.models import Listing, ListingFramework, Framework, ListingLanguage, Language

# Data reader interacts directly to the database, all sqlalchemy queries are preformed here.

# Configure browse blueprint
adapter_blueprint = Blueprint("adapter_bp", __name__, url_prefix='/api')


def get_all_listings(session):
    return session.query(Listing)


def get_listings_from_id(session, listing_id):
    return session.query(Listing).filter(Listing.ListingID == listing_id)


def get_listings_from_region(session, region, start_date):
    return session.query(Listing).filter(Listing.listingDate >= start_date, Listing.region == region).order_by(
        asc(Listing.listingDate)).all()


def get_listings_from_company(session, company):
    return session.query(Listing).filter(Listing.company == company)


def get_listings_from_company_region(session, company, region):
    return session.query(Listing).filter(Listing.company == company, Listing.region == region)


def get_top_frameworks(session, location):
    if location == None:
        subquery = session.query(
            ListingFramework.FrameworkID
        ).filter(
            ListingFramework.ListingID.in_(
                session.query(Listing.ListingID)
            )
        ).group_by(
            ListingFramework.FrameworkID
        ).order_by(
            func.count().desc()
        ).limit(10).subquery()

        top_frameworks = session.query(Framework).filter(Framework.FrameworkID.in_(subquery)).all()

        return top_frameworks

    subquery = session.query(
        ListingFramework.FrameworkID
    ).filter(
        ListingFramework.ListingID.in_(
            session.query(Listing.ListingID).filter(Listing.region == location)
        )
    ).group_by(
        ListingFramework.FrameworkID
    ).order_by(
        func.count().desc()
    ).limit(10).subquery()

    top_frameworks = session.query(Framework).filter(Framework.FrameworkID.in_(subquery)).all()

    return top_frameworks


def get_top_languages(session, location):
    if location == None:
        subquery = session.query(
            ListingLanguage.LanguageID
        ).filter(
            ListingLanguage.ListingID.in_(
                session.query(Listing.ListingID)
            )
        ).group_by(
            ListingLanguage.LanguageID
        ).order_by(
            func.count().desc()
        ).limit(10).subquery()

        top_languages = session.query(Language).filter(Language.LanguageID.in_(subquery)).all()

        return top_languages

    subquery = session.query(
        ListingLanguage.LanguageID
    ).filter(
        ListingLanguage.ListingID.in_(
            session.query(Listing.ListingID).filter(Listing.region == location)
        )
    ).group_by(
        ListingLanguage.LanguageID
    ).order_by(
        func.count().desc()
    ).limit(10).subquery()

    top_languages = session.query(Language).filter(Language.LanguageID.in_(subquery)).all()

    return top_languages


def get_top_location(session, location):
    if location == None:
        most_frequent_region = session.query(Listing.region,
                                             func.count(Listing.region).label('occurrence_count')) \
            .group_by(Listing.region) \
            .order_by(func.count(Listing.region).desc()) \
            .limit(10) \
            .all()

        return most_frequent_region

    most_frequent_suburb = session.query(Listing.suburb,
                                         func.count(Listing.suburb).label('occurrence_count')) \
        .filter(Listing.region == location) \
        .group_by(Listing.suburb) \
        .order_by(func.count(Listing.suburb).desc()) \
        .limit(10) \
        .all()

    return most_frequent_suburb


def get_number_of_listings(session, start_date, end_date, location):
    if location is None:
        number_of_listings = session.query(Listing).filter(Listing.listingDate >= start_date,
                                                           Listing.listingDate <= end_date).count()
        return number_of_listings

    number_of_listings = session.query(Listing).filter(Listing.region == location, Listing.listingDate >= start_date,
                                                       Listing.listingDate <= end_date).count()
    return number_of_listings


def get_active_salaries(session, location):
    if location is None:
        return session.query(Listing.salary)

    return session.query(Listing.salary).filter(Listing.region == location)


def get_top_employer(session, start_date, end_date, location):
    if location is None:
        most_frequent_company = session.query(Listing.company,
                                              func.count(Listing.company).label('occurrence_count')) \
            .filter(Listing.listingDate >= start_date, Listing.listingDate <= end_date) \
            .group_by(Listing.company) \
            .order_by(func.count(Listing.company).desc()) \
            .limit(10) \
            .all()

        return most_frequent_company

    most_frequent_company = session.query(Listing.company,
                                          func.count(Listing.company).label('occurrence_count')) \
        .filter(Listing.region == location, Listing.listingDate >= start_date, Listing.listingDate <= end_date) \
        .group_by(Listing.company) \
        .order_by(func.count(Listing.company).desc()) \
        .limit(10) \
        .all()

    return most_frequent_company


def get_listings_by_date(session, start_date, location):
    if location is None:
        return session.query(Listing).filter(Listing.listingDate >= start_date).order_by(asc(Listing.listingDate)).all()

    return session.query(Listing).filter(Listing.region == location, Listing.listingDate >= start_date).order_by(
        asc(Listing.listingDate)).all()


def get_number_of_active_listings(session, start_date, end_date, location):
    if location is None:
        number_of_listings = session.query(Listing).filter(Listing.listingDate >= start_date,
                                                           Listing.listingDate <= end_date,
                                                           Listing.isActive == 1).count()
        return number_of_listings

    number_of_listings = session.query(Listing).filter(Listing.region == location, Listing.listingDate >= start_date,
                                                       Listing.listingDate <= end_date, Listing.isActive == 1).count()
    return number_of_listings


def get_languages_by_listing_dates(session, start_date, end_date, active):
    query = (
        session.query(Language.name, func.count(ListingLanguage.ListingID).label('listing_count'))
        .join(ListingLanguage)
        .group_by(Language.name)
        .order_by(func.count(ListingLanguage.ListingID).desc())
    )
    if active:
        query = (
            session.query(Language.name, func.count(ListingLanguage.ListingID).label('listing_count'))
            .join(ListingLanguage)
            .join(Listing)
            .filter(and_(Listing.isActive == 1))
            .group_by(Language.name)
            .order_by(func.count(ListingLanguage.ListingID).desc())
        )
    result = query.filter(and_(Listing.listingDate >= start_date, Listing.listingDate <= end_date)).all()

    return [language[0] for language in result]


def get_number_of_listings_by_language(session, language_name, start_date, end_date, active):
    query = session.query(Listing).join(ListingLanguage).join(Language).filter(Language.name == language_name)

    if active is not None:
        query = query.filter(Listing.isActive == active)

    result = query.filter(and_(Listing.listingDate >= start_date, Listing.listingDate <= end_date)).count()

    return result





