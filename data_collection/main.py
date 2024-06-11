from bs4 import BeautifulSoup
import requests
from listing import Listing
import os
import datetime
import time
import pyodbc


def get_all_job_links(index, term):
    """Return the link to all job listings resulting from a search
     on seek.co.nz using the key terms 'Software Developer'"""
    # use the request library to access
    url = f"https://www.seek.co.nz/{term}-jobs?Page={index}&sortmode=ListedDate"
    html_code = requests.get(url).text
    soup = BeautifulSoup(html_code, 'lxml')
    # class names for all tags are hashed
    all_links = soup.select('a[id^="job-title-"]')
    # store all the links in the following list
    listings = []
    for links in all_links:
        if links['href'] not in listings:
            listings.append(f"https://www.seek.co.nz{links['href']}")
    # base case
    if not listings:
        print(f"Round Successfully Completed")
        return []
    return listings + get_all_job_links(index + 1, term)


def insert_listing(listing_instance, connection):
    cursor = connection.cursor()
    # values from each listing
    region = listing_instance.region
    suburb = listing_instance.suburb
    salary = listing_instance.salary
    job_type = listing_instance.job_type
    company = listing_instance.company
    list_date = listing_instance.listed_date
    listing_id = listing_instance.listing_id
    is_active = 1
    # query to insert into table Listing
    insert_query = "INSERT INTO Listing (ListingID, region, suburb, salary, jobType, company, listingDate, isActive) " \
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    # code to confirm the insert worked
    try:
        cursor.execute(insert_query, (listing_id, region, suburb, salary, job_type, company, list_date, is_active))
        connection.commit()
    except pyodbc.Error as ex:
        print("Error inserting values:", ex)
        connection.rollback()
    # closes the connection
    cursor.close()


def insert_listing_language(listing_instance, connection):
    cursor = connection.cursor()
    languages = listing_instance.listing_languages

    for language in languages:
        select_query = "SELECT LanguageID FROM Language WHERE name LIKE ?"
        insert_query = "INSERT INTO ListingLanguage (LanguageID, ListingID) VALUES (?, ?)"

        try:
            cursor.execute(select_query, (language,))
            language_id = cursor.fetchone()[0]  # Fetches the LanguageID from the select query result

            cursor.execute(insert_query, (language_id, listing_instance.listing_id))
            connection.commit()
        except pyodbc.Error as ex:
            print("Error inserting values:", ex)
            connection.rollback()

    cursor.close()


def insert_listing_framework(listing_instance, connection):
    cursor = connection.cursor()
    frameworks = listing_instance.technologies

    for framework in frameworks:
        select_query = "SELECT FrameworkID FROM Framework WHERE name LIKE ?"
        insert_query = "INSERT INTO ListingFramework (FrameworkID, ListingID) VALUES (?, ?)"

        try:
            cursor.execute(select_query, (framework,))
            framework_id = cursor.fetchone()[0]  # Fetches the FrameworkID from the select query result
            cursor.execute(insert_query, (framework_id, listing_instance.listing_id))
            connection.commit()
        except pyodbc.Error as ex:
            print("Error inserting values:", ex)
            connection.rollback()

    cursor.close()


def primary_key_exists(connection, table_name, primary_key_value, primary_key_column):
    cursor = connection.cursor()
    sql_query = f"SELECT 1 FROM {table_name} WHERE {primary_key_column} = ?"
    cursor.execute(sql_query, primary_key_value)
    exists = bool(cursor.fetchone())
    cursor.close()
    return exists


def get_listing_id(url):
    # splits the URL between the domain and path side, vs the query and parameter side
    # the ID is the last part of the path 'job/213124234;, where 213124234 is the ID
    url_split = url.split('?')  # ? separates both parts of the URL
    domain_and_path = url_split[0]
    return domain_and_path[-8:]  # id part is 8 characters long


def update_active(connection, all_found_ids):
    cursor = connection.cursor()
    cursor.execute("SELECT ListingID FROM Listing")
    all_database_ids = cursor.fetchall()
    for rows in all_database_ids:
        listing_id = rows[0]
        if listing_id not in all_found_ids:
            cursor.execute("UPDATE Listing SET isActive = ? WHERE ListingID = ?", (0, listing_id))
            cursor.commit()
        elif listing_id in all_found_ids:
            cursor.execute("UPDATE Listing SET isActive = ? WHERE ListingID = ?", (1, listing_id))
            cursor.commit()


def update_database(connection):
    # Connects to the database
    print("Searching for listings.")
    all_found_ids = []
    array = get_all_job_links(1, 'software-developer')
    print(f"{len(array)} Listings found in total")

    print("Inserting data into database")

    # data to be recorded for documentation
    number_of_errors = 0
    errors = []  # saves error messages for report
    counter = 0  # records the number of listings
    new_listing = "None added"
    for link in array:
        link_id = int(get_listing_id(link))
        all_found_ids.append(link_id)
        if not primary_key_exists(connection, 'listing', link_id, 'ListingID'):
            counter += 1
            try:
                new_listing = Listing(link, link_id)
                insert_listing(new_listing, connection)
                insert_listing_language(new_listing, connection)
                insert_listing_framework(new_listing, connection)
            except Exception as e:
                number_of_errors += 1
                errors.append(e)
                print(f"Error inserting listing {link} {e}")
    if len(all_found_ids) > 0:
        update_active(connection, all_found_ids)
    print(f"Number of new listings found: {counter}")
    print(f"Number of errors: {number_of_errors}")
    print(f"Time Completed: {datetime.datetime.now()}")
    write_report(len(array), counter, number_of_errors, errors, new_listing)


def write_report(total_listings, unique_listings_found, error_count, errors, listing_example):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    content = f"REPORT {timestamp}" \
              f"\n- Number of listings found: {total_listings}" \
              f"\n- Number of unique listings found: {unique_listings_found}" \
              f"\n- Number of errors encountered: {error_count}" \
              f"\n- Listing Example: {listing_example}\nERRORS"
    for i in range(len(errors)):
        content += f"\n{i + 1} {errors[i]}"

    # Create a folder named 'reports' if it doesn't exist
    folder_path = os.path.join(os.getcwd(), 'reports')
    os.makedirs(folder_path, exist_ok=True)

    # Create and write to the text file
    file_path = os.path.join(folder_path, f'report_{timestamp}.txt')
    with open(file_path, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    # automated scraper, runs every 4 hours
    while True:
 
        conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',
                              server='YOUR DB IP HERE',
                              database='YOUR DB NAME HERE',
                              uid='DB ID HERE',
                              pwd='DB PASSWORD')
        print(f"Successfully connected to server")

        update_database(conn)
        conn.close()
        print(f"Next update scheduled for {datetime.datetime.now() + datetime.timedelta(hours=24)}")
        time.sleep(14400)
        


