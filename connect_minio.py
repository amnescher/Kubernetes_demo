import argparse
from minio import Minio
from minio.error import S3Error
import os

from minio import Minio
from minio.error import S3Error

def list_objects_in_bucket(bucket_name, minio_client):
    """
    List all objects in the specified Minio bucket.

    Args:
    - bucket_name (str): The name of the Minio bucket to list the objects from.
    - minio_client (Minio): An authenticated Minio client instance.

    Returns:
    - List of object names (str) in the specified bucket.
    """
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        object_names = [obj.object_name for obj in objects]
        return object_names
    except S3Error as e:
        print(f"Error occurred while listing objects in bucket {bucket_name}: {e}")



def upload_to_minIO(ip_address, port, access_key, secret_key, bucketname, data_path):
    '''
    This takes in the following arguments:

    ip_address: The IP address of the MinIO server to connect to
    port: The port on which the MinIO server is running (default is 9000)
    access_key: The access key to use when authenticating with the MinIO server
    secret_key: The secret key to use when authenticating with the MinIO server
    bucketname: The name of the bucket to create on the MinIO server (if it doesn't already exist)
    data_path: The path to the directory containing the files to upload to the MinIO server
    
    The function first connects to the MinIO server using the given IP address, port, access key, and secret key. 
    It then checks if the specified bucket exists, and creates it if it doesn't. 
    Finally, it recursively iterates through the specified directory, and uploads each file to the specified bucket on the MinIO server.
    '''
    client = Minio(
        f"{ip_address}:{port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
    found = client.bucket_exists(bucketname)
    if not found:
        client.make_bucket(bucketname)
        print(f"Bucket {bucketname} was made")
    # Recursively iterate through the folder and upload each file to Minio bucket
    count = 0
    for root, dirs, files in os.walk(data_path):
        for file in files:
            filepath = os.path.join(root, file)
            # Upload the file to the bucket with the same structure as the original folder
            client.fput_object(bucketname, os.path.join(bucketname, os.path.relpath(filepath, data_path)), filepath)
            print(f"file uploaded {count}")
            count+=1
            
    print("Data Successfully Uploaded!")
    print(f"objects in {bucketname} are as follows.")
    minio_objects = list_objects_in_bucket(bucketname,client)
    for obj in minio_objects:
        print(obj)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip_address", help="specify IP address of minIO server")
    parser.add_argument("--port", default=9000, help="specify port of minIO server")
    parser.add_argument("--access_key", help="specify access_key of minIO server")
    parser.add_argument("--secret_key", help="specify secret_key of minIO server")
    parser.add_argument("--bucketname", default="modelweight", help="specify the bucket name to create on minIO cluster")
    parser.add_argument("--data_path", help="specify the path to directory to copy data to minIO bucket name to create on minIO cluster")
    args = parser.parse_args()
    upload_to_minIO(args.ip_address, args.port, args.access_key, args.secret_key, args.bucketname, args.data_path)
