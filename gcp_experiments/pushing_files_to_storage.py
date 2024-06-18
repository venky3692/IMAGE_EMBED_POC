from google.cloud import storage

bucket_name = 'dppit-image-embedding-json'
source_file_name = '/home/venkateshriyer/Downloads/Dataset/Class_1.csv'
destination_blob_name = 'Class_1.csv'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)

print('File uploaded!')