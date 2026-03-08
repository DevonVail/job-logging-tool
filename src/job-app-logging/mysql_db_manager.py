import mysql.connector

class MySQLDatabaseManager:
    def __init__(self, mysql_conf):

        # Configuration for your MySQL server
        self.host = mysql_conf.host
        self.user = mysql_conf.user
        self.password = mysql_conf.password
        self.database_name = mysql_conf.db_name

        mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password
        )
    
        print("MySQL Connection established successfully.")

        # 2. Create a cursor object
        # A cursor is used to execute SQL statements
        self.db_cursor = mydb.cursor()

        self.setup_db()

    def setup_db(self):
        setup_query = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        self.db_cursor.execute(setup_query)

    def create_table(self):
        create_table_query = f"""
        CREATE TABLE jobs (
        ID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        URL TEXT NOT NULL,                  
        Title TEXT NOT NULL,                  
        Company TEXT NOT NULL,                  
        Location TEXT NOT NULL,                  
        Salary FLOAT,
        Salary_Type TEXT NOT NULL,
        Job_Type TEXT NOT NULL,          
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
        """
        self.db_cursor.execute(f"USE {self.database_name}")
        self.db_cursor.execute(create_table_query)
        self.db_cursor.execute("ALTER TABLE jobs AUTO_INCREMENT = 1;")
        
    def update_table(self, table_input):
        insert_query = f"""
        INSERT INTO jobs {list(table_input.keys())}
        VALUES {list(table_input.values())};
        """
        
        
        self.db_cursor.execute(f"USE {self.database_name}")
        self.db_cursor.execute(insert_query)

        self.db_cursor.execute("SELECT * FROM jobs;")
        print("\n\nTable\n\n")
        for table in self.db_cursor:
            print(table)


"""
try:
    # 1. Establish a connection to the MySQL server
    # Do not specify the database name here, as we are creating a new one
    mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=PASSWORD
    )
    
    print("MySQL Connection established successfully.")

    # 2. Create a cursor object
    # A cursor is used to execute SQL statements
    mycursor = mydb.cursor()

    # 3. Execute the CREATE DATABASE statement
    # Using "IF NOT EXISTS" prevents an error if the database already exists
    sql_query = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
    mycursor.execute(sql_query)

    print(f"Database '{self.database_name}' created or already exists.")

    # 4. Optional: Verify creation by listing databases
    mycursor.execute("SHOW DATABASES")
    print("\nList of Databases:")
    for db in mycursor:
        print(db)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    create_table(mycursor)
    update_table(mycursor)
    # Retrieve table
    mycursor.execute("SELECT * FROM jobs;")
    print("\n\nTable\n\n")
    for table in mycursor:
        print(table)
    # Drop the database?
    mycursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
    mycursor.execute("SHOW DATABASES")
    print("\n\nList of Databases 2:")
    for db in mycursor:
        print(db)
    # 5. Close the cursor and connection
    if 'mycursor' in locals() and mycursor is not None:
        mycursor.close()
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
        print("\nMySQL connection closed.")
"""

if __name__ == "__main__":
    MySQLDatabaseManager()