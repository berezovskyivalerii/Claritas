from PySide6.QtWidgets import (QCheckBox, QComboBox, QLineEdit, QWidget, 
                               QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                               QGroupBox, QGridLayout)
from PySide6.QtCore import Qt, Signal
from config.config import BarConfig

class BarSettingsWidget(QWidget):
    request_chart_draw = Signal(str, object)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)
        
        # --- Base Settings ---
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Chart Title...")

        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X Axis Label...")
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y Axis Label...")

        self.color_input = QComboBox()
        self.color_input.addItems(['Blue', 'Red', 'Green', 'Black', 'Yellow', 'Orange'])

        self.is_grid = QCheckBox("Grid")

        # --- NEW: Bar Appearance ---
        self.orientation = QComboBox()
        self.orientation.addItems(['vertical', 'horizontal'])

        self.bar_width = QDoubleSpinBox()
        self.bar_width.setRange(0.1, 2.0)
        self.bar_width.setValue(0.8)
        self.bar_width.setSingleStep(0.1)

        self.edge_color = QComboBox()
        self.edge_color.addItems(['None', 'Black', 'White', 'Blue', 'Red'])

        self.edge_width = QDoubleSpinBox()
        self.edge_width.setRange(0.0, 5.0)
        self.edge_width.setValue(0.0)
        self.edge_width.setSingleStep(0.5)

        self.alpha = QDoubleSpinBox()
        self.alpha.setRange(0.1, 1.0)
        self.alpha.setValue(1.0)
        self.alpha.setSingleStep(0.1)

        # --- NEW: Axis Limits ---
        self.x_min = QLineEdit()
        self.x_min.setPlaceholderText("X Min")
        self.x_max = QLineEdit()
        self.x_max.setPlaceholderText("X Max")
        self.y_min = QLineEdit()
        self.y_min.setPlaceholderText("Y Min")
        self.y_max = QLineEdit()
        self.y_max.setPlaceholderText("Y Max")

        # --- NEW: Log Scale & Tick Rotation ---
        self.log_x = QCheckBox("Log X")
        self.log_y = QCheckBox("Log Y")

        self.tick_rotation = QSpinBox()
        self.tick_rotation.setRange(0, 360)
        self.tick_rotation.setValue(0)

        # --- NEW: Legend ---
        self.show_legend = QCheckBox("Legend")
        self.legend_loc = QComboBox()
        self.legend_loc.addItems(['best', 'upper right', 'upper left', 'lower left', 'lower right'])

        # --- NEW: Fonts ---
        self.title_font_size = QSpinBox()
        self.title_font_size.setRange(8, 32)
        self.title_font_size.setValue(12)

        self.axis_font_size = QSpinBox()
        self.axis_font_size.setRange(8, 32)
        self.axis_font_size.setValue(10)

        # ==========================================
        # --- Layout Assembly (Grouped) ---
        # ==========================================

        # --- Create Group: General ---
        general_group = QGroupBox("General Properties")
        general_layout = QVBoxLayout(general_group)
        general_layout.addWidget(self.title_input)
        
        axis_labels_layout = QHBoxLayout()
        axis_labels_layout.addWidget(self.x_input)
        axis_labels_layout.addWidget(self.y_input)
        general_layout.addLayout(axis_labels_layout)

        fonts_layout = QHBoxLayout()
        fonts_layout.addWidget(QLabel("Title Size:"))
        fonts_layout.addWidget(self.title_font_size)
        fonts_layout.addWidget(QLabel("Axis Size:"))
        fonts_layout.addWidget(self.axis_font_size)
        general_layout.addLayout(fonts_layout)

        # --- Create Group: Bar Appearance ---
        appearance_group = QGroupBox("Bar Appearance")
        appearance_layout = QGridLayout(appearance_group)
        
        appearance_layout.addWidget(QLabel("Color:"), 0, 0)
        appearance_layout.addWidget(self.color_input, 0, 1)
        appearance_layout.addWidget(QLabel("Orient:"), 0, 2)
        appearance_layout.addWidget(self.orientation, 0, 3)
        
        appearance_layout.addWidget(QLabel("Width:"), 1, 0)
        appearance_layout.addWidget(self.bar_width, 1, 1)
        appearance_layout.addWidget(QLabel("Alpha:"), 1, 2)
        appearance_layout.addWidget(self.alpha, 1, 3)

        appearance_layout.addWidget(QLabel("Edge Color:"), 2, 0)
        appearance_layout.addWidget(self.edge_color, 2, 1)
        appearance_layout.addWidget(QLabel("Edge Width:"), 2, 2)
        appearance_layout.addWidget(self.edge_width, 2, 3)

        # --- Create Group: Axes & Limits ---
        axes_group = QGroupBox("Axes & Limits")
        axes_layout = QGridLayout(axes_group)
        
        axes_layout.addWidget(self.x_min, 0, 0)
        axes_layout.addWidget(self.x_max, 0, 1)
        axes_layout.addWidget(self.y_min, 1, 0)
        axes_layout.addWidget(self.y_max, 1, 1)
        
        axes_layout.addWidget(self.log_x, 2, 0)
        axes_layout.addWidget(self.log_y, 2, 1)
        
        axes_layout.addWidget(QLabel("Tick Rotation:"), 3, 0)
        axes_layout.addWidget(self.tick_rotation, 3, 1)
        axes_layout.addWidget(self.is_grid, 4, 0, 1, 2)

        # --- Create Group: Extras ---
        extras_group = QGroupBox("Legend")
        extras_layout = QGridLayout(extras_group)
        
        extras_layout.addWidget(self.show_legend, 0, 0)
        extras_layout.addWidget(QLabel("Pos:"), 0, 1)
        extras_layout.addWidget(self.legend_loc, 0, 2)

        # --- Add all groups to main layout ---
        layout.addWidget(general_group)
        layout.addWidget(appearance_group)
        layout.addWidget(axes_group)
        layout.addWidget(extras_group)
        
        layout.addStretch()

        self.apply_styles()

    def create_config(self, path, raw_x, raw_y) -> BarConfig:
        config = BarConfig(
            path=path,
            title=self.title_input.text(),
            categories=raw_x,
            values=raw_y,
            x_label=self.x_input.text(),
            y_label=self.y_input.text(),
            color=self.color_input.currentText(),
            is_grid=self.is_grid.isChecked(),
            
            # Appending new settings
            orientation=self.orientation.currentText(),
            bar_width=self.bar_width.value(),
            edge_color=self.edge_color.currentText(),
            edge_width=self.edge_width.value(),
            alpha=self.alpha.value(),
            x_min=self.x_min.text(),
            x_max=self.x_max.text(),
            y_min=self.y_min.text(),
            y_max=self.y_max.text(),
            log_x=self.log_x.isChecked(),
            log_y=self.log_y.isChecked(),
            tick_rotation=self.tick_rotation.value(),
            show_legend=self.show_legend.isChecked(),
            legend_loc=self.legend_loc.currentText(),
            title_font_size=self.title_font_size.value(),
            axis_font_size=self.axis_font_size.value()
        )
        return config

    def load_ui(self, cfg: BarConfig):
        # Base settings
        self.title_input.setText(str(cfg.title) if cfg.title else "")
        self.x_input.setText(str(cfg.x_label) if cfg.x_label else "")
        self.y_input.setText(str(cfg.y_label) if cfg.y_label else "")
        
        # Safe loading for newer properties using getattr
        self.color_input.setCurrentText(getattr(cfg, 'color', 'Blue'))
        self.is_grid.setChecked(bool(getattr(cfg, 'is_grid', False)))
        
        self.orientation.setCurrentText(getattr(cfg, 'orientation', 'vertical'))
        self.bar_width.setValue(float(getattr(cfg, 'bar_width', 0.8)))
        self.edge_color.setCurrentText(getattr(cfg, 'edge_color', 'None'))
        self.edge_width.setValue(float(getattr(cfg, 'edge_width', 0.0)))
        self.alpha.setValue(float(getattr(cfg, 'alpha', 1.0)))
        
        self.x_min.setText(str(getattr(cfg, 'x_min', '')))
        self.x_max.setText(str(getattr(cfg, 'x_max', '')))
        self.y_min.setText(str(getattr(cfg, 'y_min', '')))
        self.y_max.setText(str(getattr(cfg, 'y_max', '')))
        
        self.log_x.setChecked(bool(getattr(cfg, 'log_x', False)))
        self.log_y.setChecked(bool(getattr(cfg, 'log_y', False)))
        self.tick_rotation.setValue(int(getattr(cfg, 'tick_rotation', 0)))
        
        self.show_legend.setChecked(bool(getattr(cfg, 'show_legend', False)))
        self.legend_loc.setCurrentText(getattr(cfg, 'legend_loc', 'best'))
        
        self.title_font_size.setValue(int(getattr(cfg, 'title_font_size', 12)))
        self.axis_font_size.setValue(int(getattr(cfg, 'axis_font_size', 10)))

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                color: #444444;
                font-weight: bold;
            }

            QGroupBox {
                border: 1px solid #D0D4D9;
                border-radius: 6px;
                margin-top: 14px; 
                padding-top: 12px;
                background-color: #FAFBFC;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #2C3E50;
                font-weight: bold;
                font-size: 13px;
            }

            QCheckBox {
                color: #333333;
                font-size: 13px;
                spacing: 6px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #A0AAB5;
                background-color: #FFFFFF;
                border-radius: 4px;
            }

            QCheckBox::indicator:checked {
                background-color: #4A90E2;
                border: 1px solid #4A90E2;
                image: url(black_check_mark.png); 
            }

            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                padding: 4px 6px;
                min-height: 20px;
            }

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 1px solid #4A90E2;
                background-color: #F0F8FF;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)       
