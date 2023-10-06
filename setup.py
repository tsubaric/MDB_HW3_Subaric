import psycopg2
# Function to add an event using the add_event procedure
from datetime import datetime

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

# Function to search for/select a city/cities based on postal code, country code, and/or name
def search_cities(connection):
    try:
        with connection.cursor() as cursor:
            # Gather search criteria
            city_name = input("Enter the city name (leave empty for any): ")
            country_code = input("Enter the country code (leave empty for any): ")
            postal_code = input("Enter the postal code (leave empty for any): ")

            # Build the SQL query dynamically based on the provided criteria
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

# Function to add a new city to the cities table
def add_city(connection):
    try:
        with connection.cursor() as cursor:
            # Gather information for the new city
            city_name = input("Enter the city name: ")
            country_code = input("Enter the country code: ")
            postal_code = input("Enter the postal code: ")

            # Insert the new city into the table
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

# Function to update city information
def update_city(connection):
    try:
        with connection.cursor() as cursor:
            city_name = input("Enter the city name to update: ")
            new_city_name = input("Enter the new city name: ")
            new_country_code = input("Enter the new country code: ")
            new_postal_code = input("Enter the new postal code: ")

            # Update the city information
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

# Function to delete a city
def delete_city(connection):
    try:
        with connection.cursor() as cursor:
            city_name = input("Enter the city name to delete: ")

            # Check if the city exists before deleting
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

# Function to delete a venue
def delete_venue(connection):
    try:
        with connection.cursor() as cursor:
            venue_name = input("Enter the venue name to delete: ")
            
            # Check if the venue exists before proceeding
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

# Function to add an event using SQL INSERT query
def add_event(connection):
    try:
        # Prompt the user for event details
        event_name = input("Enter event name: ")
        event_start = input("Enter event start date and time (YYYY-MM-DD HH:MI AM/PM): ")
        event_end = input("Enter event end date and time (YYYY-MM-DD HH:MI AM/PM): ")
        venue_name = input("Enter venue name: ")
        postal_code = input("Enter postal code: ")
        country_code = input("Enter country code: ")

        # Format date and time strings as timestamps
        event_start = datetime.strptime(event_start, '%Y-%m-%d %I:%M %p')
        event_end = datetime.strptime(event_end, '%Y-%m-%d %I:%M %p')

        # Create a cursor
        cursor = connection.cursor()

        # Get venue_id or insert a new venue if it doesn't exist
        cursor.execute(
            "SELECT venue_id FROM homework.venues WHERE name = %s AND postal_code = %s AND country_code = %s",
            (venue_name, postal_code, country_code)
        )
        venue_id = cursor.fetchone()

        if not venue_id:
            # Venue doesn't exist, insert it
            cursor.execute(
                "INSERT INTO homework.venues (name, postal_code, country_code) VALUES (%s, %s, %s) RETURNING venue_id",
                (venue_name, postal_code, country_code)
            )
            venue_id = cursor.fetchone()[0]

        # Insert the event
        cursor.execute(
            "INSERT INTO homework.events (title, starts, ends, venue_id) VALUES (%s, %s, %s, %s)",
            (event_name, event_start, event_end, venue_id)
        )

        # Commit the transaction
        connection.commit()

        print("Event added successfully!")

    except Exception as e:
        # Handle any exceptions
        print("Error:", e)
        
def connect_to_postgresql():
    try:
        # Read credentials from credentials.txt
        with open('credentials.txt', 'r') as file:
            username = file.readline().strip()
            password = file.readline().strip()
        # Database connection parameters
        host = 's-l112.engr.uiowa.edu'
        port = 5432
        database = username 
            
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,  # Use the username read from credentials.txt
            password=password  # Use the password read from credentials.txt
        )
        
        while True:
            print("\nMenu:")
            print("1. List all countries")
            print("2. Search for/select a city")
            print("3. Add a new city")
            print("4. Update a city")
            print("5. Delete a city")
            print('6. List all active venues')
            print('7. List all inactive venues')
            print('8. Delete venue')
            print('9. Add Event')
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                list_countries(connection)
            elif choice == '2':
                search_cities(connection)
            elif choice == '3':
                add_city(connection)
            elif choice == '4':
                update_city(connection)
            elif choice == '5':
                delete_city(connection)
            elif choice == '6':
                active_venues(connection)
            elif choice == '7':
                list_inactive(connection)
            elif choice == '8':
                delete_venue(connection)
            elif choice == '9':
                add_event(connection)
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

        connection.close()  # Close the database connection when done
        print("Disconnected from the database.")

    except Exception as e:
        print("Error connecting to the database:", str(e))

if __name__ == "__main__":
    connect_to_postgresql()
