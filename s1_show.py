import os
import pymongo

# MongoDB connection details (REPLACE WITH YOUR DETAILS)
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "s"
COLLECTION_NAME = "s1"


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


def get_filenames(collection, company_name, version_name, category_name):
    """Gets filenames from the nested structure."""
    try:
        result = collection.find_one(
            {"company_name": company_name},
            {
                "company_structure": {
                    "$elemMatch": {"version_name": version_name}
                }
            }
        )

        if result:
            for version in result.get("company_structure", []):
                if version["version_name"] == version_name:
                    for category in version.get("version_structure", []):
                        if category["category_name"] == category_name:
                            return category["category_structure"]
        return []
    except Exception as e:
        print(f"Error getting filenames: {e}")
        return []



if __name__ == "__main__":
    collection = connect_to_mongodb()

    if collection is not None:
        # Now, later in your program, you want to get the files for company1/v2/document:
        company_name = "company1"
        version_name = "v1"
        category_name = "document"
        filenames = get_filenames(collection, company_name, version_name, category_name)  # Use the function

        if filenames:
            print(f"Files: {filenames}")
        else:
            print("No files found.")
    else:
        print("failed to connect MongoDb")


 