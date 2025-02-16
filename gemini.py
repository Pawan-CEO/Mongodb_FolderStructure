import pymongo

# MongoDB connection details (replace with your connection string if needed)
MONGO_URI = "mongodb://localhost:27017/"  # Default connection string
DATABASE_NAME = "test_database"  # Name of the database to use
COLLECTION_NAME = "test_collection"  # Name of the collection to create

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]  # Access the database (will be created if it doesn't exist)
    collection = db[COLLECTION_NAME]  # Access the collection (will be created if it doesn't exist)

    # Optionally, insert a test document to verify
    result = collection.insert_one({"test1": "document"})
    if result.acknowledged:
        print(f"Collection '{COLLECTION_NAME}' created successfully in database '{DATABASE_NAME}'.")
        print(f"Inserted test document with ID: {result.inserted_id}")

    # You can also check if the collection exists using list_collection_names()
    if COLLECTION_NAME in db.list_collection_names():
        print(f"Collection '{COLLECTION_NAME}' exists")


except pymongo.errors.ConnectionFailure as e:
    print(f"Error connecting to MongoDB: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if client:
        client.close()  # Close the connection when done