import pymssql
from ConnectionManager import ConnectionManager 

# instantiating a connection manager class and cursor
cm = ConnectionManager()
conn = cm.create_connection()
cursor = conn.cursor()

# example 1: getting all names and available doses in the vaccine table
get_all_vaccines = "SELECT name, doses FROM vaccines"
try:
    cursor.execute(get_all_vaccines)
    for row in cursor:
        print(f"name: {str(row['name'])}, available_doses: {str(row['doses'])}")
except pymssql.Error:     
    print("Error occurred when getting details from Vaccines")

# example 2: getting all records where the name matches “Pfizer”
get_pfizer = "SELECT * FROM vaccine WHERE name = %s"
try:
    cursor.execute(get_pfizer)
    for row in cursor:
        print(f"name: {str(row['name'])}, available_doses: {str(row['doses'])}")
except pymssql.Error:     
    print("Error occurred when getting pfizer from Vaccines")

