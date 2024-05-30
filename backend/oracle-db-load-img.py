import os
import oracledb

# Connect to the Oracle database
connection = oracledb.connect(user='imageUser', password='imageUser123', dsn='localhost:1521/XEPDB1')

# Define the path to the folder containing images
folder_path = "/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/text_test/"

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image (you can customize this check as needed)
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".PNG"):
        # Read the image data from the file
        image_file_path = os.path.join(folder_path, filename)
        with open(image_file_path, "rb") as image_file:
            image_data = image_file.read()

        # Insert the image data into the database
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO sys.images (image_data, image_name) VALUES (:1, :2)", [image_data, filename])
            connection.commit()
            print(f"Image '{filename}' inserted successfully.")
        except oracledb.Error as error:
            print(f"Error inserting image '{filename}':", error)
        finally:
            cursor.close()

# Close the database connection
connection.close()

