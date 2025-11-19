from __future__ import annotations

import datetime as dt
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QColor, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ..db.db_manager import DbManager
from ..services.vending_controller import VendingController
from .issue_dialog import IssueDialog
from .widgets import SectorMap


class MainWindow(QMainWindow):
    def __init__(self, controller: VendingController, db: DbManager):
        super().__init__()
        self.controller = controller
        self.db = db
        self.setWindowTitle("SmartLocker Control Center")
        self.resize(1200, 700)
        self._build_ui()
        self._update_table()
        self._start_status_timer()

    def _build_ui(self) -> None:
        toolbar = QToolBar("MainToolbar")
        issue_action = QAction("Выдать", self)
        issue_action.triggered.connect(self._issue)
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self._load)
        export_action = QAction("Экспорт Excel", self)
        export_action.triggered.connect(self._export_excel)
        export_csv_action = QAction("Экспорт CSV", self)
        export_csv_action.triggered.connect(self._export_csv)
        import_action = QAction("Импорт Excel", self)
        import_action.triggered.connect(self._import_excel)
        import_csv_action = QAction("Импорт CSV", self)
        import_csv_action.triggered.connect(self._import_csv)
        toolbar.addAction(issue_action)
        toolbar.addAction(load_action)
        toolbar.addAction(export_action)
        toolbar.addAction(export_csv_action)
        toolbar.addAction(import_action)
        toolbar.addAction(import_csv_action)
        self.addToolBar(toolbar)

        central = QWidget()
        layout = QHBoxLayout(central)

        left_panel = QVBoxLayout()
        self.map = SectorMap(sectors=self.controller.sectors)
        left_panel.addWidget(self.map)

        control_box = QGroupBox("Управление")
        control_layout = QVBoxLayout(control_box)
        self.btn_open_lock = QPushButton("Открыть замок")
        self.btn_open_lock.clicked.connect(self._open_lock)
        self.btn_rotate = QPushButton("Повернуть сектор")
        self.btn_rotate.clicked.connect(self._rotate_sector)
        control_layout.addWidget(self.btn_open_lock)
        control_layout.addWidget(self.btn_rotate)
        left_panel.addWidget(control_box)

        layout.addLayout(left_panel, 2)

        right_panel = QVBoxLayout()
        status_box = QGroupBox("Статус")
        status_layout = QGridLayout(status_box)
        self.lbl_lock = QLabel("Lock: offline")
        self.lbl_servo = QLabel("Servo: offline")
        self.lbl_angle = QLabel("Angle: 0")
        status_layout.addWidget(self.lbl_lock, 0, 0)
        status_layout.addWidget(self.lbl_servo, 1, 0)
        status_layout.addWidget(self.lbl_angle, 2, 0)
        right_panel.addWidget(status_box)

        self.table = QTableView()
        right_panel.addWidget(self.table, 1)

        layout.addLayout(right_panel, 3)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())

    def _update_table(self) -> None:
        model = self.db.create_model()
        self.table.setModel(model)

    def _start_status_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_status)
        self.timer.start(2000)

    def _update_status(self) -> None:
        status = self.controller.status()
        self.lbl_lock.setText(f"Lock: {'online' if status['lock_connected'] else 'offline'}")
        self.lbl_servo.setText(f"Servo: {'online' if status['servo_connected'] else 'offline'}")
        self.lbl_angle.setText(f"Angle: {status['angle']:.1f}")

    def _issue(self) -> None:
        dialog = IssueDialog("issue", self)
        if dialog.exec() == IssueDialog.Accepted:
            data = dialog.get_data()
            result = self.controller.issue_item(data["fio"], data["barcode"], data["item"])
            self._handle_result(result)

    def _load(self) -> None:
        dialog = IssueDialog("load", self)
        if dialog.exec() == IssueDialog.Accepted:
            data = dialog.get_data()
            result = self.controller.load_item(
                data["fio"], data["barcode"], data["item"], data["row"], data["sector"]
            )
            self._handle_result(result)

    def _handle_result(self, result) -> None:
        if result.success:
            QMessageBox.information(self, "Готово", result.message)
            self.map.set_sector(result.sector)
            self._update_table()
        else:
            QMessageBox.critical(self, "Ошибка", result.message)

    def _open_lock(self) -> None:
        status = self.controller.status()
        if not status["lock_connected"]:
            QMessageBox.warning(self, "Внимание", "Контроллер замков не подключен")
            return
        # open currently highlighted lock (row = 1 default)
        self.controller.lock_driver.unlock(0)
        QMessageBox.information(self, "Замок", "Команда отправлена")

    def _rotate_sector(self) -> None:
        sector = self.map.current_sector or 0
        self.controller.servo_driver.rotate_to_sector(sector)
        self.controller.servo_driver.await_motion_complete()
        self.map.set_sector(sector)

    def _export_excel(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт Excel", str(Path.home() / "transactions.xlsx"), "Excel (*.xlsx)")
        if path:
            self.db.export_excel(Path(path))
            QMessageBox.information(self, "Экспорт", "Файл сохранён")

    def _import_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Импорт Excel", str(Path.home()), "Excel (*.xlsx)")
        if path:
            self.db.import_excel(Path(path))
            self._update_table()
            QMessageBox.information(self, "Импорт", "Импорт завершён")

    def _export_csv(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт CSV", str(Path.home() / "transactions.csv"), "CSV (*.csv)")
        if path:
            self.db.export_csv(Path(path))
            QMessageBox.information(self, "Экспорт", "CSV сохранён")

    def _import_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Импорт CSV", str(Path.home()), "CSV (*.csv)")
        if path:
            self.db.import_csv(Path(path))
            self._update_table()
            QMessageBox.information(self, "Импорт", "CSV импортирован")
