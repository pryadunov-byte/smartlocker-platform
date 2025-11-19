from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)


class IssueDialog(QDialog):
    def __init__(self, mode: str = "issue", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.setWindowTitle("Выдача" if mode == "issue" else "Загрузка")
        self.fio = QLineEdit()
        self.barcode = QLineEdit()
        self.item = QLineEdit()
        self.row = QSpinBox()
        self.row.setRange(1, 15)
        self.sector = QSpinBox()
        self.sector.setRange(0, 31)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("ФИО", self.fio)
        form.addRow("Штрихкод", self.barcode)
        form.addRow("Предмет", self.item)
        if self.mode == "load":
            form.addRow("Ряд", self.row)
            form.addRow("Сектор", self.sector)
        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self._on_accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def _on_accept(self) -> None:
        if not self.fio.text() or not self.barcode.text():
            QMessageBox.warning(self, "Ошибка", "Заполните ФИО и штрихкод")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "fio": self.fio.text(),
            "barcode": self.barcode.text(),
            "item": self.item.text(),
            "row": self.row.value(),
            "sector": self.sector.value(),
        }
