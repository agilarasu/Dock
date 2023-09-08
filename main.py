import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QFont, QCursor
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QUrl
from PyQt5.QtGui import QDesktopServices  # Use QDesktopServices from QtGui

class FloatingWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        # Set widget attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(QRect(50, 50, 100, 350))  # Adjust the size to fit 5 icons as a column

        # Create a vertical layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Create icon labels based on the configuration
        for label_name, label_info in config.items():
            icon_label = QLabel(self)
            icon_path = label_info["icon"]
            icon = QIcon(icon_path)
            pixmap = icon.pixmap(64, 64)  # Adjust the size as needed
            icon_label.setPixmap(pixmap)

            # Determine the action type and action function based on the config
            action_type = label_info["type"]
            if action_type == "execute_system_code":
                action = lambda exex=label_info["exex"]: self.execute_system_code(exex)
            elif action_type == "open_url":
                action = lambda url=label_info["url"]: self.open_website(url)
            else:
                action = lambda: None  # Default action if type is not recognized

            # Connect the icon label to the corresponding action
            icon_label.mousePressEvent = lambda event, action=action: self.on_icon_click(event, action)
            layout.addWidget(icon_label)

        # Apply the layout to the widget
        self.setLayout(layout)

        # Create a timer to toggle widget visibility on hover
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(100)  # Check hover every 100 milliseconds

        # Initialize widget visibility state
        self.is_visible = False

        # Create animations for transition effect
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)  # Adjust the duration as needed
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)

        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(300)  # Adjust the duration as needed
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.hide)

    def toggle_visibility(self):
        # Get the cursor position relative to the widget
        cursor_pos = self.mapFromGlobal(QCursor.pos())

        # Check if the cursor is over the widget
        if self.rect().contains(cursor_pos):
            if not self.is_visible:
                self.fade_in_animation.start()
                self.show()
                self.is_visible = True
        else:
            if self.is_visible:
                self.fade_out_animation.start()
                self.is_visible = False

    def on_icon_click(self, event, action):
        if event.button() == Qt.LeftButton:
            action()

    def execute_system_code(self, code):
        # Example: Open applications like Calculator or Notepad
        try:
            import subprocess
            subprocess.Popen(code)
        except Exception as e:
            print(f"Error executing code: {e}")

    def open_website(self, url):
        # Example: Open a website in the default web browser
        try:
            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            print(f"Error opening website: {e}")

def main():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    app = QApplication(sys.argv)
    widget = FloatingWidget(config)

    # Move the widget to the left-center side of the desktop
    desktop_geometry = app.desktop().availableGeometry()
    widget.move(desktop_geometry.left(), desktop_geometry.center().y() - widget.height() // 2)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
