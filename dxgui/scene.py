from PyQt6.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QSpacerItem,
                             QSizePolicy,
                             QGridLayout,
                             QVBoxLayout)

from .spacers import VSpacer

class Scene(QWidget):
    def __init__(self, 
                 scene_id,
                 scene_name:str='Scene',
                 button_dict:dict=None, 
                 col_count:int=3):
        super().__init__()
        self.scene_id = scene_id
        self.setProperty('class', 'scene')
        self.setObjectName(f'{scene_id}-scene')

        self.banner = QLabel(scene_name)
        self.banner.setProperty('class', 'header')
        self.banner.setObjectName(f'{scene_id}-header') 

        self.stage = QWidget()
        self.stage.setProperty('class', 'stage')
        self.stage_layout = QGridLayout()
        self.stage_layout.setProperty('class', 'stage-layout')
        self.stage.setLayout(self.stage_layout)

        if button_dict:
            for i, (btn_name, btn_action) in enumerate(button_dict.items()):
                btn = QPushButton(btn_name)
                btn.setProperty('class', 'scene-button')
                if btn_action:
                    btn.clicked.connect(btn_action)
                else:
                    btn.setEnabled(False)
                row = i // col_count
                col = i % col_count 
                self.stage_layout.addWidget(btn, row, col)

        self.scene_layout = QVBoxLayout()
        self.scene_layout.setProperty('class', 'scene-layout')
        self.scene_layout.addWidget(self.banner)
        self.scene_layout.addWidget(self.stage)
        self.scene_layout.addSpacerItem(VSpacer())

        self.setLayout(self.scene_layout)


    def setSpacing(self, spacing):
        self.stage_layout.setSpacing(spacing)

    def setMargins(self, left, top, right, bottom):
        self.stage_layout.setContentsMargins(left, top, right, bottom)