# from typing import Any

# from sqlalchemy import ScalarResult, select

# from src.core.db import DbSession
# from src.payment.models import Transaction


# class TransactionRepository:
#     """A Repository class for handling Data access and Manipulation logic.
#     It helps to separate Data related logic from the service
#     and also avoids direct interaction to data store.
#     """

#     @staticmethod
#     def create(db: DbSession, serialized_data: dict[str, Any]) -> Transaction:
#         """A method for creating a Transaction instance.

#         Args:
#             db (DbSession): Database session dependancy.
#             serialized_data (dict[str, Any]): a validated payload data.

#         Returns:
#             Transaction: An instance of a transaction
#             which is added to the session but not commited yet.
#         """
#         instance = Transaction(**serialized_data)

#         db.add(instance)

#         return instance

#     @staticmethod
#     def get_all_transactions(
#         db: DbSession,
#     ) -> ScalarResult[Transaction]:
#         # returning the generator as is to benefit from it's laziness
#         # since we're doing looping inside the caller.
#         return db.scalars(
#             select(Transaction)
#         )
