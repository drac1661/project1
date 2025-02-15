import sqlite3

def sqlitte():
    # Connect to the SQLite database
    db_path = 'data/ticket-sales.db'
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Query to calculate total sales for "Gold" ticket type
    query = """
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE type = 'Gold';
    """

    # Execute the query
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Get the total sales value
    total_sales = result[0] if result[0] is not None else 0

    # Write the total sales to a text file
    output_path = 'data/ticket-sales-gold.txt'
    with open(output_path, 'w') as file:
        file.write(str(total_sales))

    # Close the cursor and connection
    cursor.close()
    conn.close()