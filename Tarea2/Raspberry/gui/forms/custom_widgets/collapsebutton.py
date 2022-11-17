# solution taken from:
# https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt#answer-68141638


from PyQt5.QtWidgets import QApplication, QToolButton, QWidget
from PyQt5.QtCore import qDebug, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QSize, Qt, QMetaType
import typing


class CollapseButton(QToolButton):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.content_: QWidget = None
        self.animator_ = QParallelAnimationGroup()

        self.setCheckable(True)
        self.setStyleSheet("background:none")
        self.setIconSize(QSize(8,8))
        self.setFont(QApplication.font())

        def _checked_slot(checked: bool):
            self.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
            if self.content_ and self.animator_:
                self.showContent() if checked else self.hideContent()
                
        self.setArrowType(Qt.ArrowType.DownArrow if self.isChecked() else Qt.ArrowType.RightArrow) 
        self.clicked.connect(_checked_slot)

    
    def setText(self, text: QMetaType.Type.QString) -> None:
        super().setText(" " + text)

    def setContent(self, content: QWidget) -> None:
        assert(content != None)
        self.content_ = content
        animation = QPropertyAnimation(self.content_, b"maximumHeight")
        animation.setStartValue(0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.setDuration(300)
        animation.setEndValue(content.geometry().height() + 10)
        self.animator_.addAnimation(animation)
        if not self.isChecked():
            content.setMaximumHeight(0)

    def hideContent(self) -> None:
        self.animator_.setDirection(QAbstractAnimation.Direction.Backward)
        self.animator_.start()

    def showContent(self) -> None:
        self.animator_.setDirection(QAbstractAnimation.Direction.Forward)
        self.animator_.start()
        
