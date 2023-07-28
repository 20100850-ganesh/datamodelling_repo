import mysql.connector
import diseases

if __name__ == "__main__":
    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="proto",
        password="password",
        database="ricediseasesdb"
    )

    # Create a cursor to execute queries
    cursor = db.cursor()

    # Loop through the list of diseases and insert the information into the database
    for disease in diseases.DISEASES:
        # Insert the disease information into the diseases table
        query = "INSERT INTO diseases (name, description) VALUES (%s, %s)"
        values = (disease['name'], disease['description'])
        cursor.execute(query, values)
        db.commit()

        # Insert the control methods for the disease into the control_methods table
        disease_id = cursor.lastrowid
        for method in disease['control_methods']:
            query = "INSERT INTO control_methods (disease_id, method) VALUES (%s, %s)"
            values = (disease_id, method)
            cursor.execute(query, values)
            db.commit()

    # Close the database connection
    db.close()
