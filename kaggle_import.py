import cx_Oracle
import csv

username = 'nadiya'
password = 'nadiya'
database = 'localhost:1521/xe'

conn = cx_Oracle.connect(username, password, database)

cursor = conn.cursor()

# Deleting data from tables
table_names = ['museum_income', 'museum', 'museum_type', 'museum_location', 'museum_state', 'museum_city']
for name in table_names:
    cursor.execute("DELETE FROM " + name)
    print('deleted data from ' + name)

# Opening of the file
with open('museums.csv', errors='ignore') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)

    unique_type = []
    unique_city = []
    unique_state = []
    unique_location = []

    for row in reader:
        museum_id = row[0].strip()
        museum_name = row[1].strip()
        museum_type = row[4].strip()
        city = row[7].strip()
        m_state = row[8].strip()
        income_date = row[22].strip()
        income = row[23].strip()

        # Inserting distinct into museum_type.
        if museum_type not in unique_type:
            unique_type.append(museum_type)
            cursor.execute('INSERT INTO museum_type (museum_type) VALUES (:museum_type)', museum_type=museum_type)

        # inserting distinct into museum_state.
        if m_state not in unique_state:
            unique_state.append(m_state)
            cursor.execute('INSERT INTO museum_state (m_state) VALUES (:m_state)', m_state=m_state)

        # Inserting distinct into museum_city.
        if city not in unique_city:
            unique_city.append(city)
            cursor.execute('INSERT INTO museum_city (city) VALUES (:city)', city=city)

        # Inserting distinct values into museum_location.
        location = [m_state, city]
        if location not in unique_location:
            unique_location.append(location)
            cursor.execute("INSERT INTO museum_location (m_state, city) VALUES (:state, :city)",
                           state=m_state, city=city)

        # Inserting data into museum table
        cursor.execute('''INSERT INTO museum (museum_id, museum_name, museum_type, m_state, city) 
                        VALUES (:museum_id, :museum_name, :museum_type, :state, :city)''',
                       museum_id=museum_id, museum_name=museum_name, museum_type=museum_type,
                       state=m_state, city=city)

        # Inserting data into museum_income table.
        cursor.execute('''
        INSERT INTO museum_income (museum_id, income, income_date)
        VALUES (:museum_id, :income, :income_date)
        ''', museum_id=museum_id, income=income, income_date=income_date)

    cursor.close()
    conn.commit()
