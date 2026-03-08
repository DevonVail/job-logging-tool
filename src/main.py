import mysql.connector

# 1. Establish the database connection
try:
    mydb = mysql.connector.connect(
      host="localhost",          # Your host name
      user="root",       # Your MySQL username
      password="Derbydog11",   # Your MySQL password
      database="mydatabase"      # The database you want to use
    )
    print("Database connection established successfully!")

except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    exit()

# 2. Create a cursor object
mycursor = mydb.cursor()

# 3. Define the SQL CREATE TABLE statement
# The IF NOT EXISTS clause prevents an error if the table already exists.
# Example data types include INT, VARCHAR(255), etc.
sql_query = """
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255)
)
"""

# 4. Execute the query
try:
    mycursor.execute(sql_query)
    print("Table 'customers' created successfully or already exists.")

except mysql.connector.Error as err:
    print(f"Failed to create table: {err}")

# 5. Close the cursor and connection
mycursor.close()
mydb.close()