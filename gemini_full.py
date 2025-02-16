import os
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB connection string
DATABASE_NAME = "my_file_storage"  # Replace with your database name (recommended to not use 'admin')
COLLECTION_NAME = "file_structure"  # Replace with your collection name

def connect_to_mongodb():
    """Connects to MongoDB and returns the collection object."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        return collection
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def store_file_structure(root_dir, collection):
    """Recursively traverses the directory structure and stores it in MongoDB."""

    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)

        if os.path.isdir(item_path):
            existing_dir = collection.find_one({"path": item_path})

            if not existing_dir:
                collection.insert_one({"path": item_path, "type": "directory", "files": []})
                print(f"Inserted directory: {item_path}")

            store_file_structure(item_path, collection)

        elif os.path.isfile(item_path):
            parent_dir = os.path.dirname(item_path)
            existing_file = collection.find_one({"path": parent_dir, "files": {"$elemMatch": {"name": item}}})

            if not existing_file:
                result = collection.update_one(
                    {"path": parent_dir},
                    {"$push": {"files": {"name": item, "path": item_path}}}
                )

                if result.modified_count > 0:
                    print(f"Inserted file: {item_path}")
                else:
                    # Handle the case where the parent directory isn't found (shouldn't happen with recursion)
                    print(f"Error: Parent directory not found for file {item_path}")  # Log or handle appropriately
                    # You might want to insert the parent directory here if it's truly missing.
                    collection.insert_one({"path": parent_dir, "type": "directory", "files": []})
                    result = collection.update_one(
                        {"path": parent_dir},
                        {"$push": {"files": {"name": item, "path": item_path}}}
                    )
                    if result.modified_count > 0:
                        print(f"Inserted file: {item_path}")
                    else:
                        print(f"Error: Parent directory not found for file {item_path}")

            else:
                print(f"File {item_path} already exists")

if __name__ == "__main__":
    root_directory = r"C:\Users\mailp\OneDrive\Desktop\m_mongo\structure" 
    collection = connect_to_mongodb()

    if collection is not None:  # Correct way to check if collection is valid
        store_file_structure(root_directory, collection)
        print("File structure stored successfully.")
    else:
        print("Failed to connect to MongoDB or get collection.")  # More informative message