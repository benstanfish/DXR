light_theme = """

QPushButton {
    font-weight: bold;
    color: white;
    padding: 12px;
    border-radius: 16px;

    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 orangered,
        stop: 1 magenta
    );
}

QPushButton:hover {
    background: mediumseagreen;
}

QPushButton:disabled {
    background: #aaa;
}

#exit_button {
    margin: 10px;
}

.scene-button {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 mediumseagreen,
        stop: 1 dodgerblue
    );
}

.scene-button:hover {
    background: tomato;
}

.central-widget {
    background: transparent;
    border-radius: 6px;
}   

.left-panel {
    background: #ccc;
    border: none;
    border-radius: 12px;
}

.right-panel {
    background: #aaa;
    border: none;
    border-radius: 12px;
}

.left-panel-header,
.right-panel-header,
.scene-header {
    border-bottom: none;
    border-radius: 12px;
    padding: 4px;
}

.left-panel-header {
    background: #ccc;
}

.scene-header {
    background: #ddd;
}

.right-panel-header {
    background: #aaa;
}

.scene {
    background: #bbb;

    border-radius: 12px;
}

.header {
    font-size: 14px;
    font-weight: bold;
}

.section-header {
    font-weight: bold;
}

"""