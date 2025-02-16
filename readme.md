# File Structure Storage in MongoDB

This project demonstrates how to store and manage a file structure in MongoDB using Python. It provides scripts to insert/update the file structure and to retrieve file lists for specific company/version/category combinations.

## Setup

### 1. Python Environment

It is highly recommended to use a virtual environment to manage your project dependencies.

```bash
# Create a virtual environment (replace myenv with your preferred name)
python -m venv myenv

# Activate the virtual environment (Windows)
myenv\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source myenv/bin/activate
2. Requirements
Install the required Python packages using pip:

Bash

pip install -r requirements.txt

3. MongoDB Setup
Starting MongoDB Locally
Ensure you have MongoDB installed. If not, download and install it from the official MongoDB website: https://www.mongodb.com/try/download/community

Start the MongoDB server. The exact command depends on your installation, but it's usually something like:

Bash

mongod --dbpath <path_to_your_data_directory> 
Replace <path_to_your_data_directory> with the directory where you want MongoDB to store its data files.  If you don't specify --dbpath, MongoDB will use a default location (which may vary depending on your operating system).

It is recommended to run mongod in a separate terminal window.

4. File Structure Creation (CMD)
The create_structure.bat file contains the Windows command prompt commands to create the file and folder structure.

Create a create_structure.bat file in the same directory as your Python scripts.
Copy and paste the following commands into the create_structure.bat file and save it:
<!-- end list -->

Code snippet

mkdir company1
mkdir company1\v1
mkdir company1\v1\certificate
echo "" > company1\v1\certificate\filec1.txt
echo "" > company1\v1\certificate\filec12.txt
mkdir company1\v1\document
echo "" > company1\v1\document\file1.txt
echo "" > company1\v1\document\file2.txt
mkdir company1\v2
mkdir company1\v2\certificate
echo "" > company1\v2\certificate\file1.txt
mkdir company1\v2\document
echo "" > company1\v2\document\file1.txt
mkdir company1\v3
mkdir company1\v3\checkfolder
echo "" > company1\v3\checkfolder\file1.txt

mkdir company2
mkdir company2\v1
mkdir company2\v1\document
echo "" > company2\v1\document\file1.txt

mkdir company3
mkdir company3\v2
mkdir company3\v2\document
echo "" > company3\v2\document\file1.txt
mkdir company3\v3
mkdir company3\v3\certificate
echo "" > company3\v3\certificate\file1.txt

mkdir company4
mkdir company4\v1
mkdir company4\v1\document
echo "" > company4\v1\document\file1.txt
mkdir company4\v2
mkdir company4\v2\document
echo "" > company4\v2\document\file1.txt
Run the batch file from the command prompt: create_structure.bat
This will create a structure folder in the same directory, with all the nested company/version/category directories and empty files.

Running the Scripts
s1.py (Insert/Update File Structure)
This script reads the file structure created by the create_structure.bat file and stores it in your MongoDB database.  It also handles updates – if you add new files to the file system, running s1.py again will update the database accordingly.

Make sure your MongoDB server is running.
Activate your Python virtual environment.
Run the script: python s1.py
s1_show.py (Show Files)
This script demonstrates how to retrieve file lists from the MongoDB database.  You can modify the company_name, version_name, and category_name variables in the script to query for different file lists.

Make sure your MongoDB server is running.
Activate your Python virtual environment.
Run the script: python s1_show.py
MongoDB Configuration
Remember to update the MONGO_URI, DATABASE_NAME, and COLLECTION_NAME variables in both s1.py and s1_show.py to match your MongoDB connection details.  It is highly recommended to create a separate database and user for this project (instead of using the admin database) for security best practices.