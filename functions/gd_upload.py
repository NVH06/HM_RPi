import os
import io
import pickle
from classes.cloud_info import GoogleDrive
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseUpload


def upload_gd(db_backup, logfile):
    print("-- GD UPLOAD FUNCTION INITIATED --")

    # OAuth 2.0 scope for accessing Google Drive
    scopes = ['https://www.googleapis.com/auth/drive']

    # Auth credentials
    client_secrets_file = GoogleDrive.client_secret_file
    token_pickle_file = GoogleDrive.token_pickle_file

    # Load or create the token.pickle file
    print("Authenticating ...")
    creds = None
    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available, authenticate and save the token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    # Create a Drive service using the authorized credentials
    drive_service = build('drive', 'v3', credentials=creds)

    # Get files already on Drive
    print("Checking files already on Google Drive...")

    folder_id = GoogleDrive.folder_id
    cur_files = []
    cur_file_ids = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"

    while True:
        response = drive_service.files().list(
            q=query,
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            cur_files.append(file['name'])
            cur_file_ids.append(file['id'])

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    # Upload the file to Google Drive
    print("Uploading files ...")
    upload_files = [db_backup, logfile]

    for file in upload_files:
        filename = os.path.basename(file)

        # Overwrite file if it already exists
        if filename in cur_files:
            id_index = cur_files.index(filename)
            id = cur_file_ids[id_index]

            file_metadata = {
                'name': filename,
                'addParents': [folder_id]
            }
            media = MediaIoBaseUpload(io.FileIO(file, 'rb'), mimetype='text/plain')

            upload = drive_service.files().update(
                fileId=id,
                body=file_metadata,
                media_body=media,
                fields='id'
                ).execute()

            print(f"Uploaded {filename}")

        # Upload new file if it does not already exist
        else:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media = MediaIoBaseUpload(io.FileIO(file, 'rb'), mimetype='text/plain')

            upload = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
                ).execute()

            print(f"Uploaded {filename}")

    print("Upload completed.")

# db_backup_file = r"C:\Users\Nils\Documents\Projects\Housing_Market\hm_backup\backup_test.txt"   ### change to directory path ###
# log_file = r"C:\Users\Nils\Documents\Projects\Housing_Market\log\hm_log.txt"   ### change to directory path ###
#
# upload_gd(db_backup_file, log_file)
