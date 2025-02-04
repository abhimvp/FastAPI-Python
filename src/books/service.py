from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book


class BookService:
    # session object allows us to interact with the database   - to create a statement to read our books
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        book_data_dictionary = book_data.model_dump()
        new_book = Book(**book_data_dictionary)  # unpacking the dictionary
        new_book.published_date = datetime.strptime(
            book_data_dictionary["published_date"], "%Y-%m-%d"
        )
        new_book.user_uid = user_uid
        session.add(new_book)  # adds this data to session
        await session.commit()  # then commit the current transaction
        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is not None:
            update_data_dictionary = (
                update_data.model_dump()
            )  # exclude_unset=True - this will only update the fields that are present in the update_data dictionary
            for key, value in update_data_dictionary.items():
                setattr(book_to_update, key, value)
            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return None
