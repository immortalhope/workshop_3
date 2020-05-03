import cx_Oracle
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import re
import chart_studio.dashboard_objs as dashboard


def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')


chart_studio.tools.set_credentials_file('immortal_hope', 'U9n78L48XKgiXzsl1tLO')

username = 'nadiya'
password = 'nadiya'
database = 'localhost:1521/xe'

connection = cx_Oracle.connect(username, password, database)
# -------------------------------------------
# Перший запит. Кругова діаграма з відсотковим віднощенням кількості всіх типів музеїв у мість Нью-Йорк
# -------------------------------------------
query = """

SELECT  
 museum_type,
COUNT(*)
FROM type_museum
INNER JOIN museum_location ON type_museum.m_state = museum_location.m_state and type_museum.city = museum_location.city
WHERE museum_location.city = 'NEW YORK'
GROUP BY museum_type

"""

cursor = connection.cursor()

cursor.execute(query)

museum_type = []
amount = []
for data in cursor.fetchall():
    museum_type.append(data[0])
    amount.append(data[1])

# print(museum_type, amount)


data = go.Pie(labels=museum_type, values=amount)
# fig = go.Figure(data)
# fig.show()
art_galleries_in_ny = py.plot([data], auto_open=True, filename='oracle_data')

#  ------------------------------
# Другий запит. Графык залежносты між типом музею та прибутком.
#--------------------------------
query1 = """
SELECT AVG(income) AS Avg_income_per_type, 
    type_museum.museum_type as museum_type
from museum_income
INNER JOIN type_museum ON museum_income.museum_id = type_museum.museum_id
group by type_museum.museum_type
"""

cursor1 = connection.cursor()

cursor1.execute(query1)

avg_income = []
museum_type = []

for data in cursor1.fetchall():
    avg_income.append(data[0])
    museum_type.append(data[1])

data1 = go.Scatter(x=museum_type, y=avg_income)
type_income = py.plot([data1], auto_open=True, filename='oracle_data_1')

# ----------------------------------
# Третій запит. Стовпчикова діаграма зі штатами та кількістю історичниx пам'яток, що знаходяться на їxній території.
# ----------------------------------
query2 = """
SELECT museum_location.m_state as museum_state, 
        COUNT(*) as amount
FROM museum_location
INNER JOIN type_museum ON museum_location.m_state = type_museum.m_state and museum_location.city = type_museum.city
INNER JOIN museum_state ON museum_location.m_state = museum_state.m_state
WHERE type_museum.museum_type = 'HISTORIC PRESERVATION'
group by museum_location.m_state
order by amount DESC
"""

cursor2 = connection.cursor()

cursor2.execute(query2)

state = []
amount = []
for data in cursor2.fetchall():
    state.append(data[0])
    amount.append(data[1])

data2 = go.Bar(x=state, y=amount)
historic_preservations = py.plot([data2], auto_open=True, filename='oracle_data_2')


art_galleries_url = fileId_from_url(art_galleries_in_ny)
income_type_url = fileId_from_url(type_income)
historic_preservations_ulr = fileId_from_url(historic_preservations)

my_dboard = dashboard.Dashboard()

box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': art_galleries_url,
    'title': 'Galleries in NY '
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId':  income_type_url,
    'title': 'Income per type'
}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId':  historic_preservations_ulr,
    'title': 'Historic preservation amount'
}

my_dboard.insert(box_2)
my_dboard.insert(box_3, 'below', 1)
my_dboard.insert(box_1, 'left', 2)

py.dashboard_ops.upload(my_dboard, 'My dashboard')

cursor.close()
connection.close()
