from enum import Enum


class ResultCodes(Enum):
    SUCCESS: str = "00000"
    SUCCESS_GATEWAY: str = "00"
    SUCCESS_GATEWAY_APPROVE: str = "APPROVED"
    SUCCESS_GATEWAY_PREAUTH_APPROVE: str = "PREAUTH-APPROVED"
    WARNING: str = "01000"
    ERROR: str = "15000"
    INVALID_PARAMETERS: str = "15400"
    UNAUTHORIZED: str = "14010"
    TOKEN_NOT_PRESENT: str = "14013"
    INVALID_TOKEN: str = "14014"
