from enum import Enum

class Status(Enum):
    Closed = 0      # False == 0
    Open = 1        # True == 1
    Concur = 2
    For_Information_Only = 3
    Non_Concur = 4
    Check_And_Resolve = 5
    # Shorthands:
    FIO = For_Information_Only
    NC = Non_Concur
    CNR = Check_And_Resolve

class Classification(Enum):
    Public = 1
    Unclassified = 2
    CUI = 3

class Sensitive(Enum):
    No = 0
    Yes = 1