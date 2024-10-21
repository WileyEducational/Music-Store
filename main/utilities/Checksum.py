import hashlib

class ChecksumUtility:
    @staticmethod
    def calculate_checksum(file_path: str) -> str:
        """Calculate checksum of a file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as file:
            chunk = 0
            while chunk := file.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()