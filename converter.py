import os
import numpy as np
import imageio.v2 as imageio
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QListWidget, QLineEdit,
                             QMessageBox, QProgressBar, QCheckBox, QGroupBox, QRadioButton,
                             QFrame, QTabWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QUrl, QSize
from PyQt6.QtGui import QColor, QPalette, QFont, QIcon, QPixmap, QDesktopServices


class StalkerStyle:
    @staticmethod
    def get_dark_palette():
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 200, 200))
        palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(200, 200, 200))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
        palette.setColor(QPalette.ColorRole.Button, QColor(70, 70, 70))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 200, 200))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 120, 50))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        return palette

    @staticmethod
    def get_stylesheet():
        return """
            QMainWindow {
                background-color: #1e1e1e;
                border: 1px solid #3a3a3a;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                border-radius: 2px;
                margin-top: 5px;
                background: #262626;
            }
            QTabBar::tab {
                background: #262626;
                color: #c8c8c8;
                padding: 8px;
                border: 1px solid #3a3a3a;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #323232;
                color: #e0e0e0;
                border-color: #646464;
            }
            QTabBar::tab:hover {
                background: #323232;
            }
            QGroupBox {
                color: #a0a0a0;
                font-weight: bold;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                margin-top: 10px;
                padding-top: 15px;
                background: #262626;
            }
            QLabel {
                color: #c8c8c8;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #c8c8c8;
                border: 1px solid #3a3a3a;
                border-radius: 2px;
                padding: 5px;
                selection-background-color: #646464;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #c8c8c8;
                border: 1px solid #3a3a3a;
                border-radius: 2px;
                selection-background-color: #646464;
            }
            QProgressBar {
                border: 1px solid #3a3a3a;
                border-radius: 2px;
                text-align: center;
                color: #c8c8c8;
                background: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #647833;
            }
            QCheckBox, QRadioButton {
                color: #c8c8c8;
                spacing: 5px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #3a3a3a;
                background: #2a2a2a;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background: #647833;
                border: 1px solid #7a8c43;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #c8c8c8;
                border: 1px solid #4a4a4a;
                border-radius: 2px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #6a6a6a;
            }
            #githubButton {
                border: none;
                background: transparent;
            }
            #githubButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color = QColor("#3a3a3a")
        self._default_color = QColor("#3a3a3a")
        self._hover_color = QColor("#4a4a4a")
        self._pressed_color = QColor("#2a2a2a")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color.name()};
                color: #c8c8c8;
                border: 1px solid #4a4a4a;
                border-radius: 2px;
                padding: 5px 10px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
                border-color: #5a5a5a;
            }}
            QPushButton:pressed {{
                background-color: {self._pressed_color.name()};
            }}
        """)
    
    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._update_style()

    def enterEvent(self, event):
        self._animate_color(self._hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_color(self._default_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._animate_color(self._pressed_color, 100)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._animate_color(self._hover_color if self.underMouse() else self._default_color)
        super().mouseReleaseEvent(event)

    def _animate_color(self, target_color, duration=200):
        self._animation.stop()
        self._animation.setDuration(duration)
        self._animation.setEndValue(target_color)
        self._animation.start()


class FileProcessingTab(QWidget):
    def __init__(self, file_extension, parent=None):
        super().__init__(parent)
        self.file_extension = file_extension
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        self.mode_group = QGroupBox("Режим работы:")
        mode_layout = QHBoxLayout()
        self.mode_convert = QRadioButton("Конвертация bump в normal")
        self.mode_alpha = QRadioButton("Извлечение roughness")
        self.mode_global = QRadioButton("Глобальная обработка")
        self.mode_global.setChecked(True)
        mode_layout.addWidget(self.mode_convert)
        mode_layout.addWidget(self.mode_alpha)
        mode_layout.addWidget(self.mode_global)
        self.mode_group.setLayout(mode_layout)
        layout.addWidget(self.mode_group)
        self._setup_folder_controls(layout)
        self.file_list_label = QLabel(f"Найденные файлы (.{self.file_extension}):")
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.file_list_label)
        layout.addWidget(self.file_list)
        self._setup_options(layout)
        self._setup_buttons(layout)
        self.mode_convert.toggled.connect(self._toggle_mode)
        self.mode_alpha.toggled.connect(self._toggle_mode)
        self.mode_global.toggled.connect(self._toggle_mode)
    
    def _setup_folder_controls(self, layout):
        source_layout = QHBoxLayout()
        self.source_label = QLabel("Исходная папка:")
        self.source_path = QLineEdit()
        self.source_path.setReadOnly(True)
        self.browse_source = AnimatedButton("Обзор...")
        self.browse_source.clicked.connect(self._select_source_folder)
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_path)
        source_layout.addWidget(self.browse_source)
        layout.addLayout(source_layout)
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Папка назначения:")
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        self.browse_output = AnimatedButton("Обзор...")
        self.browse_output.clicked.connect(self._select_output_folder)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.browse_output)
        layout.addLayout(output_layout)
    
    def _setup_options(self, layout):
        self.convert_options = QGroupBox("Настройки конвертации:")
        convert_layout = QVBoxLayout()
        self.process_bump = QCheckBox(f"Обрабатывать только *_bump.{self.file_extension}")
        self.process_bump.setChecked(True)
        self.create_spec = QCheckBox("Создавать specular карты")
        self.create_spec.setChecked(True)
        self.convert_to_png = QCheckBox("Конвертировать в PNG" if self.file_extension == "dds" else "Конвертировать в DDS")
        convert_layout.addWidget(self.process_bump)
        convert_layout.addWidget(self.create_spec)
        convert_layout.addWidget(self.convert_to_png)
        self.convert_options.setLayout(convert_layout)
        self.convert_options.setVisible(False)
        layout.addWidget(self.convert_options)
        self.alpha_options = QGroupBox("Настройки roughness:")
        alpha_layout = QVBoxLayout()
        self.process_alpha = QCheckBox(f"Обрабатывать *bump#.{self.file_extension}")
        self.process_alpha.setChecked(True)
        self.delete_original = QCheckBox("Удалять исходные файлы")
        self.alpha_convert_to_png = QCheckBox("Конвертировать в PNG" if self.file_extension == "dds" else "Конвертировать в DDS")
        alpha_layout.addWidget(self.process_alpha)
        alpha_layout.addWidget(self.delete_original)
        alpha_layout.addWidget(self.alpha_convert_to_png)
        self.alpha_options.setLayout(alpha_layout)
        self.alpha_options.setVisible(False)
        layout.addWidget(self.alpha_options)
        self.global_options = QGroupBox("Глобальные настройки:")
        global_layout = QVBoxLayout()
        self.convert_colormap = QCheckBox(f"Конвертировать *_colormap.{self.file_extension}")
        self.convert_colormap.setChecked(True)
        self.convert_bump = QCheckBox(f"Конвертировать *_bump.{self.file_extension}")
        self.convert_bump.setChecked(True)
        self.extract_roughness = QCheckBox(f"Извлекать roughness из *bump#.{self.file_extension}")
        self.extract_roughness.setChecked(True)
        self.keep_originals = QCheckBox("Сохранять оригиналы")
        self.keep_originals.setChecked(True)
        global_layout.addWidget(self.convert_colormap)
        global_layout.addWidget(self.convert_bump)
        global_layout.addWidget(self.extract_roughness)
        global_layout.addWidget(self.keep_originals)
        self.global_options.setLayout(global_layout)
        layout.addWidget(self.global_options)
    
    def _setup_buttons(self, layout):
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.refresh_button = AnimatedButton("Обновить список")
        self.refresh_button.clicked.connect(self._refresh_file_list)
        self.convert_button = AnimatedButton("Конвертировать")
        self.convert_button.clicked.connect(self._process_files)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)
    
    def _toggle_mode(self):
        self.convert_options.setVisible(self.mode_convert.isChecked())
        self.alpha_options.setVisible(self.mode_alpha.isChecked())
        self.global_options.setVisible(self.mode_global.isChecked())
        self._refresh_file_list()
    
    def _select_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите исходную папку")
        if folder:
            self.source_path.setText(folder)
            self._refresh_file_list()
    
    def _select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку назначения")
        if folder:
            self.output_path.setText(folder)
    
    def _refresh_file_list(self):
        self.file_list.clear()
        source_folder = self.source_path.text()
        if not source_folder or not os.path.exists(source_folder):
            return
        if self.mode_global.isChecked():
            files = [f for f in os.listdir(source_folder) if f.lower().endswith(f'.{self.file_extension}')]
        elif self.mode_convert.isChecked():
            if self.process_bump.isChecked():
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(f"_bump.{self.file_extension}")]
            else:
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(f".{self.file_extension}")]
        else:
            if self.process_alpha.isChecked():
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(f"bump#.{self.file_extension}")]
            else:
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(f".{self.file_extension}")]
        self.file_list.addItems(sorted(files))
    
    def _get_output_extension(self, mode):
        if mode == "convert" and not self.convert_to_png.isChecked():
            return f".{self.file_extension}"
        if mode == "alpha" and not self.alpha_convert_to_png.isChecked():
            return f".{self.file_extension}"
        return ".png" if self.file_extension == "dds" else ".dds"
    
    def convert_bump_to_normal(self, img):
        new_img = np.zeros_like(img)
        if img.shape[2] == 4:
            new_img[:,:,0] = img[:,:,3]
            new_img[:,:,3] = 255
        else:
            new_img[:,:,0] = 128
        new_img[:,:,1] = img[:,:,2]
        new_img[:,:,2] = img[:,:,1]
        return new_img
    
    def _process_files(self):
        source_folder = self.source_path.text()
        output_folder = self.output_path.text() or source_folder
        if not source_folder or not os.path.exists(source_folder):
            QMessageBox.warning(self, "Ошибка", "Укажите корректную исходную папку")
            return
        selected_items = self.file_list.selectedItems()
        files_to_process = [item.text() for item in selected_items] if selected_items else None
        if self.mode_global.isChecked() and not files_to_process:
            reply = QMessageBox.question(self, "Подтверждение", 
                                       "Обработать все файлы в папке?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
            files_to_process = [f for f in os.listdir(source_folder) if f.lower().endswith(f'.{self.file_extension}')]
        elif not files_to_process:
            QMessageBox.warning(self, "Ошибка", "Выберите файлы для обработки")
            return
        self.progress.setVisible(True)
        self.progress.setMaximum(len(files_to_process))
        for i, file_name in enumerate(files_to_process):
            self.progress.setValue(i + 1)
            QApplication.processEvents()
            try:
                input_path = os.path.join(source_folder, file_name)
                base_name = os.path.splitext(file_name)[0]
                if self.mode_global.isChecked():
                    img = imageio.imread(input_path)
                    if "colormap" in file_name.lower() and self.convert_colormap.isChecked():
                        output_path = os.path.join(output_folder, f"{base_name}.png")
                        imageio.imsave(output_path, img)
                    elif "bump#" in file_name.lower() and self.extract_roughness.isChecked():
                        alpha_channel = img[:, :, 3] if img.shape[2] >= 4 else img[:, :, 0]
                        output_path = os.path.join(output_folder, f"{base_name.replace('bump#', 'roughness')}.png")
                        imageio.imsave(output_path, alpha_channel)
                    elif "bump" in file_name.lower() and self.convert_bump.isChecked():
                        normal_map = self.convert_bump_to_normal(img)
                        output_path = os.path.join(output_folder, f"{base_name.replace('_bump', '_nmap')}.png")
                        imageio.imsave(output_path, normal_map)
                    if not self.keep_originals.isChecked():
                        os.remove(input_path)
                elif self.mode_convert.isChecked():
                    img = imageio.imread(input_path)
                    normal_map = self.convert_bump_to_normal(img)
                    ext = self._get_output_extension("convert")
                    output_path = os.path.join(output_folder, f"{base_name.replace('_bump', '_nmap')}{ext}")
                    imageio.imsave(output_path, normal_map)
                    if self.create_spec.isChecked():
                        specular = img[:, :, 0]
                        spec_path = os.path.join(output_folder, f"{base_name}_spec{ext}")
                        imageio.imsave(spec_path, specular)
                else:
                    img = imageio.imread(input_path)
                    alpha_channel = img[:, :, 3] if img.shape[2] >= 4 else img[:, :, 0]
                    ext = self._get_output_extension("alpha")
                    output_path = os.path.join(output_folder, f"{base_name.replace('bump#', 'roughness')}{ext}")
                    imageio.imsave(output_path, alpha_channel)
                    if self.delete_original.isChecked():
                        os.remove(input_path)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка обработки {file_name}:\n{str(e)}")
                continue
        self.progress.setVisible(False)
        QMessageBox.information(self, "Готово", "Обработка завершена!")


class StalkerConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S.T.A.L.K.E.R. Texture Converter")
        self.setGeometry(100, 100, 900, 700)
        if os.path.exists("stalker_icon.png"):
            self.setWindowIcon(QIcon("stalker_icon.png"))
        self._setup_ui()
        self._setup_style()
        self.show()
    
    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        header = QHBoxLayout()
        
        if os.path.exists("stalker_logo.png"):
            logo = QLabel()
            logo.setPixmap(QPixmap("stalker_logo.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            header.addWidget(logo)
        else:
            header.addStretch()
        
        title = QLabel("S.T.A.L.K.E.R. TEXTURE CONVERTER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #647833; margin-bottom: 10px;")
        header.addWidget(title)
        
        if not os.path.exists("stalker_logo.png"):
            header.addStretch()

        self.github_btn = QPushButton()
        if os.path.exists("github_icon.png"):
            icon = QIcon("github_icon.png")
            self.github_btn.setIcon(icon)
            self.github_btn.setIconSize(QSize(32, 32))
        else:
            self.github_btn.setText("GitHub")
        self.github_btn.setObjectName("githubButton")
        self.github_btn.setToolTip("Открыть репозиторий на GitHub")
        self.github_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Endenss/TextureConverterPro-TCP")))
        header.addWidget(self.github_btn)
        
        layout.addLayout(header)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #3a3a3a;")
        layout.addWidget(separator)

        self.tabs = QTabWidget()
        self.dds_tab = FileProcessingTab("dds")
        self.tabs.addTab(self.dds_tab, "DDS Processing")
        self.png_tab = FileProcessingTab("png")
        self.tabs.addTab(self.png_tab, "PNG Processing")
        layout.addWidget(self.tabs)
    
    def _setup_style(self):
        app.setPalette(StalkerStyle.get_dark_palette())
        self.setStyleSheet(StalkerStyle.get_stylesheet())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = StalkerConverterApp()
    sys.exit(app.exec())