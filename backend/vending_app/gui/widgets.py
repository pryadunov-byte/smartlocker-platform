from __future__ import annotations

import math
from typing import Optional

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class SectorMap(QWidget):
    def __init__(self, sectors: int = 32, parent: QWidget | None = None):
        super().__init__(parent)
        self.sectors = sectors
        self.current_sector: Optional[int] = None
        self.setMinimumSize(280, 280)
        self._bg_color = QColor(25, 25, 35)
        self._active_color = QColor(0, 170, 255)
        self._idle_color = QColor(80, 80, 100)

    def set_sector(self, sector: Optional[int]) -> None:
        self.current_sector = sector
        self.update()

    def paintEvent(self, event):  # noqa: D401
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(10, 10, min(self.width(), self.height()) - 20, min(self.width(), self.height()) - 20)
        painter.fillRect(self.rect(), self._bg_color)
        painter.setPen(QPen(QColor(120, 120, 150), 2))
        painter.drawEllipse(rect)
        center = rect.center()
        radius = rect.width() / 2
        angle_step = 360 / self.sectors
        for sector in range(self.sectors):
            start_angle = math.radians(angle_step * sector)
            end_angle = math.radians(angle_step * (sector + 1))
            color = self._active_color if sector == self.current_sector else self._idle_color
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            path = self._sector_path(center, radius, start_angle, end_angle)
            painter.drawPath(path)
        painter.setPen(QPen(QColor(200, 200, 220), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(rect.adjusted(20, 20, -20, -20))

    def _sector_path(self, center: QPointF, radius: float, start_angle: float, end_angle: float):
        from PySide6.QtGui import QPainterPath

        path = QPainterPath()
        path.moveTo(center)
        path.arcTo(QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2), -math.degrees(start_angle), -math.degrees(end_angle - start_angle))
        path.closeSubpath()
        return path
