from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class HSpacer(QSpacerItem):
    def __init__(self):
        super().__init__(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

class VSpacer(QSpacerItem):
    def __init__(self):
        super().__init__(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)