import os
import shutil

class FileHandler:
    current_directory = os.path.dirname(os.path.abspath(__file__))  
    uploads_folder = os.path.abspath(os.path.join(current_directory, "..", "uploads"))

    @staticmethod
    def uploaded_file_path(file_path: str) -> str:
        upload_filename = os.path.basename(file_path)
        upload_path = os.path.join(FileHandler.uploads_folder, upload_filename)
        return upload_path

    @staticmethod
    def copy_file_to_uploads(file_path: str) -> str:
        upload_path = FileHandler.uploaded_file_path(file_path)
        
        if os.path.exists(upload_path):
            raise FileExistsError(f"A file with the name '{os.path.basename(file_path)}' already exists in the uploads folder.")
        
        os.makedirs(FileHandler.uploads_folder, exist_ok=True)
        shutil.copy2(file_path, upload_path)
        return upload_path

    @staticmethod
    def replace_file(existing_file_path: str, new_file_path: str) -> None:
        if not os.path.exists(existing_file_path):
            raise FileNotFoundError(f"The file '{existing_file_path}' does not exist.")
        
        os.remove(existing_file_path)
        shutil.copy2(new_file_path, existing_file_path)