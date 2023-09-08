import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation

class UncoverTransitionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set widget attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(QRect(50, 50, 100, 350))  # Adjust the size and position as needed

        # Create a vertical layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Create a label with an image (adjust the icon path as needed)
        icon_label = QLabel(self)
        icon = QIcon("icon.png")  # Replace with the path to your icon image
        pixmap = icon.pixmap(64, 64)  # Adjust the size as needed
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        # Apply the layout to the widget
        self.setLayout(layout)

        # Create an animation for the "Uncover" transition effect
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)  # Animation duration in milliseconds (1 second)
        self.animation.setStartValue(QRect(50, 50, 100, 0))  # Initial position and height (hidden)
        self.animation.setEndValue(QRect(50, 50, 100, 350))  # Final position and height (revealed)

        # Initialize widget visibility state
        self.is_visible = False

        # Create a timer to toggle widget visibility
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(1000)  # Toggle visibility every 1000 milliseconds (1 second)

    def toggle_visibility(self):
        if not self.is_visible:
            self.animation.start()
            self.is_visible = True

def main():
    app = QApplication(sys.argv)
    widget = UncoverTransitionWidget()

    # Move the widget to the desired position on the desktop
    widget.move(50, 50)  # Adjust the position as needed

    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
