
# from src.payment.repositories import TransactionRepository
# from src.payment.schemas import (
#     TransactionResponseSchema
# )

# class PaymentService:
#     @staticmethod
#     def get_transactions(
#         db: DbSession,
#     ) -> list[TransactionResponseSchema]:
#         transactions = TransactionRepository.get_all_transactions(db)

#         # TODO: Consider this might be an overhead for large transaction records
#         return [TransactionResponseSchema.model_validate(trans) for trans in transactions]
