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
    """Stores/Updates the company structure in MongoDB."""
    for company in company_data:
        existing_company = collection.find_one({"company_name": company["company_name"]})

        if existing_company:
            # Company exists, update it
            for version in company["company_structure"]:
                existing_version = next((v for v in existing_company["company_structure"] if v["version_name"] == version["version_name"]), None)

                if existing_version:
                    for category in version["version_structure"]:
                        existing_category = next((c for c in existing_version["version_structure"] if c["category_name"] == category["category_name"]), None)

                        if existing_category:
                            # Category exists, update (add new files if any)
                            new_files = [f for f in category["category_structure"] if f not in existing_category["category_structure"]]
                            if new_files:
                                collection.update_one(
                                    {"company_name": company["company_name"], "company_structure.version_name": version["version_name"], "company_structure.version_structure.category_name": category["category_name"]},
                                    {"$push": {"company_structure.$[outer].version_structure.$[inner].category_structure": {"$each": new_files}}},
                                    array_filters=[{"outer.version_name": version["version_name"]}, {"inner.category_name": category["category_name"]}]
                                )
                                print(f"Updated {company['company_name']}/{version['version_name']}/{category['category_name']}: Added {new_files}")
                        else:
                            # Category doesn't exist, add it
                            collection.update_one(
                                {"company_name": company["company_name"], "company_structure.version_name": version["version_name"]},
                                {"$push": {"company_structure.$[outer].version_structure": category}},
                                array_filters=[{"outer.version_name": version["version_name"]}]
                            )
                            print(f"Added category {category['category_name']} to {company['company_name']}/{version['version_name']}")

                else:
                    # Version doesn't exist, add it
                    collection.update_one(
                        {"company_name": company["company_name"]},
                        {"$push": {"company_structure": version}}
                    )
                    print(f"Added version {version['version_name']} to {company['company_name']}")


        else:
            # Company doesn't exist, insert it
            collection.insert_one(company)
            print(f"Inserted company: {company['company_name']}")





if __name__ == "__main__":
    root_directory = "structure"  # Your root directory
    collection = connect_to_mongodb()

    if collection is not None:  # Correct way to check the collection object
        company_structure = create_company_structure(root_directory)
        store_company_structure(company_structure, collection)  # Call ONCE

    else:
        print("Failed to connect to MongoDB.")


