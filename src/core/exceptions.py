from typing import Callable
from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, message: str = "Resource Not Found.") -> None:
        self.message: str = message
        super().__init__(self.message)


class InternalInvariantError(Exception):
    """Raised when the backend hits an unexpected
    state that shouldn't happen in production."""

    def __init__(self, message="An internal error occurred.") -> None:
        super().__init__(message)


# * I didn't want to put the registratio code in the main.py
# * file so I just used this function to accept app.
def register_global_exceptions(app: Callable) -> None:
    """
    A wrapper function to register Global exceptions.
    """

    @app.exception_handler(NotFoundException)
    def not_found_exception_handler(
        request: Request, exc: NotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message}
        )

    @app.exception_handler(InternalInvariantError)
    def internal_invariant_exception_handler(
        request: Request, exc: InternalInvariantError
    ) -> JSONResponse:
        # TODO: To see the technical related error, you should do that
        # TODO: in logger since internal errors are our mistakes.

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."}
        )
