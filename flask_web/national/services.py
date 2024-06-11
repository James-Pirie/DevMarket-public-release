from flask_web.datareader import SQLAlchemyAdapter as Adapter


def get_number_of_listings_by_region(session, start_date, end_date, active):
    regions = ['Auckland', 'Wellington', 'Canterbury', 'Waikato', 'Otago', 'Bay of Plenty', 'Hawkes Bay',
               'Manawatu', 'Taranaki', 'Northland', 'Southland', 'Tasman']
    number_of_listings = []
    if active:
        for region in regions:
            number_of_listings.append(Adapter.get_number_of_active_listings(session, start_date, end_date, region))
        return {'labels': regions, 'data': number_of_listings, }

    for region in regions:
        number_of_listings.append(Adapter.get_number_of_listings(session, start_date, end_date, region))

    return {'labels': regions, 'data': number_of_listings,}


def get_number_of_listings_by_languages(session, start_date, end_date, active):
    language_names = Adapter.get_languages_by_listing_dates(session, start_date, end_date, active)

    language_numbers_data = []
    language_labels = []

    number_of_languages = 0
    other = 0

    for language in language_names:
        language_number = Adapter.get_number_of_listings_by_language(session, language, start_date, end_date, active)

        if number_of_languages >= 15:
            other += language_number

        else:
            language_labels.append(language)
            language_numbers_data.append(language_number)
            number_of_languages += 1

    if other > 1:
        language_labels.append('Other Languages')
        language_numbers_data.append(other)

    return {'labels': language_labels, 'data': language_numbers_data}
