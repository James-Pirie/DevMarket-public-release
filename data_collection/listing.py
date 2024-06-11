import re

from bs4 import BeautifulSoup
import datetime
import requests
import string


class Listing:
    def __init__(self, url, id):
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        self.listing_id = id
        self.region = self.get_location_and_salary()
        self.suburb: None  # defined in get_location_and_salary method
        self.company = self.get_company()
        self.salary: str  # defined in get_location_and_salary method
        self.job_type = self.get_job_type()
        self.listed_date = self.get_date()
        self.listing_languages = []
        self.technologies = []
        self.read_page()

    def __str__(self):
        return (f"{self.listing_id} {self.region} {self.suburb} {self.company} {self.salary} "
                f"{self.job_type} {self.listed_date} {self.listing_languages} {self.technologies}")

    def get_location_and_salary(self):
        #  the class of the span object
        location = self.soup.select('span.y735df0._1iz8dgs4y._94v4w0._94v4w1._94v4w21._4rkdcp4._94v4w7')[:14]
        listing_information = []
        # there will be multiple span objects of the desired class
        for locations in location:
            # if the location contains a suburb, the format will be district, suburb
            listing_information.append(locations.text.split(','))

        self.salary = self.find_salary(listing_information)
        # if there is two items in the list the suburb is listed
        if len(listing_information[6]) == 2:
            self.suburb = listing_information[6][0].strip()
            return listing_information[6][1].strip()

        self.suburb = None
        return listing_information[6][0].strip()

    @staticmethod
    def find_salary(tags):
        desired_spans = [span for span in tags if '$' in span[0]]
        if desired_spans:
            return ','.join(desired_spans[0])
        return None

    def get_company(self):
        company = self.soup.select('span.y735df0._1iz8dgs4y._94v4w0._94v4w1._94v4w21._4rkdcp4._94v4wa')[4].text
        return company

    def get_date(self):
        # if the suburb exists the date will be at a different location on the page, try both ways
        try:
            posted_date = self.soup.select('span.y735df0._1iz8dgs4y._94v4w0._94v4w1._94v4w22._4rkdcp4._94v4w7')[2].text

            date_specific = posted_date.split()

            if date_specific[len(date_specific) - 1] != 'ago':
                date_string = f"{date_specific[1]} {date_specific[2]} {date_specific[3]}"
                date_format = "%d %B %Y"
                return datetime.datetime.strptime(date_string, date_format)

        except:
            posted_date = self.soup.select('span.y735df0._1iz8dgs4y._94v4w0._94v4w1._94v4w22._4rkdcp4._94v4w7')[1].text

            date_specific = posted_date.split()

            if date_specific[len(date_specific) - 1] != 'ago':
                date_string = f"{date_specific[1]} {date_specific[2]} {date_specific[3]}"
                date_format = "%d %B %Y"
                return datetime.datetime.strptime(date_string, date_format)

        units = date_specific[1][len(date_specific[1]) - 1]
        value = int(date_specific[1][:-1])
        if units != 'd':
            return datetime.date.today()
        return datetime.date.today() - datetime.timedelta(value)

    def get_job_type(self):
        job_type = self.soup.select_one('span[data-automation="job-detail-work-type"]').text
        return job_type

    def read_page(self):
        languages_file = open("languages.txt", 'r')
        languages = languages_file.read().split()

        frameworks_file = open("all_frameworks.txt", 'r')
        frameworks_list_data = frameworks_file.read().split()
        frameworks_file.close()
        # creates list of frameworks and language corresponding to the framework
        framework = [pair.split(',')[0] for pair in frameworks_list_data]
        frame_language = [pair.split(',')[1] for pair in frameworks_list_data]

        job_description = ' '.join(self.soup.select_one('div.y735df0._1pehz540').stripped_strings)

        translator = str.maketrans("", "", string.punctuation.replace("+", "").replace("#", ""))
        job_description = job_description.translate(translator)

        for word in job_description.split():
            clean_word = word.lower().strip()

            if clean_word in languages and clean_word not in self.listing_languages:
                self.listing_languages.append(clean_word)

            if clean_word in framework and clean_word not in self.technologies:
                self.technologies.append(clean_word)

                index = framework.index(clean_word)
                # checks if language is in the listing_languages list
                if frame_language[index] not in self.listing_languages:
                    self.listing_languages.append(frame_language[index].lower().strip())

            if clean_word == 'front-end':
                self.listing_languages += ['html', 'css']


if __name__ == '__main__':
    new_listing = Listing(
        'https://www.seek.co.nz/job/76261214?type=promoted&ref=search-standalone&origin=cardTitle',
        72326820)
    new_listing.read_page()
    print(new_listing)
