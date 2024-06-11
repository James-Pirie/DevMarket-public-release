import pyodbc


def insert_language(connection, language_id: int, language_name: str):
    cursor = connection.cursor()
    insert_query = "INSERT INTO Language (LanguageID, name) VALUES (?, ?)"
    try:
        cursor.execute(insert_query, (language_id, language_name))
        connection.commit()
        print("Values inserted successfully!")
    except pyodbc.Error as ex:
        print("Error inserting values:", ex)
        connection.rollback()
    cursor.close()


def setup_language_table(connection):
    languages_file = open("languages.txt", 'r')
    languages = languages_file.read().split()
    for i in range(len(languages)):
        insert_language(connection=connection, language_id=i, language_name=languages[i])


def insert_framework(connection, language_name: str, framework_id: int, framework_name: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT LanguageID FROM Language WHERE name LIKE '{language_name}'")
    language_id = cursor.fetchone()[0]
    insert_query = "INSERT INTO Framework (FrameworkID, LanguageID, name) VALUES (?, ?, ?)"
    try:
        cursor.execute(insert_query, (framework_id, language_id, framework_name))
        connection.commit()
        print("Values inserted successfully!")
    except pyodbc.Error as ex:
        print("Error inserting values:", ex)
        connection.rollback()
    cursor.close()


def setup_framework_table(connection):
    framework_file = open("all_frameworks.txt", 'r')
    framework_data = framework_file.read().split()
    for i in range(len(framework_data)):
        framework_name = framework_data[i].split(',')[0]
        language_name = framework_data[i].split(',')[1]
        insert_framework(connection, language_name, i, framework_name)


if __name__ == '__main__':
    conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',
                          server='YOUR DB IP HERE',
                          database='YOUR DB NAME HERE',
                          uid='DB ID HERE',
                          pwd='DB PASSWORD')

    setup_language_table(conn)
    setup_framework_table(conn)
    conn.close()

