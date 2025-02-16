import os
import pymongo

# MongoDB connection details (REPLACE WITH YOUR DETAILS)
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "d_3"
COLLECTION_NAME = "newstr"

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

def create_company_structure(root_dir):
    """Creates the nested company structure dictionary."""
    company_data = {}
    for company_name in os.listdir(root_dir):
        company_path = os.path.join(root_dir, company_name)
        if os.path.isdir(company_path):
            company_data[company_name] = {"company_name": company_name, "company_structure": []}
            for version_name in os.listdir(company_path):
                version_path = os.path.join(company_path, version_name)
                if os.path.isdir(version_path):
                    version_data = {"version_name": version_name, "version_structure": []}
                    for category_name in os.listdir(version_path):
                        category_path = os.path.join(version_path, category_name)
                        if os.path.isdir(category_path):
                            files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
                            version_data["version_structure"].append({"category_name": category_name, "category_structure": files})
                    company_data[company_name]["company_structure"].append(version_data)
    return list(company_data.values())  # Convert to a list of company dictionaries

def store_company_structure(company_data, collection):
    """Stores the company structure in MongoDB."""
    try:
        collection.insert_many(company_data)
        print("Company structure stored successfully.")
    except Exception as e:
        print(f"Error storing company structure: {e}")


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
    root_directory = "structure"  # Your root directory (relative to the script)
    collection = connect_to_mongodb()

    if collection is not None:  # Correct way to check the collection object
        company_structure = create_company_structure(root_directory)
        store_company_structure(company_structure, collection)
    else:
        print("Failed to connect to MongoDB.")