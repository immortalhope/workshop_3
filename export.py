import csv
import cx_Oracle

username = 'nadiya'
password = 'nadiya'
database = 'localhost:1521/xe'

conn = cx_Oracle.connect(username, password, database)

# Writing from museum table.
cursor_museum = conn.cursor()

cursor_museum.execute('''
    SELECT
    TRIM(museum_id) as museum_id,
    TRIM(museum_name) as museum_name,
    TRIM(museum_type) as museum_type,
    TRIM(m_state) as state, 
    TRIM(city) as city
    FROM museum
''')

row = cursor_museum.fetchall()

with open('museum_table.csv', "w", newline='') as file:
    writer = csv.writer(file, delimiter=',')

    writer.writerow(['Id', 'Name', 'Type', 'State', 'City'])
    for elm in row:
        writer.writerow(elm)

    cursor_museum.close()

# Getting data from museum_type table.
cursor_type = conn.cursor()

cursor_type.execute('''
SELECT 
TRIM(museum_type) as museum_type
FROM museum_type
''')

row = cursor_type.fetchall()

with open('type_table.csv', "w", newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Type'])

    for elm in row:
        writer.writerow(elm)
    cursor_type.close()


# Writing from museum_location table.
cursor_location = conn.cursor()

cursor_location.execute('''
SELECT 
TRIM(m_state) as state,
TRIM(city) AS city
FROM museum_location
''')

row = cursor_location.fetchall()

with open('location_table.csv', "w", newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['State', 'City'])

    for elm in row:
        writer.writerow(elm)
    cursor_location.close()

# Writing from museum_income table.
cursor_income = conn.cursor()

cursor_income.execute('''
SELECT 
TRIM(museum_id) as museum_id, 
TRIM(income) as income,
TRIM(income_date) as income_date
FROM museum_income
''')

row = cursor_income.fetchall()

with open('income_table.csv', "w", newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['ID', 'Income', 'Date'])

    for elm in row:
        writer.writerow(elm)
    cursor_income.close()
