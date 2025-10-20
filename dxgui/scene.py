from PyQt6.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QSpacerItem,
                             QSizePolicy,
                             QGridLayout,
                             QVBoxLayout)

DEFAULT_SPACING = 16
DEFAULT_MARGIN = 16

class Scene(QWidget):
    def __init__(self, 
                 scene_name:str="Scene",
                 scene_id=None, 
                 button_dict:dict=None, 
                 col_count:int=3):
        super().__init__()
        self.setProperty("class", "scene")
        self.scene_id = scene_id
        if scene_id:
            self.setObjectName(self.scene_id)

        self.scene_title = QLabel(scene_name)
        self.scene_title.setProperty("class", "scene-title") 

        self.scene_grid = QGridLayout()
        self.scene_grid.setProperty("class", "scene-grid")
        self.scene_grid.setSpacing(DEFAULT_SPACING)

        if button_dict:
            for i, (btn_name, btn_action) in enumerate(button_dict.items()):
                btn = QPushButton(btn_name)
                btn.setProperty("class", "scene-button")
                btn.clicked.connect(btn_action)
                row = i // col_count
                col = i % col_count 
                self.scene_grid.addWidget(btn, row, col)

        self.scene_container = QVBoxLayout()
        self.scene_container.setProperty("class", "scene-container")

        self.scene_container.addWidget(self.scene_title)
        self.scene_container.addLayout(self.scene_grid)
        self.scene_container.setContentsMargins(DEFAULT_MARGIN, DEFAULT_MARGIN, DEFAULT_MARGIN, DEFAULT_MARGIN)

        self.stage_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.scene_container.addSpacerItem(self.stage_spacer)

        self.setLayout(self.scene_container)