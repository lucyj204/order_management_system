## **Order Management System**

An order management system that can store orders along with their products referred to as orderlines.

### **Tools used:**
- Python
- MySQL

### **Instructions**

This project uses MySQL Connector/ Python. If you would like to run the project and do not have MySQL Connector/ Python installed, please use the below command:

pip install mysql-connector-python

#### **Setting up the database**

In the folder 'MySQL_DB', the SQL code to create the database can be found. Please run this code in a MySQL file to create the order_management DB.

I have provided a config file for mysql.connector. Please update the file with your details in order to connect to the DB.

#### **Using the CLI**

Please run the main.py file to start the CLI. This will show you a list of commands and inventory options.

#### **Tests**

Tests for the system can be found in test.main.py. 

test.db_utils.py contains a test for the connection to the DB.