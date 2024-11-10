import base64
from pymongo import MongoClient
import re


#mongo db stuff
#client = MongoClient("mongodb+srv://saqibmaz:Mongodb%40Modulo48@cluster0.beh24.mongodb.net/?retryWrites=true&w=majority", ssl = True)
client = MongoClient("mongodb+srv://MrVarmint_gw:5HUInvuir2390@cluster0.6fkb0.mongodb.net/cstuff?retryWrites=true&w=majority")

db = client['sadsDB']
user_collection = db['users']

# Function to encode a file as Base64
def encode_file(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# Function to sanitize filenames by removing invalid characters
def sanitize_filename(filename):
    # Remove invalid characters using a regular expression
    return re.sub(r'[<>:"/\\|?*]', '', filename)
# Upload function that adds the encoded file to a user's document


def add_document_to_user(user_identifier, file_path):
    # Read and encode the file in Base64 format
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode("utf-8")

    # Prepare the document entry with metadata (optional)
    document_entry = {
        "filename": file_path.split("/")[-1],  # Extracts the filename
        "data": encoded_file
    }

    # Update user's document array by appending the new document
    user_collection.update_one(
        {"email": user_identifier},  # Filter by user identifier (e.g., email)
        {"$push": {"documents": document_entry}}  # Add document to documents array
    )
    print(f"Document '{file_path}' added to user '{user_identifier}'.")


def download_user_documents(user_identifier):
    # Retrieve the user's documents array
    user = user_collection.find_one({"email": user_identifier}, {"documents": 1})

    # Check if the user and their documents exist
    if user and "documents" in user:
        for index, document in enumerate(user["documents"], start=1):
            # Decode the Base64 data
            pdf_data = base64.b64decode(document["data"])

            # Define a unique filename, sanitizing the original filename
            original_filename = document.get("filename", "unknown")
            sanitized_filename = sanitize_filename(original_filename)
            output_path = f"Downloaded Document {index} - {sanitized_filename}"

            # Write the binary data to a file
            with open(output_path, "wb") as pdf_file:
                pdf_file.write(pdf_data)

            print(f"PDF file saved as {output_path}")
    else:
        print("No documents found for the specified user.")