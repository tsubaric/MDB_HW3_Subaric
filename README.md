# MDB_HW3_Subaric

## Task 1: Connecting a Database to an Application

### Overview
The goal of this assignment is to become comfortable connecting a database to an application. You need to create an application that lets a user interact and manage the following tables from our in-class example:

![MDB_HW3_SUBARIC](moderndb_example.png)

### Getting Started

To get started with this assignment, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/your_repo.git

2. Connecting to Postgres Database with Python or Java
    * Python - https://www.postgresqltutorial.com/postgresql-python/connect/
   
3. Create Menu Functionality

Your menu interface should have the following functionality:

- **List all the countries:** Display a list of all the countries in the database.
    ```bash
    # Function to list all countries
    def list_countries(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT country_name FROM homework.countries")
                countries = cursor.fetchall()
                for country in countries:
                    print(country[0])
        except psycopg2.Error as e:
            print("Error listing countries:", e)

- **Search for/select a city/cities based on postal code, country code, and/or name:** Provide a search feature that allows users to search for and select cities using criteria such as postal code, country code, and city name.
    ```bash
    # Function to search for/select a city/cities based on postal code, country code, and/or name
    def search_cities(connection):
        try:
            with connection.cursor() as cursor:
                # Gather search criteria
                city_name = input("Enter the city name (leave empty for any): ")
                country_code = input("Enter the country code (leave empty for any): ")
                postal_code = input("Enter the postal code (leave empty for any): ")

                query = "SELECT * FROM homework.cities WHERE TRUE"
                parameters = []

                if city_name:
                    query += " AND name = %s"
                    parameters.append(city_name)

                if country_code:
                    query += " AND country_code = %s"
                    parameters.append(country_code)

                if postal_code:
                    query += " AND postal_code = %s"
                    parameters.append(postal_code)

                cursor.execute(query, parameters)
                cities = cursor.fetchall()

                if cities:
                    print("Matching cities:")
                    for city in cities:
                        print(city)
                else:
                    print("No cities found matching the criteria.")

        except psycopg2.Error as e:
            print("Error searching for cities:", e)

- **Add a new city to the cities table:** Implement a feature that enables users to add a new city to the cities table, including providing details such as city name, country code, and postal code.
    ```bash
    #Function to add a new city to the cities table
    def add_city(connection):
        try:
            with connection.cursor() as cursor:
                # Gather information for the new city
                city_name = input("Enter the city name: ")
                country_code = input("Enter the country code: ")
                postal_code = input("Enter the postal code: ")

                cursor.execute(
                    "INSERT INTO homework.cities (name, country_code, postal_code) "
                    "VALUES (%s, %s, %s)",
                    (city_name, country_code, postal_code)
                )
                connection.commit()  # Commit the transaction
                print(f"Added {city_name} to the cities table.")

        except psycopg2.Error as e:
            connection.rollback()  # Rollback the transaction in case of an error
            print("Error adding city:", e)

- **Update a city name, country code, and/or postal code:** Allow users to update existing city records by modifying attributes such as city name, country code, and postal code.
    ```bash
    #Function to update city information
    def update_city(connection):
        try:
            with connection.cursor() as cursor:
                city_name = input("Enter the city name to update: ")
                new_city_name = input("Enter the new city name: ")
                new_country_code = input("Enter the new country code: ")
                new_postal_code = input("Enter the new postal code: ")

                cursor.execute(
                    "UPDATE homework.cities "
                    "SET name = %s, country_code = %s, postal_code = %s "
                    "WHERE name = %s",
                    (new_city_name, new_country_code, new_postal_code, city_name)
                )
                connection.commit()  # Commit the transaction
                print(f"Updated information for {city_name}.")
        except psycopg2.Error as e:
            connection.rollback()  # Rollback the transaction in case of an error
            print("Error updating city:", e)

- **Delete a city:** Implement the ability to delete a city from the database.
    ```bash
    #Function to delete a city
    def delete_city(connection):
        try:
            with connection.cursor() as cursor:
                city_name = input("Enter the city name to delete: ")

                cursor.execute(
                    "SELECT name FROM homework.cities WHERE name = %s",
                    (city_name,)
                )
                existing_city = cursor.fetchone()

                if existing_city:
                    # Delete the city if it exists
                    cursor.execute(
                        "DELETE FROM homework.cities WHERE name = %s",
                        (city_name,)
                    )
                    connection.commit()  # Commit the transaction
                    print(f"{city_name} has been deleted from the cities table.")
                else:
                    print(f"{city_name} does not exist in the cities table.")
        except psycopg2.Error as e:
            connection.rollback()  # Rollback the transaction in case of an error
            print("Error deleting city:", e)

4. Create an inactive attribute in the venues table that acts as a flag indicating whether a venue
is active or not.
    ```bash
    ALTER TABLE venues
    ADD COLUMN inactive BOOLEAN DEFAULT FALSE;

5. Create a rule for the venues table – instead of deleting the venue(s) this rule will set the
active flag to false and the venue information will persist in the table.
    ```bash
    CREATE OR REPLACE RULE set_inactive_flag
    AS ON DELETE TO venues
    DO INSTEAD (
    UPDATE venues
    SET inactive = TRUE
    WHERE venue_id = OLD.venue_id;
    );

6. Additions to Menu
- **List all the active venues given a country code**
    ```bash
    # Function to list all active venues given a country code
    def active_venues(connection):
        try:
            with connection.cursor() as cursor:
                country_code = input("Enter the country code to list active venues: ")
                
                cursor.execute(
                    "SELECT venue_name FROM homework.venues WHERE country_code = %s AND inactive = FALSE",
                    (country_code,)
                )
                
                active_venues = cursor.fetchall()
                
                if active_venues:
                    print("Active venues in the specified country:")
                    for venue in active_venues:
                        print(venue[0])
                else:
                    print("No active venues found in the specified country.")
        except psycopg2.Error as e:
            print("Error listing active venues:", e)

- **List of the inactive venues**
    ```bash
    # Function to list all inactive venues
    def list_inactive(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT venue_name FROM homework.venues WHERE inactive = TRUE"
                )
                
                inactive_venues = cursor.fetchall()
                
                if inactive_venues:
                    print("Inactive venues:")
                    for venue in inactive_venues:
                        print(venue[0])
                else:
                    print("No inactive venues found.")
        except psycopg2.Error as e:
            print("Error listing inactive venues:", e)

- **Delete a venue using the venue name**
    ```bash
    # Function to delete a venue
    def delete_venue(connection):
        try:
            with connection.cursor() as cursor:
                venue_name = input("Enter the venue name to delete: ")
                
                cursor.execute(
                    "SELECT venue_name FROM homework.venues WHERE venue_name = %s",
                    (venue_name,)
                )
                
                existing_venue = cursor.fetchone()
                
                if existing_venue:
                    # Confirm with the user before deletion
                    confirm_delete = input(f"Do you want to delete the venue '{venue_name}'? (yes/no): ").strip().lower()
                    
                    if confirm_delete == "yes":
                        # Delete the venue
                        cursor.execute(
                            "DELETE FROM homework.venues WHERE venue_name = %s",
                            (venue_name,)
                        )
                        connection.commit()  # Commit the transaction
                        print(f"{venue_name} has been deleted.")
                    else:
                        print("Deletion canceled.")
                else:
                    print(f"Venue '{venue_name}' does not exist.")
        except psycopg2.Error as e:
            connection.rollback()  # Rollback the transaction in case of an error
            print("Error deleting venue:", e)

7. Prompt the user for the event information and use the add_event procedure to insert the
specified event into the table. Please add the following to the menu:

- **Add an Event**
    ```bash
    # Function to add an event using SQL INSERT query
    def add_event(connection):
        try:
            event_name = input("Enter event name: ")
            event_start = input("Enter event start date and time (YYYY-MM-DD HH:MI AM/PM): ")
            event_end = input("Enter event end date and time (YYYY-MM-DD HH:MI AM/PM): ")
            venue_name = input("Enter venue name: ")
            postal_code = input("Enter postal code: ")
            country_code = input("Enter country code: ")

            event_start = datetime.strptime(event_start, '%Y-%m-%d %I:%M %p')
            event_end = datetime.strptime(event_end, '%Y-%m-%d %I:%M %p')

            cursor = connection.cursor()

            cursor.execute(
                "SELECT venue_id FROM homework.venues WHERE name = %s AND postal_code = %s AND country_code = %s",
                (venue_name, postal_code, country_code)
            )
            venue_id = cursor.fetchone()

            if not venue_id:
                cursor.execute(
                    "INSERT INTO homework.venues (name, postal_code, country_code) VALUES (%s, %s, %s) RETURNING venue_id",
                    (venue_name, postal_code, country_code)
                )
                venue_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO homework.events (title, starts, ends, venue_id) VALUES (%s, %s, %s, %s)",
                (event_name, event_start, event_end, venue_id)
            )

            connection.commit()

            print("Event added successfully!")

        except Exception as e:
            print("Error:", e)
