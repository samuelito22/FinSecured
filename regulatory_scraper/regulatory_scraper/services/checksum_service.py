from sqlalchemy.orm import Session
from regulatory_scraper.database.models import DocumentChecksum
from sqlalchemy.sql import func

class ChecksumService:
    def __init__(self, session: Session):
        self.session = session

    def add_checksum(self, file_url, checksum):
        """
        Add a new checksum entry to the database.
        Parameters:
            file_url (str): URL of the file to which the checksum corresponds.
            checksum (str): The checksum value for the file.
        Returns:
            DocumentChecksum: The newly created checksum entry.
        """
        if self.get_checksum_by_url(file_url):
            raise ValueError("A checksum entry already exists for this URL.")
        new_checksum = DocumentChecksum(
            file_url=file_url,
            checksum=checksum,
            last_accessed=func.now()
        )
        self.session.add(new_checksum)
        return new_checksum

    def get_checksum_by_url(self, file_url):
        """
        Retrieve a checksum entry by file URL.
        Parameters:
            file_url (str): URL of the file to retrieve the checksum for.
        Returns:
            DocumentChecksum: The checksum entry if found, None otherwise.
        """
        return self.session.query(DocumentChecksum).filter_by(file_url=file_url).first()

    def update_last_accessed(self, file_url):
        """
        Update the last accessed time for a checksum entry.
        Parameters:
            file_url (str): URL of the file whose last accessed time needs updating.
        Returns:
            DocumentChecksum: The updated checksum entry.
        """
        checksum_entry = self.get_checksum_by_url(file_url)
        if checksum_entry:
            checksum_entry.last_accessed = func.now()
            return checksum_entry
        else:
            raise ValueError("Checksum entry not found for the specified URL")

    def verify_checksum(self, file_url, checksum):
        """
        Verify if the provided checksum matches the stored checksum for a given URL.
        Parameters:
            file_url (str): URL of the file to verify the checksum against.
            checksum (str): The checksum to verify.
        Returns:
            bool: True if the checksum matches, False otherwise.
        """
        checksum_entry = self.get_checksum_by_url(file_url)
        return bool(checksum_entry and checksum_entry.checksum == checksum)

    def update_checksum_by_url(self, file_url, new_checksum):
        """
        Update or create a checksum entry for a given file URL.
        Parameters:
            file_url (str): URL of the file to update or create the checksum entry for.
            new_checksum (str): The new checksum to be stored.
        Returns:
            DocumentChecksum: The updated or newly created checksum entry.
        """
        checksum_entry = self.get_checksum_by_url(file_url)
        if checksum_entry:
            # Update existing checksum and last accessed time
            checksum_entry.checksum = new_checksum
            checksum_entry.last_accessed = func.now()
            return checksum_entry
        else:
            # Create new checksum entry if it does not exist
            return self.add_checksum(file_url, new_checksum)
