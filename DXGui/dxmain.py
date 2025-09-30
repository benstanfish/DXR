import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow, 
                             QWidget,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QToolButton)
from PyQt6.QtCore import (Qt, QSize, QEvent)
from PyQt6.QtGui import QIcon


stop_0 = "#406175"
stop_1 = "#5f2157"

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            """
            QLabel { text-transform: uppercase; font-size: 10pt; margin-left: 48px; }
            """
        )

        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)


        # Min button
        self.min_button = QToolButton(self)
        min_icon = QIcon()
        min_icon.addFile("./dxgui/min.svg")
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = QIcon()
        max_icon.addFile("./dxgui/max.svg")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = QIcon()
        close_icon.addFile("./dxgui/close.svg")  # Close has only a single state.
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = QIcon()
        normal_icon.addFile("./dxgui/normal.svg")
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(16, 16))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)


class DXRMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DXR v1.0")
        self.resize(600, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        central_widget = QWidget()

        central_widget.setObjectName("Container")
        central_widget.setStyleSheet(
            r"#Container {background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 "
              + stop_0 + " stop:1 " + stop_1 + "); border-radius: 5px;}"
        )
        self.title_bar = CustomTitleBar(self)

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(11, 11, 11, 11)

        open_files_button = QPushButton('Create from XML', self)
        open_files_button.setObjectName('OpenFileButton')
        open_files_button.setStyleSheet(
            """
            #OpenFileButton {background: transparent; border: 1px solid white; border-radius: 6px; padding: 6px}
            #OpenFileButton::hover {background: #333;}
            """)
        open_files_button.clicked.connect(self.on_open_files_button_clicked)

        work_space_layout.addWidget(QLabel("Select a Tool:", self))
        work_space_layout.addWidget(open_files_button)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)


    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
        self.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def on_open_files_button_clicked(self, event):
        print('Button Clicked!')



if __name__ == "__main__":
    app = QApplication([])
    window = DXRMainWindow()
    window.show()
    sys.exit(app.exec())

