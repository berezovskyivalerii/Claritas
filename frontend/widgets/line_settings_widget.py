from PySide6.QtWidgets import (QLineEdit, QComboBox, QCheckBox, QWidget, 
                               QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                               QGroupBox, QGridLayout, QScrollArea)
from PySide6.QtCore import Qt, Signal
from config.config import LineConfig

class LineSettingsWidget(QWidget):
    request_chart_draw = Signal(str, object)
    
    def __init__(self):
        super().__init__()
        # Main layout for the widget itself
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove margins around scroll area
        
        # --- Create Scroll Area ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame) # Clean look
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # --- Create Container Widget for Scroll Area ---
        container_widget = QWidget()
        layout = QVBoxLayout(container_widget)
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
        self.color_input.addItems(['#2563EB', '#EF4444', '#10B981', '#F59E0B', '#111827']) # Updated defaults
        # Optional: You can keep color names if your backend handles them, 
        # but HEX codes matching our Ocean Blue theme look more professional.

        self.is_grid = QCheckBox("Grid")

        # --- Line Appearance ---
        self.line_style = QComboBox()
        self.line_style.addItems(['solid', 'dashed', 'dotted', 'dashdot'])

        self.line_width = QDoubleSpinBox()
        self.line_width.setRange(0.1, 10.0)
        self.line_width.setValue(1.5)
        self.line_width.setSingleStep(0.5)

        # --- Markers ---
        self.marker_style = QComboBox()
        self.marker_style.addItems(['None', 'o', 's', '^', 'D'])

        self.marker_size = QSpinBox()
        self.marker_size.setRange(1, 20)
        self.marker_size.setValue(5)

        # --- Axis Limits ---
        self.x_min = QLineEdit()
        self.x_min.setPlaceholderText("X Min")
        self.x_max = QLineEdit()
        self.x_max.setPlaceholderText("X Max")
        self.y_min = QLineEdit()
        self.y_min.setPlaceholderText("Y Min")
        self.y_max = QLineEdit()
        self.y_max.setPlaceholderText("Y Max")

        # --- Log Scale & Tick Rotation ---
        self.log_x = QCheckBox("Log X")
        self.log_y = QCheckBox("Log Y")

        self.tick_rotation = QSpinBox()
        self.tick_rotation.setRange(0, 360)
        self.tick_rotation.setValue(0)

        # --- Legend & Fill ---
        self.show_legend = QCheckBox("Legend")
        self.legend_loc = QComboBox()
        self.legend_loc.addItems(['best', 'upper right', 'upper left', 'lower left', 'lower right'])

        self.fill_under = QCheckBox("Fill Under")
        self.alpha = QDoubleSpinBox()
        self.alpha.setRange(0.1, 1.0)
        self.alpha.setValue(1.0)
        self.alpha.setSingleStep(0.1)

        # --- Fonts ---
        self.title_font_size = QSpinBox()
        self.title_font_size.setRange(8, 32)
        self.title_font_size.setValue(14)

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

        # --- Create Group: Line & Markers ---
        appearance_group = QGroupBox("Line & Markers")
        appearance_layout = QGridLayout(appearance_group)
        
        appearance_layout.addWidget(QLabel("Color:"), 0, 0)
        appearance_layout.addWidget(self.color_input, 0, 1)
        appearance_layout.addWidget(QLabel("Style:"), 0, 2)
        appearance_layout.addWidget(self.line_style, 0, 3)
        
        appearance_layout.addWidget(QLabel("Width:"), 1, 0)
        appearance_layout.addWidget(self.line_width, 1, 1)
        appearance_layout.addWidget(QLabel("Alpha:"), 1, 2)
        appearance_layout.addWidget(self.alpha, 1, 3)
        
        appearance_layout.addWidget(QLabel("Marker:"), 2, 0)
        appearance_layout.addWidget(self.marker_style, 2, 1)
        appearance_layout.addWidget(QLabel("Size:"), 2, 2)
        appearance_layout.addWidget(self.marker_size, 2, 3)

        # --- Create Group: Axes & Limits ---
        axes_group = QGroupBox("Axes & Limits")
        axes_layout = QGridLayout(axes_group)
        
        axes_layout.addWidget(self.x_min, 0, 0)
        axes_layout.addWidget(self.x_max, 0, 1)
        axes_layout.addWidget(self.y_min, 1, 0)
        axes_layout.addWidget(self.y_max, 1, 1)
        
        # Group Checkboxes and small inputs together tightly
        axes_layout.addWidget(self.log_x, 2, 0)
        axes_layout.addWidget(self.log_y, 2, 1)
        axes_layout.addWidget(self.is_grid, 3, 0)
        
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        rotation_layout.addWidget(self.tick_rotation)
        axes_layout.addLayout(rotation_layout, 3, 1)

        # --- Create Group: Extras ---
        extras_group = QGroupBox("Legend & Fill")
        extras_layout = QGridLayout(extras_group)
        
        extras_layout.addWidget(self.show_legend, 0, 0)
        extras_layout.addWidget(QLabel("Pos:"), 0, 1)
        extras_layout.addWidget(self.legend_loc, 0, 2)
        extras_layout.addWidget(self.fill_under, 1, 0, 1, 3)

        # --- Add all groups to the container layout ---
        layout.addWidget(general_group)
        layout.addWidget(appearance_group)
        layout.addWidget(axes_group)
        layout.addWidget(extras_group)
        
        # Set the container widget to the scroll area
        scroll_area.setWidget(container_widget)
        
        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.apply_styles()

    def create_config(self, path, raw_x, raw_y) -> LineConfig:
        config = LineConfig(
            path=path,
            title=self.title_input.text(),
            x_data=raw_x,
            y_data=raw_y,
            x_label=self.x_input.text(),
            y_label=self.y_input.text(),
            color=self.color_input.currentText(),
            is_grid=self.is_grid.isChecked(),
            
            # Appending new settings
            line_style=self.line_style.currentText(),
            line_width=self.line_width.value(),
            marker_style=self.marker_style.currentText(),
            marker_size=self.marker_size.value(),
            x_min=self.x_min.text(),
            x_max=self.x_max.text(),
            y_min=self.y_min.text(),
            y_max=self.y_max.text(),
            log_x=self.log_x.isChecked(),
            log_y=self.log_y.isChecked(),
            tick_rotation=self.tick_rotation.value(),
            show_legend=self.show_legend.isChecked(),
            legend_loc=self.legend_loc.currentText(),
            fill_under=self.fill_under.isChecked(),
            alpha=self.alpha.value(),
            title_font_size=self.title_font_size.value(),
            axis_font_size=self.axis_font_size.value()
        )
        return config

    def load_ui(self, cfg: LineConfig):
        # Base settings
        self.title_input.setText(str(cfg.title) if cfg.title else "")
        self.x_input.setText(str(cfg.x_label) if cfg.x_label else "")
        self.y_input.setText(str(cfg.y_label) if cfg.y_label else "")
        
        # Ensure the color combo box has the value before setting it
        color_text = str(cfg.color) if cfg.color else "#2563EB"
        if self.color_input.findText(color_text) == -1:
            self.color_input.addItem(color_text)
        self.color_input.setCurrentText(color_text)
        
        # Boolean handling for JSON consistency
        self.is_grid.setChecked(bool(getattr(cfg, 'is_grid', False)))

        # Loading new properties safely using getattr
        self.line_style.setCurrentText(getattr(cfg, 'line_style', 'solid'))
        self.line_width.setValue(float(getattr(cfg, 'line_width', 1.5)))
        self.marker_style.setCurrentText(getattr(cfg, 'marker_style', 'None'))
        self.marker_size.setValue(int(getattr(cfg, 'marker_size', 5)))
        
        self.x_min.setText(str(getattr(cfg, 'x_min', '')))
        self.x_max.setText(str(getattr(cfg, 'x_max', '')))
        self.y_min.setText(str(getattr(cfg, 'y_min', '')))
        self.y_max.setText(str(getattr(cfg, 'y_max', '')))
        
        self.log_x.setChecked(bool(getattr(cfg, 'log_x', False)))
        self.log_y.setChecked(bool(getattr(cfg, 'log_y', False)))
        self.tick_rotation.setValue(int(getattr(cfg, 'tick_rotation', 0)))
        
        self.show_legend.setChecked(bool(getattr(cfg, 'show_legend', False)))
        self.legend_loc.setCurrentText(getattr(cfg, 'legend_loc', 'best'))
        self.fill_under.setChecked(bool(getattr(cfg, 'fill_under', False)))
        self.alpha.setValue(float(getattr(cfg, 'alpha', 1.0)))
        
        self.title_font_size.setValue(int(getattr(cfg, 'title_font_size', 14)))
        self.axis_font_size.setValue(int(getattr(cfg, 'axis_font_size', 10)))

    def apply_styles(self):
        # Updated to match the Ocean Blue / Postman Light theme
        self.setStyleSheet("""
            /* Base Label Style */
            QLabel {
                color: #6B6B6B;
                font-weight: bold;
                font-size: 11px;
            }

            /* Modern GroupBox Styling */
            QGroupBox {
                border: 1px solid #EAEAEA;
                border-radius: 6px;
                margin-top: 10px; 
                padding-top: 15px;
                background-color: #FFFFFF;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #212121;
                font-weight: bold;
                font-size: 12px;
            }

            /* Checkbox Styling */
            QCheckBox {
                color: #212121;
                font-size: 12px;
                spacing: 6px;
            }

            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
                border-radius: 3px;
            }

            QCheckBox::indicator:checked {
                background-color: #2563EB;
                border: 1px solid #2563EB;
                /* Note: Ensure black_check_mark.png exists, or use a white one for better contrast against blue */
            }

            /* Uniform Inputs Styling */
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #FFFFFF;
                color: #212121;
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                padding: 4px 6px;
                min-height: 22px;
                font-size: 12px;
            }

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 1px solid #3B82F6;
                background-color: #F8FAFC;
            }
            
            /* ScrollBar Styling to look clean */
            QScrollBar:vertical {
                border: none;
                background: #FAFAFA;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
