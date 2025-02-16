import os
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "newstr"  # Or your database name
COLLECTION_NAME = "file_structure"


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

def store_file_structure(root_dir, collection, base_path=""):
    """Recursively traverses and stores file structure."""
    full_dir_path = os.path.join(base_path, root_dir)  # Construct the full path
    try:  # Handle potential FileNotFoundError
        for item in os.listdir(full_dir_path):
            item_path = os.path.join(full_dir_path, item)
            relative_item_path = os.path.join(root_dir, item)  # Relative path for the database

            if os.path.isdir(item_path):
                existing_dir = collection.find_one({"path": relative_item_path})

                if not existing_dir:
                    collection.insert_one({"path": relative_item_path, "type": "directory", "files": []})
                    print(f"Inserted directory: {relative_item_path}")

                store_file_structure(item, collection, full_dir_path)  # Correct recursive call!

            elif os.path.isfile(item_path):
                parent_dir = os.path.dirname(relative_item_path)
                existing_file = collection.find_one({"path": parent_dir, "files": {"$elemMatch": {"name": item}}})

                if not existing_file:
                    result = collection.update_one(
                        {"path": parent_dir},
                        {"$push": {"files": {"name": item, "path": relative_item_path}}}
                    )

                    if result.modified_count > 0:
                        print(f"Inserted file: {relative_item_path}")
                    else:
                        print(f"Error: Parent directory not found for file {relative_item_path}")
                        collection.insert_one({"path": parent_dir, "type": "directory", "files": []})  # Create parent if missing
                        result = collection.update_one(
                            {"path": parent_dir},
                            {"$push": {"files": {"name": item, "path": relative_item_path}}}
                        )
                        if result.modified_count > 0:
                            print(f"Inserted file: {relative_item_path}")
                        else:
                            print(f"Error: Parent directory STILL not found for file {relative_item_path}")

                else:
                    print(f"File {relative_item_path} already exists")

    except FileNotFoundError:
        print(f"Error: Directory not found: {full_dir_path}")

def get_filenames(collection, relative_path):  # Modified to accept relative path
    full_path = os.path.join(root_directory, relative_path) #create full path
    result = collection.find_one(
        {"path": full_path},  # Use the full path in the query
        {"files.name": 1, "_id": 0}
    )
    if result and "files" in result:
        return [file["name"] for file in result["files"]]
    else:
        return []

if __name__ == "__main__":
    root_directory = "structure"
    collection = connect_to_mongodb()

    if collection is not None:
        store_file_structure(root_directory, collection)  # Correct call to store_file_structure
        # ... (rest of the code remains the same)
    else:
        print("Failed to connect to MongoDB or get collection.")
