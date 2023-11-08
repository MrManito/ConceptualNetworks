button_style_normal = (
    "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
    "QPushButton:hover { background-color: darkgray;}"
)

button_style_add = (
    "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
    "QPushButton:hover { background-color: #2980b9; }"
    "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
)

button_style_delete = (
    "QPushButton { border-radius: 10px; padding: 10px; background-color: #e74c3c; color: white; }"
    "QPushButton:hover { background-color: #c0392b; }"
    "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
    "QPushButton:pressed { background-color: #d35400; }"
)

button_style_warming = (
    "QPushButton { border-radius: 10px; padding: 10px; background-color: #FFA500; color: white; }"
    "QPushButton:hover { background-color: #FFC04D; }"
)

list_style = (
    "QListWidget { background-color: #f0f0f0;  }"
    "QListWidget::item { background-color: #ffffff; border: 1px solid #d0d0d0; padding: 10px; }"
    "QListWidget::item:selected { background-color: #3498db; color: white; }"
)

label_style_title = (
    "QLabel { padding: 5px; font-weight: bold; font-size: 16px; }"
)

input_txt_style = (
    "QLineEdit { background-color: #f0f0f0; border: 2px solid #3498db; padding: 5px; color: #333; }"
    "QLineEdit:hover { border-color: #2980b9; }"
    "QLineEdit:focus { border-color: #e74c3c; }"
)

label_style_progress_bar = (
    "QLabel { background-color: #3498db; color: white; padding: 10px; border-radius: 5px; max-width: 250px; }"
)

progress_bar_style = (
    "QProgressBar { background-color: #f0f0f0; border: 1px solid #d0d0d0; border-radius: 5px; text-align: center; }"
    "QProgressBar::chunk { background-color: #3498db; border-radius: 5px; }"
)

about_style = (
    "QPushButton {border-radius: 10px; padding: 10px; background-color: #3498db; color: white; border: 2px solid #2980b9; }"
    "QPushButton:hover {background-color: #2980b9;}"
)

table_header_style = (
    "QHeaderView::section { background-color: #3498db; color: white; }"
)

frame_borders_style = (
    "border: 2px solid black;"
)

combobox_normal_style = (
    "QComboBox { background-color: white; color: #333; border: 1px solid #ccc; padding: 5px; }"
)

checkbox_style = (
    """
        QCheckBox {
            spacing: 5px;
            color: #333;
        }
    
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            background-color: #FFFFFF;
            border: 2px solid #333;
            border-radius: 10px;
        }
    
        QCheckBox::indicator:checked {
            background-color: #2980b9; 
            border: 2px solid #000000; 
        }
    
        QCheckBox::indicator:unchecked {
            background-color: #FFFFFF;
            border: 2px solid #333; 
        }
    """
)

button_style_selection = (
    "QPushButton { border-radius: 5px; background-color: gray; color: white; }"
    "QPushButton:hover { background-color: darkgray;}"
)

progress_bar_circular_style = (
    """
        QProgressBar {
            border: 2px solid gray;
            border-radius: 10px;
            background-color: #E0E0E0;
        }
        QProgressBar::chunk {
            background-color: #1E90FF;
            width: 10px;
            margin: 0.5px;
            border-radius: 5px;
        }
    """
)


