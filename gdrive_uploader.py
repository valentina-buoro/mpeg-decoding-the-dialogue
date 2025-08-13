
import os
import zipfile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def create_zip(folder_path, zip_name):
    """Create zip file from folder"""
    print(f"Creating zip: {zip_name}")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Skip virtual environment folders
            dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '__pycache__']]

            for file in files:
                if not file.endswith('.pyc'):  # Skip Python cache files
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arc_path)

    print(f"✅ Zip created: {zip_name}")
    return zip_name


def upload_to_drive(file_path):
    """Upload file to Google Drive"""
    # Authenticate
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens browser for authentication
    drive = GoogleDrive(gauth)

    # Upload file
    filename = os.path.basename(file_path)
    print(f"Uploading {filename} to Google Drive...")

    file = drive.CreateFile({'title': filename})
    file.SetContentFile(file_path)
    file.Upload()

    print(f"✅ Upload complete!")
    print(f"File ID: {file['id']}")


# Main function
def backup_project(project_path):
    """Backup project to Google Drive"""
    if not os.path.exists(project_path):
        print(f"Error: {project_path} not found")
        return

    # Create zip
    project_name = os.path.basename(project_path)
    zip_name = f"{project_name}_backup.zip"
    create_zip(project_path, zip_name)

    # Upload to Drive
    upload_to_drive(zip_name)

    # Clean up
    os.remove(zip_name)
    print("🗑️ Cleaned up local zip file")


if __name__ == "__main__":
    # Change this path to your project folder
    project_path = './TrainFiles'
    backup_project(project_path)