from sqlalchemy.orm import Session
from regulatory_scraper.database.models import Category
import uuid
from sqlalchemy.sql import func

class CategoryService:
    def get_category(self, session: Session, name):
        """
        Retrieve a category from the database by its name.
        Parameters:
            name (str): The name of the category to find.
        Returns:
            Category: The Category object if found, None otherwise.
        """
        return session.query(Category).filter_by(name=name).first()

    def create_category(self, session: Session, name, description=None):
        """
        Create and add a new category to the database. This method does not commit the change.
        Parameters:
            name (str): The name of the new category.
            description (str, optional): A description for the new category.
        Returns:
            Category: The newly created Category object.
        """
        if self.get_category(session,name):
            raise ValueError("A category with the given name already exists.")
        new_category = Category(
            name=name,
            description=description
        )
        session.add(new_category)
        return new_category

    def get_or_create_category(self, session: Session, name, description=None):
        """
        Retrieve a category from the database by name, or create a new one if it does not exist.
        Parameters:
            name (str): The name of the category to retrieve or create.
            description (str, optional): A description for the category if it needs to be created.
        Returns:
            Category: The existing or newly created Category object.
        """
        category = self.get_category(session,name)
        if category:
            return category
        else:
            return self.create_category(session, name, description)
