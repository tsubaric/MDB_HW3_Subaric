# MDB_HW3_Subaric

## Task 1: Connecting a Database to an Application

### Overview
The goal of this assignment is to become comfortable connecting a database to an application. You need to create an application that lets a user interact and manage the following tables from our in-class example:

![MDB_HW3_SUBARIC](moderndb_example.png)

### Getting Started

To get started with this assignment, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/MDB_HW3_Subaric.git

2. Connecting to Postgres Database with Python or Java
    * Python - https://www.postgresqltutorial.com/postgresql-python/connect/
   
3. Once your database is connected, the next step is to design your menu interface. As mentioned above, this can be a command line interface. Unless explicitly stated, you should NOT add any additional constraints to the database but you are welcome to define views or functions if convenient. Your interface should handle errors/database messages and communicate these to the user within the program. If an error is encountered your program should prompt the user with a decision on what to do next (re-enter query, exit to main, etc)
Your menu interface should have the following functionality:
    • List all the countries
    • Search for/select a city/cities based on postal code, country code, and/or name
    • Add a new city to the cities table
    • Update a city name, country code, and/or postal code
    • Delete a city