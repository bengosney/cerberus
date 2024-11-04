from rest_framework import status
from rest_framework.exceptions import APIException


class BookingSlotError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class IncorectServiceError(BookingSlotError):
    def __init__(self):
        super().__init__("Booking is for a different service")


class DiffrentCustomerError(BookingSlotError):
    def __init__(self):
        super().__init__("Booking must be for the same customer")


class MaxCustomersError(BookingSlotError):
    def __init__(self, max_customers: int):
        super().__init__(f"Booking has max customers for service, {max_customers}")


class MaxPetsError(BookingSlotError):
    def __init__(self, max_pets: int):
        super().__init__(f"Booking has max pets for service, {max_pets}")


class SlotOverlapsError(BookingSlotError):
    def __init__(self):
        super().__init__("Slot overlaps another")


class InvalidEmailError(Exception):
    def __init__(self) -> None:
        super().__init__("Can only set email as invoice email")


class ChargeRefundError(Exception):
    pass


class ChargeAllreadyRefundedError(ChargeRefundError):
    def __init__(self):
        super().__init__("Charge has already been refunded")


class RefundAmountExceedsError(ChargeRefundError):
    def __init__(self):
        super().__init__("Refund amount exceeds the refundable amount")
