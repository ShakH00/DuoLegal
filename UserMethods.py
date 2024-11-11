import json
import os

import bcrypt
from bson import json_util
from pymongo import MongoClient
client = MongoClient(os.getenv("MONGO_KEY"))
db = client['sadsDB']
user_collection = db['users']
###
# First Name
# Last Name
# Email
# Password
# Concern
# Array = Evidence
###

###
# First Name
# Last Name
# Email
# Password
# Bar ID
# Speciality and University
# Bio
# Law Firm
###

class user:
    def __init__(self, name, lastname, email, password,location, concern, lawyer, lic=None, school=None, firm=None, documents=None, posts=None):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = self.hash_password(password)
        self.concern = concern
        self.location = location
        self.lawyer = lawyer
        self.lic = lic
        self.school = school if school is not None else None
        self.firm = firm if firm is not None else None
        self.documents = documents if documents is not None else []
        self.posts = posts if posts is not None else []


    # Convert user attributes to a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "location": self.location,
            "concern": self.concern,
            "lawyer": self.lawyer,
            "license": self.lic,
            "school": self.school,
            "firm": self.firm,
            "documents": self.documents,
            "posts": self.posts

        }

    def hash_password(self, password):
        """Hash a plaintext password with bcrypt."""
        salt = bcrypt.gensalt()  # Generate a salt
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
        return hashed

    def insert_doc(self):
        # Use the dictionary representation for insertion
        insert_doc = user_collection.insert_one(self.to_dict())
        print(f"Success, ID: {insert_doc.inserted_id}")

    def delete_doc(self):
        delete_doc = user_collection.delete_one(self.to_dict())
        return delete_doc.deleted_count

    def find_doc(self):
        person = user_collection.find_one(self.to_dict())
        return person


    def update_doc(self, identifier_doc, new_doc):
        # Ensure both parameters are dictionaries
        if isinstance(identifier_doc, user):
            identifier_doc = identifier_doc.to_dict()
        if isinstance(new_doc, user):
            new_doc = new_doc.to_dict()

        # Update the document in the database
        update_document = user_collection.update_one(identifier_doc, {"$set": new_doc})
        return update_document.modified_count

        # Helper function to convert BSON documents to JSON format

    def bson_to_json(self, data):
        return json.dumps(json.loads(json_util.dumps(data)), indent=4)

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by the user."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

# --------------------- General User Methods ----------------------------------


def get_all_users():
    # Retrieve all user documents and convert to a list
    users = list(user_collection.find())
    #all_users = get_all_users()
    return users


def get_user_credentials(email):
    # Use a dictionary as the filter
    curr = user_collection.find_one({"email": email})

    # Check if a user document was found
    if curr:
        return curr["email"], curr["password"]
    else:
        return None, None  # Return None values if the user is not found
