import mariadb
import sys

class DB():
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                host="localhost",
                port=3306,
                user="root",
                password="123456789",
                database="binsystem"
            )

            # Instantiate Cursor
            self.cur = self.conn.cursor()
            print("connection db succes",self.cur)  # This will print the cursor object for debugging

        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)

    def print_transaction(self):
        try:
            self.cur.execute("SELECT * FROM transaction LIMIT 10")  # Adjust this query based on your actual table name and columns
            for row in self.cur:
                print(row)
        except mariadb.Error as e:
            print(f"Error executing query: {e}")

    def close_connection(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except mariadb.Error as e:
            print(f"Error closing the connection: {e}")

    def insert_transaction(self, point, prediction, imagepath):
        try:
            self.cur.execute("INSERT INTO transaction (point, Prediction, imagepath) VALUES (?, ?, ?)", (point, prediction, imagepath))
            self.conn.commit()  # Make sure to commit the transaction
        except mariadb.Error as e:
            print(f"Error inserting data: {e}")
            
    def delete_transaction(self,transactionId):
        try:
            self.cur.execute("DELETE FROM transaction WHERE transactionId = ?",(transactionId,))
            self.conn.commit()  # Make sure to commit the transaction
        except mariadb.Error as e:
            print(f"Error inserting data: {e}")

    def select_transaction(self,transactionId):
        try:
            self.cur.execute("SELECT * FROM transaction WHERE transactionId =?",(transactionId,))
            for row in self.cur:
                print(row)
            return(self.cur)
        except mariadb.Error as e:
            print(f"Error inserting data: {e}")

    def create_transaction_table(self):
        try:
            self.cur.execute("""CREATE TABLE transaction (
                                transactionId INT AUTO_INCREMENT PRIMARY KEY,
                                stationId INT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                point INT,
                                Prediction VARCHAR(255),
                                imagepath VARCHAR(255)
                              )""")
            self.conn.commit()
            print("Table created successfully")
        except mariadb.Error as e:
            print(f"Error creating table: {e}")

            
if __name__ == '__main__':
    db = DB()
    # db.print_transaction()
    # db.insert_transaction(20, "test", "test_image_path.jpg")  # Adjusted call with correct arguments
    # print("after")
    # db.print_transaction()
    # print("deleted")
    # db.delete_transaction(10)
    # db.print_transaction()
    # db.select_transaction(2)
    # db.create_transaction_table()
    db.close_connection()
