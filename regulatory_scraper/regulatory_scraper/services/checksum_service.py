from sqlalchemy.orm import Session
from regulatory_scraper.database.models import DocumentChecksum
from sqlalchemy.sql import func

class ChecksumService:
    def add_checksum(self, session: Session, file_url, checksum):
        """
        Add a new checksum entry to the database.
        Parameters:
            file_url (str): URL of the file to which the checksum corresponds.
            checksum (str): The checksum value for the file.
        Returns:
            DocumentChecksum: The newly created checksum entry.
        """
        if self.get_checksum_by_url(session, file_url):
            raise ValueError("A checksum entry already exists for this URL.")
        new_checksum = DocumentChecksum(
            file_url=file_url,
            checksum=checksum,
            last_accessed=func.now()
        )
        session.add(new_checksum)
        return new_checksum

    def get_checksum_by_url(self, session: Session, file_url):
        """
        Retrieve a checksum entry by file URL.
        Parameters:
            file_url (str): URL of the file to retrieve the checksum for.
        Returns:
            DocumentChecksum: The checksum entry if found, None otherwise.
        """
        checksum_entry = session.query(DocumentChecksum).filter_by(file_url=file_url).first()
        if checksum_entry:
            checksum_entry.last_accessed = func.now()

        return checksum_entry

    def update_last_accessed(self, session: Session, file_url):
        """
        Update the last accessed time for a checksum entry.
        Parameters:
            file_url (str): URL of the file whose last accessed time needs updating.
        Returns:
            DocumentChecksum: The updated checksum entry.
        """
        checksum_entry = self.get_checksum_by_url(session,file_url)
        if checksum_entry:
            checksum_entry.last_accessed = func.now()
            return checksum_entry
        else:
            raise ValueError("Checksum entry not found for the specified URL")

    def verify_checksum(self, session: Session, file_url, checksum):
        """
        Verify if the provided checksum matches the stored checksum for a given URL and check if an entry exists.
        Parameters:
            file_url (str): URL of the file to verify the checksum against.
            checksum (str): The checksum to verify.
        Returns:
            tuple(bool, bool): 
                First bool is True if the checksum matches, False otherwise.
                Second bool is True if a checksum entry exists for the URL, False otherwise.
        """
        checksum_entry = self.get_checksum_by_url(session, file_url)
        if checksum_entry:
            # Check if the checksums match
            is_match = checksum_entry.checksum == checksum
        else:
            # No checksum entry found, so no match is possible
            is_match = False

        # The presence of a checksum entry is determined by whether checksum_entry is not None
        entry_exists = bool(checksum_entry)
        
        return is_match, entry_exists

    def update_checksum_by_url(self, session: Session, file_url, new_checksum):
        """
        Update or create a checksum entry for a given file URL.
        Parameters:
            file_url (str): URL of the file to update or create the checksum entry for.
            new_checksum (str): The new checksum to be stored.
        Returns:
            DocumentChecksum: The updated or newly created checksum entry.
        """
        checksum_entry = self.get_checksum_by_url(session,file_url)
        if checksum_entry:
            # Update existing checksum and last accessed time
            checksum_entry.checksum = new_checksum
            checksum_entry.last_accessed = func.now()
            return checksum_entry
        else:
            # Create new checksum entry if it does not exist
            return self.add_checksum(session, file_url, new_checksum)
