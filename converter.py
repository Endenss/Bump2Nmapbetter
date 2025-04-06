import os
import numpy as np
import imageio.v2 as imageio
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QListWidget, QLineEdit,
                             QMessageBox, QProgressBar, QCheckBox, QGroupBox, QRadioButton,
                             QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color = QColor("#3498db")
        self._default_color = QColor("#3498db")
        self._hover_color = QColor("#2980b9")
        self._pressed_color = QColor("#1a5276")
        
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()
        
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(300)
    
    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color.name()};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
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

    def _animate_color(self, target_color, duration=300):
        self._animation.stop()
        self._animation.setDuration(duration)
        self._animation.setEndValue(target_color)
        self._animation.start()


class DDSConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер DDS текстур")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon("icon.png"))
        
        self._setup_ui()
        self._setup_style()
        self.show()
    
    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("Bump2Nmap but better")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #3498db; margin-bottom: 15px;")
        layout.addWidget(title)

        # Режимы работы
        self.mode_group = QGroupBox("Режим работы:")
        mode_layout = QHBoxLayout()
        
        self.mode_convert = QRadioButton("Конвертация каналов")
        self.mode_alpha = QRadioButton("Извлечение альфа-канала")
        self.mode_global = QRadioButton("Глобальная обработка")
        self.mode_global.setChecked(True)
        
        mode_layout.addWidget(self.mode_convert)
        mode_layout.addWidget(self.mode_alpha)
        mode_layout.addWidget(self.mode_global)
        self.mode_group.setLayout(mode_layout)
        layout.addWidget(self.mode_group)

        # Папки
        self._setup_folder_controls(layout)
        
        # Список файлов
        self.file_list_label = QLabel("Найденные файлы:")
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.file_list_label)
        layout.addWidget(self.file_list)

        # Настройки
        self._setup_options(layout)

        # Кнопки
        self._setup_buttons(layout)

        # Связывание событий
        self.mode_convert.toggled.connect(self._toggle_mode)
        self.mode_alpha.toggled.connect(self._toggle_mode)
        self.mode_global.toggled.connect(self._toggle_mode)
    
    def _setup_folder_controls(self, layout):
        # Исходная папка
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

        # Папка назначения
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
        # Настройки конвертации
        self.convert_options = QGroupBox("Настройки конвертации:")
        convert_layout = QVBoxLayout()
        self.process_bump = QCheckBox("Обрабатывать только bump-карты")
        self.process_bump.setChecked(True)
        self.create_spec = QCheckBox("Создавать specular-карты")
        self.create_spec.setChecked(True)
        self.convert_to_png = QCheckBox("Конвертировать в PNG")
        self.convert_to_png.setChecked(True)
        convert_layout.addWidget(self.process_bump)
        convert_layout.addWidget(self.create_spec)
        convert_layout.addWidget(self.convert_to_png)
        self.convert_options.setLayout(convert_layout)
        self.convert_options.setVisible(False)
        layout.addWidget(self.convert_options)

        # Настройки альфа-канала
        self.alpha_options = QGroupBox("Настройки альфа-канала:")
        alpha_layout = QVBoxLayout()
        self.process_alpha = QCheckBox("Обрабатывать bump#.dds")
        self.process_alpha.setChecked(True)
        self.delete_original = QCheckBox("Удалять исходные файлы")
        self.alpha_convert_to_png = QCheckBox("Конвертировать в PNG")
        self.alpha_convert_to_png.setChecked(True)
        alpha_layout.addWidget(self.process_alpha)
        alpha_layout.addWidget(self.delete_original)
        alpha_layout.addWidget(self.alpha_convert_to_png)
        self.alpha_options.setLayout(alpha_layout)
        self.alpha_options.setVisible(False)
        layout.addWidget(self.alpha_options)

        # Глобальные настройки
        self.global_options = QGroupBox("Глобальные настройки:")
        global_layout = QVBoxLayout()
        self.convert_colormap = QCheckBox("Конвертировать colormap")
        self.convert_colormap.setChecked(True)
        self.convert_bump = QCheckBox("Конвертировать bump")
        self.convert_bump.setChecked(True)
        self.extract_roughness = QCheckBox("Извлекать roughness")
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
        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Кнопки действий
        button_layout = QHBoxLayout()
        self.refresh_button = AnimatedButton("Обновить список")
        self.refresh_button.clicked.connect(self._refresh_file_list)
        self.convert_button = AnimatedButton("Конвертировать")
        self.convert_button.clicked.connect(self._process_files)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)
    
    def _setup_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QGroupBox {
                color: #ecf0f1;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 3px;
                padding: 5px;
            }
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 3px;
            }
            QProgressBar {
                border: 1px solid #3498db;
                border-radius: 3px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
            QCheckBox, QRadioButton {
                color: #ecf0f1;
                spacing: 5px;
            }
        """)
    
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
            files = [f for f in os.listdir(source_folder) if f.lower().endswith('.dds')]
        elif self.mode_convert.isChecked():
            if self.process_bump.isChecked():
                files = [f for f in os.listdir(source_folder) if f.lower().endswith("bump.dds")]
            else:
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(".dds")]
        else:
            if self.process_alpha.isChecked():
                files = [f for f in os.listdir(source_folder) if f.lower().endswith("bump#.dds")]
            else:
                files = [f for f in os.listdir(source_folder) if f.lower().endswith(".dds")]
        
        self.file_list.addItems(sorted(files))
    
    def _get_output_extension(self, mode):
        if mode == "convert" and not self.convert_to_png.isChecked():
            return ".dds"
        if mode == "alpha" and not self.alpha_convert_to_png.isChecked():
            return ".dds"
        return ".png"
    
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
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            files_to_process = [f for f in os.listdir(source_folder) if f.lower().endswith('.dds')]
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
                        alpha_channel = img[:, :, 3]
                        output_path = os.path.join(output_folder, f"{base_name.replace('bump#', 'roughness')}.png")
                        imageio.imsave(output_path, alpha_channel)
                        
                    elif "bump" in file_name.lower() and self.convert_bump.isChecked():
                        new_img = np.empty(img.shape, dtype=np.uint8)
                        new_img[:,:,0] = img[:,:,3]
                        new_img[:,:,1] = img[:,:,2]
                        new_img[:,:,2] = img[:,:,1]
                        output_path = os.path.join(output_folder, f"{base_name}.png")
                        imageio.imsave(output_path, new_img)
                    
                    if not self.keep_originals.isChecked():
                        os.remove(input_path)
                        
                elif self.mode_convert.isChecked():
                    img = imageio.imread(input_path)
                    new_img = np.empty(img.shape, dtype=np.uint8)
                    new_img[:,:,0] = img[:,:,3]
                    new_img[:,:,1] = img[:,:,2]
                    new_img[:,:,2] = img[:,:,1]
                    
                    ext = self._get_output_extension("convert")
                    output_path = os.path.join(output_folder, f"{base_name}{ext}")
                    imageio.imsave(output_path, new_img)
                    
                    if self.create_spec.isChecked():
                        red_channel = img[:, :, 0]
                        spec_path = os.path.join(output_folder, f"{base_name}_spec{ext}")
                        imageio.imsave(spec_path, red_channel)
                        
                else:
                    img = imageio.imread(input_path)
                    alpha_channel = img[:, :, 3]
                    
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


if __name__ == "__main__":
    app = QApplication([])
    
    # Настройка палитры для темной темы
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(44, 62, 80))
    palette.setColor(QPalette.WindowText, QColor(236, 240, 241))
    palette.setColor(QPalette.Base, QColor(52, 73, 94))
    palette.setColor(QPalette.AlternateBase, QColor(44, 62, 80))
    palette.setColor(QPalette.ToolTipBase, QColor(236, 240, 241))
    palette.setColor(QPalette.ToolTipText, QColor(236, 240, 241))
    palette.setColor(QPalette.Text, QColor(236, 240, 241))
    palette.setColor(QPalette.Button, QColor(52, 152, 219))
    palette.setColor(QPalette.ButtonText, QColor(236, 240, 241))
    palette.setColor(QPalette.BrightText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor(41, 128, 185))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = DDSConverterApp()
    app.exec_()