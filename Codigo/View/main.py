# PyQt6 dependencies
import csv

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QColorDialog, QTableWidget, QSpinBox, QTableWidgetItem, QTabWidget, QDialog, \
    QMessageBox, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QPushButton, QLineEdit, \
    QWidget, QLabel, QProgressBar, QComboBox, QCheckBox, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSlider, \
    QTextBrowser
from PyQt6.QtGui import QIcon, QPalette, QPixmap, QTextCursor, QTextCharFormat

import matplotlib.pyplot as plt
import matplotlib.font_manager
import networkx as nx
import numpy as np
from PIL import Image
from random import randint

# Import the main controller
from Codigo.Controller.Controller import MainController

# Import the Ignore word dialog
from Codigo.View.IgnoreWordsDialog import IgnoreWordsDialog

# Import the Thread using to the interface process
from Codigo.View.GraphThread import GraphThread

# Import the Thread using to the interface process
from Codigo.View.CloudThread import CloudThread

# Import the Thread using to the interface process
from Codigo.View.NetworkThread import NetworkThread

# Import the Thread using to the interface process
from Codigo.Model.StructureStemming import StructureStemming

# Import the stemming structure class
from Codigo.View.SVGWidget import SVGWidget

# Import the style sheets
from Codigo.View.Styles.Styles import *

# Import of the system managers
import sys
import os

codigo_dir = os.path.dirname(os.path.abspath(__file__))
codigo_dir = os.path.join(codigo_dir, '..')  # Path file level up
codigo_dir = os.path.join(codigo_dir, '..')
sys.path.append(codigo_dir)

path = ""

import matplotlib.backends.backend_qt5agg
import matplotlib.backends.backend_svg
matplotlib.use('Qt5Agg')


# matplotlib.use('TkAgg')
def resource_path(relative_path):
    global path
    try:
        base_path = os.path.dirname(__file__)
        path = base_path
    except:
        base_path = os.path.abspath(".")
        path = base_path
    return os.path.join(base_path, relative_path)


# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Interface control variables
        self.cloudParameters = {'width': 512, 'height': 512, 'background_color': (255, 255, 255),
                                'color': (255, 255, 255), 'mask': None, 'font': None}
        self.num_func_words = 0
        self.page_size = 50  # Table Page Size
        self.current_page = 1  # Actual page
        self.word_freq_dict = StructureStemming()
        self.fonts = {}
        # Main controller class
        self.mainController = MainController()

        # IgnoreWords dialog
        self.ignore_words_dialog = IgnoreWordsDialog(self.mainController)

        # Define the layout of the window
        self.setWindowTitle("Conceptual Networks")
        self.resize(1000, 600)  # Set the window size

        self.mwlayout = QGridLayout()
        self.mwlayout.setSpacing(10)

        #Graph Default Colors
        self.nodeColor = 'lightblue'
        self.graphcolor = '#00aae4'

        url_layout = QHBoxLayout()
        files_layout = QVBoxLayout()

        # The list widget
        list_widget_container = QWidget()
        list_widget_container_layout = QVBoxLayout()
        list_widget_container.setLayout(list_widget_container_layout)
        lbl_layout = QVBoxLayout()
        list_widget_container_layout.addLayout(lbl_layout)

        list_label = QLabel("Lista de Archivos")
        list_label.setStyleSheet(label_style_title)

        lbl_layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(list_style)

        list_widget_container_layout.addWidget(self.file_list)
        lbl_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        list_widget_container_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.mwlayout.addWidget(list_widget_container, 0, 0)

        # Title lable of the file space
        lbl_actions_title_layout = QVBoxLayout()
        file_label = QLabel("Acciones")
        file_label.setStyleSheet(label_style_title)

        lbl_actions_title_layout.addWidget(file_label)

        lbl_actions_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        files_layout.addLayout(lbl_actions_title_layout)
        # Text box to contain the URL
        self.url_txb = QLineEdit()
        self.url_txb.setStyleSheet(input_txt_style)
        url_layout.addWidget(self.url_txb)

        # Button to add the URL to the file list
        url_path = resource_path("Icons/globo.png")
        url_icon = QIcon(url_path)
        add_url_btn = QPushButton("Añadir URL")
        add_url_btn.setToolTip("Añade el URL ingresado a la lista de elementos")
        add_url_btn.setStyleSheet(button_style_add)
        add_url_btn.setIcon(url_icon)
        add_url_btn.clicked.connect(self.add_url_to_list)
        url_layout.addWidget(add_url_btn)

        files_layout.addLayout(url_layout)

        file_btn_layout = QHBoxLayout()
        # Add a button to add files
        doc_path = resource_path("Icons/documento.png")
        doc_icon = QIcon(doc_path)
        add_files_frame_btn = QPushButton("Añadir Archivo")
        add_files_frame_btn.setToolTip("Abre un diálogo para seleccionar un archivo")
        add_files_frame_btn.setIcon(doc_icon)
        add_files_frame_btn.clicked.connect(self.add_files)
        add_files_frame_btn.setStyleSheet(button_style_add)

        file_btn_layout.addWidget(add_files_frame_btn)

        # Add a remove item button
        remove_path = resource_path("Icons/basura.png")
        remove_icon = QIcon(remove_path)
        self.remove_button = QPushButton("Remover Archivo")
        self.remove_button.setToolTip("Remueve un elemento seleccionado en la lista")
        self.remove_button.setIcon(remove_icon)
        self.remove_button.setStyleSheet(button_style_delete)
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setEnabled(False)  # Desactivate the button

        file_btn_layout.addWidget(self.remove_button)

        # Add ignored words
        ignore_path = resource_path("Icons/comprobacion-de-lista.png")
        ignore_icon = QIcon(ignore_path)
        ignore_btn = QPushButton("Añadir Palabras Ignoradas")
        ignore_btn.setToolTip("Abre la ventana de gestion de palabras a ignorar")
        ignore_btn.setIcon(ignore_icon)
        ignore_btn.setStyleSheet(button_style_normal)
        ignore_btn.clicked.connect(self.open_dialog)
        file_btn_layout.addWidget(ignore_btn)

        files_layout.addLayout(file_btn_layout)

        self.file_list.itemSelectionChanged.connect(self.update_remove_button)

        files_layout.addStretch(1)
        self.mwlayout.addLayout(files_layout, 0, 2)

        # Add a button to start the creation of the graph
        add_path = resource_path("Icons/agregar.png")
        graph_icon = QIcon(add_path)
        self.create_graph_btn = QPushButton("Procesar Texto")
        self.create_graph_btn.setToolTip("Envia a procesar los archivos y URL agregados")
        self.create_graph_btn.setIcon(graph_icon)
        self.create_graph_btn.setStyleSheet(button_style_add)
        self.create_graph_btn.clicked.connect(self.create_graph)
        self.create_graph_btn.setEnabled(False)
        self.mwlayout.addWidget(self.create_graph_btn, 1, 1)

        # Creation of a widget with a label and a progress bar
        self.progressb_widget = QWidget()

        self.progressbar_layout = QHBoxLayout()

        self.pbar_lb = QLabel("Iniciando Proceso")
        self.pbar_lb.setStyleSheet(label_style_progress_bar)
        self.progressbar_layout.addWidget(self.pbar_lb)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(progress_bar_style)
        self.progressbar_layout.addWidget(self.progress_bar)

        self.progressb_widget.setLayout(self.progressbar_layout)
        self.mwlayout.addWidget(self.progressb_widget, 2, 0)

        self.progressb_widget.setVisible(False)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.tab_widget)

        # About button
        info_path = resource_path("Icons/informacion.png")
        about_icon = QIcon(info_path)
        self.about_button = QPushButton("")
        self.about_button.setIcon(about_icon)
        self.about_button.setFixedSize(30, 30)
        self.about_button.setStyleSheet(about_style)
        self.about_button.clicked.connect(self.show_about_dialog)
        self.central_layout.addWidget(self.about_button)

        # Tab widgets
        self.files_widget = QWidget()
        self.table_widget = QWidget()
        self.text_visualizer_widget = QWidget()
        self.conceptual_cloud_widget = QWidget()
        self.conceptual_network_widget = QWidget()

        # Set the widgets to the window
        self.tab_widget.addTab(self.files_widget, "Archivos")
        self.tab_widget.addTab(self.table_widget, "Estadísticas")
        self.tab_widget.addTab(self.text_visualizer_widget, "Citas")
        self.tab_widget.addTab(self.conceptual_cloud_widget, "Nube de Conceptos")
        self.tab_widget.addTab(self.conceptual_network_widget, "Red de Conceptos")

        # Set the content
        # Files menus
        self.files_widget.setLayout(self.mwlayout)

        # Table and graph menus
        statistics_layout = QHBoxLayout()

        # Create a table with the necessary columns and buttons
        self.table_view_widget = QWidget()
        table_view_widget_layout = QVBoxLayout()
        self.table_view_widget.setLayout(table_view_widget_layout)

        # Creation of the filter
        self.filterComboBox = QComboBox()
        self.filterComboBox.addItem("A - Z")
        self.filterComboBox.addItem("Peso")
        self.filterComboBox.setStyleSheet(combobox_normal_style)
        self.filterComboBox.setToolTip("Ordena la tabla segun la selección")

        filter_widget = QWidget()
        filter_widget_layout = QHBoxLayout()
        filter_widget.setLayout(filter_widget_layout)
        filter_label = QLabel()
        filter_label_icon = QIcon(resource_path("Icons/ordenar-alt.png"))
        filter_label.setPixmap(filter_label_icon.pixmap(15, 15))

        export_table_stats = QPushButton("Exportar Tabla")
        export_table_stats.setStyleSheet(button_style_warming)
        export_table_stats.setToolTip("Exporta las raíces y su frecuencia en un archivo CSV")
        export_table_stats.setIcon(QIcon(resource_path("Icons/descargar.png")))
        export_table_stats.clicked.connect(self.export_table)

        filter_widget_layout.addWidget(filter_label)

        self.filterComboBox.activated.connect(self.onFilterComboBoxActivated)
        filter_widget_layout.addWidget(self.filterComboBox)

        filter_widget_layout.addWidget(export_table_stats)
        table_view_widget_layout.addWidget(filter_widget)


        # Creation of the table interface
        self.table_info_widget = QTableWidget()
        self.table_info_widget.setColumnCount(4)
        header = self.table_info_widget.horizontalHeader()
        header.setStyleSheet(table_header_style)
        self.table_info_widget.setHorizontalHeaderLabels(["Raíz", "Palabras", "Frecuencia", "Porcentaje"])
        table_view_widget_layout.addWidget(self.table_info_widget)

        # Creation of the page menu of the table
        self.pagination_widget = QWidget()
        pagination_layout = QHBoxLayout()
        self.pagination_widget.setLayout(pagination_layout)

        prev_path = resource_path("Icons/angulo-izquierdo.png")
        prevIcon = QIcon(prev_path)
        self.prevButton = QPushButton("")
        self.prevButton.setToolTip("Anterior")
        self.prevButton.setStyleSheet(button_style_add)
        self.prevButton.setIcon(prevIcon)
        self.prevButton.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prevButton)

        self.pageLabel1 = QLabel("Página ")
        self.tpg_number_input = QSpinBox(self)
        self.tpg_number_input.setMinimum(1)  # Valor mínimo permitido
        self.tpg_number_input.setMaximum(10000)
        self.tpg_number_input.setValue(1)  # Valor predeterminado
        self.tpg_number_input.editingFinished.connect(self.validate_table_nav_text)

        self.pageLabel2 = QLabel(" de 1")
        self.pageLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pageLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pagination_layout.addWidget(self.pageLabel1)
        pagination_layout.addWidget(self.tpg_number_input)
        pagination_layout.addWidget(self.pageLabel2)

        next_path = resource_path("Icons/angulo-derecho.png")
        nextIcon = QIcon(next_path)
        self.nextButton = QPushButton("")
        self.nextButton.setToolTip("Siguiente")
        self.nextButton.setStyleSheet(button_style_add)
        self.nextButton.setIcon(nextIcon)
        self.nextButton.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.nextButton)

        table_view_widget_layout.addWidget(self.pagination_widget)

        statistics_layout.addWidget(self.table_view_widget)

        # List of combine roots widget
        self.root_list = QWidget()
        root_list_layout = QVBoxLayout()
        combine_list_label = QLabel("Combinar Raices")
        combine_list_label.setStyleSheet(label_style_title)
        combine_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root_list_layout.addWidget(combine_list_label)
        self.root_list_list = QListWidget()
        self.root_list_list.setStyleSheet(list_style)
        root_list_layout.addWidget(self.root_list_list)

        self.botton_bar = QWidget()
        botton_bar_layout = QHBoxLayout()

        add_root_button = QPushButton('Añadir')
        add_root_button.setToolTip("Añadir raíz a la lista de combinación")
        add_root_button.setIcon(QIcon(resource_path("Icons/agregar.png")))
        add_root_button.setStyleSheet(button_style_add)
        self.remove_root_button = QPushButton('Eliminar')
        self.remove_root_button.setToolTip("Eliminar raíz de la lista de combinación")
        self.remove_root_button.setIcon(QIcon(resource_path("Icons/basura.png")))
        self.remove_root_button.setStyleSheet(button_style_delete)
        combine_root_button = QPushButton('Combinar')
        combine_root_button.setToolTip("Combina las palabras en la lista de raices a combinar")
        combine_root_button.setIcon(QIcon(resource_path("Icons/controlar.png")))
        combine_root_button.setStyleSheet(button_style_normal)

        add_root_button.clicked.connect(self.add_item_to_root_list)
        self.remove_root_button.clicked.connect(self.remove_item_from_root_list)

        self.remove_root_button.setEnabled(False)

        self.root_list_list.itemSelectionChanged.connect(self.update_root_remove_button)
        combine_root_button.clicked.connect(self.combine_roots)

        botton_bar_layout.addWidget(add_root_button)
        botton_bar_layout.addWidget(self.remove_root_button)
        botton_bar_layout.addWidget(combine_root_button)

        self.botton_bar.setLayout(botton_bar_layout)
        root_list_layout.addWidget(self.botton_bar)
        self.root_list.setLayout(root_list_layout)
        statistics_layout.addWidget(self.root_list)
        self.table_widget.setLayout(statistics_layout)
        self.tab_widget.setTabEnabled(1, False)

        # -------------------------------------Cites-------------------------------------
        text_visualizer_widget_layout = QHBoxLayout()
        self.text_visualizer_widget.setLayout(text_visualizer_widget_layout)

        # Crear el visor de texto
        self.text_browser = QTextBrowser()

        # Crear el widget de búsqueda
        search_widget = QWidget()
        search_layout = QVBoxLayout()

        # Crear un campo de entrada para la palabra clave
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet(input_txt_style)
        search_layout.addWidget(self.search_input)

        # Crear un botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_text)
        search_button.setStyleSheet(button_style_add)
        search_layout.addWidget(search_button)

        search_widget.setLayout(search_layout)

        self.cites_text_widget = QWidget()
        cites_text_widget_layout = QVBoxLayout()
        self.cites_text_widget.setLayout(cites_text_widget_layout)

        cites_text_widget_layout.addWidget(search_widget)

        cites_text_widget_layout.addWidget(self.text_browser)

        text_visualizer_widget_layout.addWidget(self.cites_text_widget)

        self.cites_list_widget = QWidget()
        cites_list_widget_layout = QVBoxLayout()
        self.cites_list_widget.setLayout(cites_list_widget_layout)

        cites_title_lable = QLabel("Citas")
        cites_title_lable.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        cites_title_lable.setStyleSheet(label_style_title)
        cites_list_widget_layout.addWidget(cites_title_lable)

        self.cites_qlist = QListWidget()
        self.cites_qlist.setStyleSheet(list_style)
        self.cites_qlist.itemDoubleClicked.connect(self.on_double_click_cites_list_item)
        cites_list_widget_layout.addWidget(self.cites_qlist)

        text_visualizer_widget_layout.addWidget(self.cites_list_widget)

        # -------------------------------------Cites-------------------------------------

        # -------------------------------------Conceptual Cloud-------------------------------------
        # Here is the configuration of the conceptual cloud tab
        conceptual_cloud_widget_layout = QGridLayout()

        # Here comes the SVG
        # self.svg_image = SVGWidget()
        # self.svg_image.load_svg(resource_path("Icons/imagen-de-archivo.svg"))
        svg_image_widget = QWidget()
        svg_image_widget_layout = QVBoxLayout()
        svg_image_widget.setLayout(svg_image_widget_layout)

        self.info_label = QLabel()
        svg_image_widget_layout.addWidget(self.info_label)

        zoom_btn_widget = QWidget()
        zoom_btn_widget_layout = QHBoxLayout()
        zoom_btn_widget.setLayout(zoom_btn_widget_layout)

        self.zoom_in_button = QPushButton("")
        self.zoom_in_button.setIcon(QIcon(resource_path("Icons/acercarse.png")))
        self.zoom_in_button.setToolTip("Acerca la imagen")
        self.zoom_in_button.setStyleSheet(button_style_add)
        self.zoom_out_button = QPushButton("")
        self.zoom_out_button.setIcon(QIcon(resource_path("Icons/disminuir-el-zoom.png")))
        self.zoom_out_button.setToolTip("Aleja la imagen")
        self.zoom_out_button.setStyleSheet(button_style_add)
        zoom_btn_widget_layout.addWidget(self.zoom_in_button)
        zoom_btn_widget_layout.addWidget(self.zoom_out_button)

        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        svg_image_widget_layout.addWidget(zoom_btn_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # self.svg_image = QLabel()
        # self.svg_image.setPixmap(QPixmap(resource_path("Icons/imagen-de-archivo.png")))
        # self.svg_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # self.svg_image.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        svg_image_widget_layout.addWidget(self.view)

        self.image_progress_bar = QWidget()
        image_progress_bar_layout = QHBoxLayout()
        self.image_progress_bar.setLayout(image_progress_bar_layout)
        img_pgrsb_label = QLabel("Procesando")
        image_progress_bar_layout.addWidget(img_pgrsb_label)
        self.img_progress_bar = QProgressBar()
        self.img_progress_bar.setRange(0, 0)
        self.img_progress_bar.setTextVisible(False)
        self.img_progress_bar.setStyleSheet(progress_bar_circular_style)

        image_progress_bar_layout.addWidget(self.img_progress_bar)

        # Iniciar un temporizador para simular la carga
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_img_progress)

        svg_image_widget_layout.addWidget(self.image_progress_bar)

        self.image_progress_bar.setVisible(False)

        conceptual_cloud_widget_layout.addWidget(svg_image_widget, 0, 0)

        # Here comes the personalization tools
        self.svg_personalization_tools = QWidget()
        svg_personalization_tools_layout = QVBoxLayout()

        svg_label_tools = QLabel("Herramientas")
        svg_label_tools.setStyleSheet(label_style_title)
        svg_label_tools.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        svg_personalization_tools_layout.addWidget(svg_label_tools)

        self.cloud_personalization_menu = QWidget()
        cloud_personalization_menu_layout = QHBoxLayout()
        self.cloud_personalization_menu.setLayout(cloud_personalization_menu_layout)

        self.cloud_personalization_menu_colors = QWidget()
        cloud_personalization_menu_colors_layout = QVBoxLayout()
        self.cloud_personalization_menu_colors.setLayout(cloud_personalization_menu_colors_layout)
        color_label = QLabel("Color")
        color_label.setStyleSheet(label_style_title)
        cloud_personalization_menu_colors_layout.addWidget(color_label)

        self.color_selecctor = QWidget()
        color_selecctor_layout = QVBoxLayout()
        self.color_selecctor.setLayout(color_selecctor_layout)
        color_frame1_widget = QWidget()
        color_frame1_widget_layout = QHBoxLayout()
        color_frame1_widget.setLayout(color_frame1_widget_layout)
        self.color_frame = QWidget()
        self.color_frame.setMinimumSize(30, 30)
        self.color_frame.setMaximumSize(30, 30)
        self.color_frame.setStyleSheet(frame_borders_style)
        self.color_frame.setContentsMargins(0, 0, 0, 0)
        color_frame1_widget_layout.addWidget(self.color_frame)
        color_selector_button = QPushButton("")
        color_selector_button.setToolTip("Color de las palabras de la nube")
        color_selector_button.setIcon(QIcon(resource_path("Icons/angulo-pequeno-hacia-abajo.png")))
        color_selector_button.setStyleSheet(button_style_selection)
        color_selector_button.setMaximumSize(50, 30)
        color_selector_button.setContentsMargins(0, 0, 0, 0)
        color_selector_button.clicked.connect(self.changePalette)
        color_frame1_widget_layout.addWidget(color_selector_button)
        color_selecctor_layout.addWidget(color_frame1_widget)

        color_frame2_widget = QWidget()
        color_frame2_widget_layout = QHBoxLayout()
        color_frame2_widget.setLayout(color_frame2_widget_layout)
        self.color_frame2 = QWidget()
        self.color_frame2.setMinimumSize(30, 30)
        self.color_frame2.setMaximumSize(30, 30)
        self.color_frame2.setStyleSheet(frame_borders_style)
        self.color_frame2.setContentsMargins(0, 0, 0, 0)
        color_frame2_widget_layout.addWidget(self.color_frame2)

        background_color_selector_button = QPushButton("")
        background_color_selector_button.setToolTip("Color del fondo de la nube")
        background_color_selector_button.setIcon(QIcon(resource_path("Icons/angulo-pequeno-hacia-abajo.png")))
        background_color_selector_button.setStyleSheet(button_style_selection)
        background_color_selector_button.setMaximumSize(50, 30)
        background_color_selector_button.setContentsMargins(0, 0, 0, 0)
        background_color_selector_button.clicked.connect(self.changeBGPalette)
        color_frame2_widget_layout.addWidget(background_color_selector_button)
        color_selecctor_layout.addWidget(color_frame2_widget)

        cloud_personalization_menu_colors_layout.addWidget(self.color_selecctor)

        self.random_colors_chkbox = QCheckBox("Random")
        self.random_colors_chkbox.setChecked(True)
        self.random_colors_chkbox.setStyleSheet(checkbox_style)
        self.random_colors_chkbox.setToolTip("Selecciona el color de las palabras de forma aleatoria")

        color_selecctor_layout.addWidget(self.random_colors_chkbox)

        self.transparent_colors_chkbox = QCheckBox("Transparente")
        self.transparent_colors_chkbox.setChecked(True)
        self.transparent_colors_chkbox.setStyleSheet(checkbox_style)
        self.transparent_colors_chkbox.setToolTip("Hace que el fondo de la imagen sea transparente")

        color_selecctor_layout.addWidget(self.transparent_colors_chkbox)

        cloud_personalization_menu_layout.addWidget(self.cloud_personalization_menu_colors)

        self.cloud_personalization_menu_shape = QWidget()
        cloud_personalization_menu_shape_layout = QVBoxLayout()
        self.cloud_personalization_menu_shape.setLayout(cloud_personalization_menu_shape_layout)

        shape_label = QLabel("Figura")
        shape_label.setStyleSheet(label_style_title)
        cloud_personalization_menu_shape_layout.addWidget(shape_label)

        self.shape_widget = QWidget()
        shape_widget_layout = QHBoxLayout()
        self.shape_widget.setLayout(shape_widget_layout)
        self.shape_img_label = QLabel()
        shape_img_label_icon = QIcon(resource_path("Icons/imagen-de-archivo.png"))
        self.shape_img_label.setPixmap(shape_img_label_icon.pixmap(50, 50))
        shape_widget_layout.addWidget(self.shape_img_label)
        shape_buttons_widget = QWidget()
        shape_buttons_widget_layout = QVBoxLayout()
        shape_buttons_widget.setLayout(shape_buttons_widget_layout)
        shape_selection_button = QPushButton("Añadir")
        shape_selection_button.setIcon(QIcon(resource_path("Icons/recursos.png")))
        shape_selection_button.setToolTip("Añade una mascara a la creación de la nube")
        shape_selection_button.setStyleSheet(button_style_add)
        shape_selection_button.clicked.connect(self.selectMask)
        shape_buttons_widget_layout.addWidget(shape_selection_button)
        shape_delete_button = QPushButton("Quitar")
        shape_delete_button.setIcon(QIcon(resource_path("Icons/basura.png")))
        shape_delete_button.setToolTip("Quita la mascara agregada")
        shape_delete_button.setStyleSheet(button_style_delete)
        shape_delete_button.clicked.connect(self.deleteselectMask)
        shape_buttons_widget_layout.addWidget(shape_delete_button)
        shape_widget_layout.addWidget(shape_buttons_widget)

        cloud_personalization_menu_shape_layout.addWidget(self.shape_widget)

        self.shapeComboBox = QComboBox()
        self.shapeComboBox.setStyleSheet(combobox_normal_style)
        self.shapeComboBox.setToolTip("Tamaño de la figura")
        self.shapeComboBox.addItem("512x512")
        self.shapeComboBox.addItem("800x600")
        self.shapeComboBox.addItem("1080x720")
        self.shapeComboBox.addItem("2560x1440")
        self.shapeComboBox.addItem("3840x2160")

        cloud_personalization_menu_shape_layout.addWidget(self.shapeComboBox)

        cloud_personalization_menu_layout.addWidget(self.cloud_personalization_menu_shape)

        svg_personalization_tools_layout.addWidget(self.cloud_personalization_menu)

        self.shapeComboBox.activated.connect(self.onZiseComboboxActivivated)

        self.font_widget = QWidget()
        font_widget_layout = QHBoxLayout()
        self.font_widget.setLayout(font_widget_layout)
        font_label = QLabel("Tipografía")
        font_label.setStyleSheet(label_style_title)
        self.font_combobox = QComboBox()
        self.font_combobox.setToolTip("Selección de la tipografía")
        self.font_combobox.setStyleSheet(combobox_normal_style)
        self.fill_font_combobox()
        font_widget_layout.addWidget(font_label)
        font_widget_layout.addWidget(self.font_combobox)

        svg_personalization_tools_layout.addWidget(self.font_widget)

        self.select_word_func_widget = QWidget()
        select_word_func_widget_layout = QHBoxLayout()
        self.select_word_func_widget.setLayout(select_word_func_widget_layout)
        word_func_label = QLabel("Palabras")
        word_func_label.setStyleSheet(label_style_title)
        self.word_func_combobox = QComboBox()
        self.word_func_combobox.setToolTip("Selección del algoritmo de selección de palabras")
        self.word_func_combobox.setStyleSheet(combobox_normal_style)
        self.word_func_combobox.addItem("Primera en aparecer")
        self.word_func_combobox.addItem("Con más apariciones")
        self.word_func_combobox.addItem("Mas corta")
        select_word_func_widget_layout.addWidget(word_func_label)
        select_word_func_widget_layout.addWidget(self.word_func_combobox)

        svg_personalization_tools_layout.addWidget(self.select_word_func_widget)

        self.font_combobox.activated.connect(self.onFontComboboxActivated)
        self.word_func_combobox.activated.connect(self.onFuncWordComboboxActivated)

        self.create_word_cloud_button = QPushButton("Crear Nube de Palabras")
        self.create_word_cloud_button.setIcon(QIcon(resource_path("Icons/rodillo.png")))
        self.create_word_cloud_button.setToolTip("Genera una nube de palabras con la configuración establecida")
        self.create_word_cloud_button.setStyleSheet(button_style_normal)
        self.create_word_cloud_button.clicked.connect(self.generate_word_cloud)

        svg_personalization_tools_layout.addWidget(self.create_word_cloud_button)

        export_word_cloud_button = QPushButton("Exportar Nube de Palabras")
        export_word_cloud_button.setIcon(QIcon(resource_path("Icons/descargar.png")))
        export_word_cloud_button.setToolTip("Exporta la imagen en un formato seleccionado")
        export_word_cloud_button.setStyleSheet(button_style_warming)
        export_word_cloud_button.clicked.connect(self.exportwordcloud)

        svg_personalization_tools_layout.addWidget(export_word_cloud_button)

        self.svg_personalization_tools.setLayout(svg_personalization_tools_layout)

        conceptual_cloud_widget_layout.addWidget(self.svg_personalization_tools, 0, 1)
        conceptual_cloud_widget_layout.setColumnStretch(0, 2)
        # Here the layout is loaded to the tab
        self.conceptual_cloud_widget.setLayout(conceptual_cloud_widget_layout)
        # ------------------------------Conceptual Cloud End------------------------------------------

        # ------------------------------Conceptual Network Tab------------------------------------------

        conceptual_network_widget_layout = QHBoxLayout()

        # Poner gráfico de red acá

        '''network_config_label = QLabel("Grafico")
        network_config_label.setStyleSheet(label_style_title)
        network_config_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)'''

        self.svg2_image = QLabel()
        self.svg2_image.setPixmap(QPixmap(resource_path("Icons/imagen-de-archivo.png")))
        self.svg2_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.svg2_image.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.conceptual_network_widget_vertical_widget = QWidget()
        conceptual_network_widget_vertical_layout = QVBoxLayout()
        self.conceptual_network_widget_vertical_widget.setLayout(conceptual_network_widget_vertical_layout)

        conceptual_network_widget_vertical_layout.addWidget(self.svg2_image)

        self.image_progress_bar2 = QWidget()
        image_progress_bar2_layout = QHBoxLayout()
        self.image_progress_bar2.setLayout(image_progress_bar2_layout)

        img_pgrsb2_label = QLabel("Procesando")
        image_progress_bar2_layout.addWidget(img_pgrsb2_label)
        self.img_progress_bar2 = QProgressBar()
        self.img_progress_bar2.setRange(0, 0)
        self.img_progress_bar2.setTextVisible(False)
        self.img_progress_bar2.setStyleSheet(progress_bar_circular_style)

        image_progress_bar2_layout.addWidget(self.img_progress_bar2)

        # Iniciar un temporizador para simular la carga
        self.loading_timer2 = QTimer()

        self.loading_timer2.timeout.connect(self.update_img_progress2)
        self.image_progress_bar2.setVisible(False)


        conceptual_network_widget_vertical_layout.addWidget(self.image_progress_bar2)
        conceptual_network_widget_layout.addWidget(self.conceptual_network_widget_vertical_widget)

        # onceptual_network_widget_layout.addWidget(network_config_label)

        conceptual_network_widget_vertical_layout = QVBoxLayout()

        network_config_label = QLabel("Configuraciones")
        network_config_label.setStyleSheet(label_style_title)
        network_config_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        conceptual_network_widget_vertical_layout.addWidget(network_config_label)

        # Node Edge Relation Selection Layout
        conceptual_network_widget_horizontal_inside_relation_layout = QHBoxLayout()

        relation_layout_label = QLabel("Cantidad de Saltos en Relaciones")
        relation_layout_label.setStyleSheet(label_style_title)
        self.relation_combobox = QComboBox()
        self.relation_combobox.setToolTip("Selección de Cantidad de Saltos en Relaciones Mínimas del Nodo")
        self.relation_combobox.addItem("1")
        self.relation_combobox.addItem("2")
        self.relation_combobox.addItem("3")
        self.relation_combobox.addItem("4")
        self.relation_combobox.addItem("5")
        self.relation_combobox.setStyleSheet(combobox_normal_style)

        #self.relation_combobox.currentIndexChanged.connect(self.network_relations_checkbok_manage)

        conceptual_network_widget_horizontal_inside_relation_layout.addWidget(relation_layout_label)
        conceptual_network_widget_horizontal_inside_relation_layout.addWidget(self.relation_combobox)


        #Graph Distribution Layout
        conceptual_network_widget_horizontal_graph_distro_layout = QHBoxLayout()

        graph_distro_label = QLabel("Distribución de Grafo")
        graph_distro_label.setStyleSheet(label_style_title)
        self.graph_distro_combobox = QComboBox()
        self.graph_distro_combobox.setToolTip("Selección Distribución de Grafo")
        self.graph_distro_combobox.setStyleSheet(combobox_normal_style)
        self.graph_distro_combobox.addItem("Default - Spring")                          #nx.spring_layout(graph, k=0.30)
        self.graph_distro_combobox.addItem("Kamada Kawaii")                             #nx.kamada_kawai_layout(graph)
        self.graph_distro_combobox.addItem("Random")                                    #nx.random_layout(graph)
        self.graph_distro_combobox.addItem("Shell")                                     #nx.shell_layout(graph)
        self.graph_distro_combobox.addItem("Spectral")                                  #nx.spectral_layout(graph)
        #self.graph_distro_combobox.addItem("Planar")                                   #nx.planar_layout(graph)
        self.graph_distro_combobox.addItem("Fruchterman Reingold")                      #nx.fruchterman_reingold_layout(graph, k=0.30)
        self.graph_distro_combobox.addItem("Spiral")                                    #nx.spiral_layout(graph)
        self.graph_distro_combobox.addItem("Arf")                                       #nx.arf_layout(graph)


        conceptual_network_widget_horizontal_graph_distro_layout.addWidget(graph_distro_label)
        conceptual_network_widget_horizontal_graph_distro_layout.addWidget(self.graph_distro_combobox)
        # self.typeword_combobox.currentIndexChanged.connect(self.network_relations_checkbok_manage)

        #Word Order Selection
        conceptual_network_widget_horizontal_inside_select_typeword_layout = QHBoxLayout()


        typeword_label = QLabel("Selección de Palabras")
        typeword_label.setStyleSheet(label_style_title)
        self.typeword_combobox = QComboBox()
        self.typeword_combobox.setToolTip("Selección del algoritmo de selección de palabras")
        self.typeword_combobox.setStyleSheet(combobox_normal_style)
        self.typeword_combobox.addItem("Primera en aparecer")
        self.typeword_combobox.addItem("Con más apariciones")
        self.typeword_combobox.addItem("Mas cortas")


        conceptual_network_widget_horizontal_inside_select_typeword_layout.addWidget(typeword_label)
        conceptual_network_widget_horizontal_inside_select_typeword_layout.addWidget(self.typeword_combobox)
        #self.typeword_combobox.currentIndexChanged.connect(self.network_relations_checkbok_manage)

        # Filter Selection Layout
        conceptual_network_widget_horizontal_inside_distribution_layout = QHBoxLayout()
        conceptual_network_widget_horizontal_inside_distribution_vertical_layout = QVBoxLayout()
        graph_layout_label = QLabel("Filtros:")
        graph_layout_label.setStyleSheet(label_style_title)

        filter_network_graph_layout = QHBoxLayout()
        #filter_network_graph_label = QLabel("Sí")
        self.filter_network_graph_Checkbox = QCheckBox()
        self.filter_network_graph_Checkbox.setStyleSheet(checkbox_style)

        #filter_network_graph_layout.addWidget(filter_network_graph_label)
        filter_network_graph_layout.addWidget(self.filter_network_graph_Checkbox)

        self.filter_network_graph_Checkbox.stateChanged.connect(self.network_checkbox_management)

        conceptual_network_widget_horizontal_inside_distribution_layout.addWidget(graph_layout_label)
        #conceptual_network_widget_horizontal_inside_distribution_vertical_layout.addLayout(general_network_graph_layout)
        conceptual_network_widget_horizontal_inside_distribution_vertical_layout.addLayout(filter_network_graph_layout)

        conceptual_network_widget_horizontal_inside_distribution_layout.addLayout(conceptual_network_widget_horizontal_inside_distribution_vertical_layout)


        # Node Size Selection Layout
        conceptual_network_widget_horizontal_inside_size_layout = QHBoxLayout()
        node_size_label = QLabel("Nodos De Aparición Mayor A")
        node_size_label.setStyleSheet(label_style_title)

        # Text box to get the node size
        self.NodeSize_txb = QLineEdit()
        self.NodeSize_txb.setStyleSheet(input_txt_style)

        #Slider to get the node size info
        #self.node_size_slider = QSlider(Qt.Orientation.Horizontal, self)
        #self.node_size_slider.setGeometry(50, 50, 200, 50)

        #self.node_size_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        #self.node_size_slider.setMinimum(1)

        #self.node_size_slider.setMaximum(10)
        #self.node_size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        #self.node_size_slider.setTickInterval(3)


        #QLabel to show current slider size selection
        self.node_size_value_label = QLabel("Valor Máximo Posible: 0")

        conceptual_network_widget_horizontal_inside_size_layout.addWidget(node_size_label)
        conceptual_network_widget_horizontal_inside_size_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        conceptual_network_widget_horizontal_inside_size_layout.addWidget(self.NodeSize_txb)
        conceptual_network_widget_horizontal_inside_size_layout.addWidget(self.node_size_value_label)


        #Node grade Selection Layout

        conceptual_network_widget_horizontal_inside_grade_layout = QHBoxLayout()
        node_grade_label = QLabel("Nodos con Grado Mayor A:")
        node_grade_label.setStyleSheet(label_style_title)

        # Text box to get the node grade
        self.NodeGrade_txb = QLineEdit()
        self.NodeGrade_txb.setStyleSheet(input_txt_style)

        # self.node_grade_slider = QSlider(Qt.Orientation.Horizontal, self)
        # self.node_grade_slider.setGeometry(50, 50, 200, 50)
        # self.node_grade_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        # self.node_grade_slider.setMinimum(1)
        #
        # self.node_grade_slider.setMaximum(10)
        # self.node_grade_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        # self.node_grade_slider.setTickInterval(3)

        self.node_grade_value_label = QLabel("Valor Máximo Posible: 0")

        conceptual_network_widget_horizontal_inside_grade_layout.addWidget(node_grade_label)
        conceptual_network_widget_horizontal_inside_grade_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        conceptual_network_widget_horizontal_inside_grade_layout.addWidget(self.NodeGrade_txb)
        conceptual_network_widget_horizontal_inside_grade_layout.addWidget(self.node_grade_value_label)

        # Node Relation Selection Layout
        conceptual_network_widget_horizontal_inside_edge_weight_layout = QHBoxLayout()
        edge_weight_label = QLabel("Nodos Con Relaciones Mayores A:")
        edge_weight_label.setStyleSheet(label_style_title)

        # Text box to get the node grade
        self.EdgeWeight_txb = QLineEdit()
        self.EdgeWeight_txb.setStyleSheet(input_txt_style)

        # self.edge_weight_slider = QSlider(Qt.Orientation.Horizontal, self)
        # self.edge_weight_slider.setGeometry(50, 50, 200, 50)
        # self.edge_weight_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        #
        # self.edge_weight_slider.setMinimum(1)
        # self.edge_weight_slider.setMaximum(10)
        # self.edge_weight_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        # self.edge_weight_slider.setTickInterval(3)

        # Crear un QLabel para mostrar el valor del slider
        self.edge_weight_label = QLabel("Valor Máximo Posible: 0")

        conceptual_network_widget_horizontal_inside_edge_weight_layout.addWidget(edge_weight_label)
        conceptual_network_widget_horizontal_inside_edge_weight_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        conceptual_network_widget_horizontal_inside_edge_weight_layout.addWidget(self.EdgeWeight_txb)
        conceptual_network_widget_horizontal_inside_edge_weight_layout.addWidget(self.edge_weight_label)

        # self.node_size_slider.valueChanged.connect(self.displaySlidervalueNodeSize)
        # self.edge_weight_slider.valueChanged.connect(self.displaySlidervalueEdgeWeight)
        # self.node_grade_slider.valueChanged.connect(self.displaySlidervalueNodeGrade)

        #No Words Config

        conceptual_network_widget_horizontal_inside_no_words_layout = QHBoxLayout()
        no_words_network_graph_Label = QLabel("No Mostrar Palabras")
        no_words_network_graph_Label.setStyleSheet(label_style_title)
        self.no_words_network_graph_Checkbox = QCheckBox()
        self.no_words_network_graph_Checkbox.setStyleSheet(checkbox_style)
        conceptual_network_widget_horizontal_inside_no_words_layout.addWidget(no_words_network_graph_Label)
        conceptual_network_widget_horizontal_inside_no_words_layout.addWidget(self.no_words_network_graph_Checkbox)

        #Color Edges For Graph

        graph_color_frame_widget = QWidget()
        conceptual_network_widget_horizontal_inside_graph_color_layout = QHBoxLayout()
        conceptual_network_widget_horizontal_inside_graph_color_layout.addWidget(graph_color_frame_widget)

        color_graph_Label = QLabel("Color de Nodos")
        color_graph_Label.setStyleSheet(label_style_title)
        self.graph_color_frame = QWidget()
        self.graph_color_frame.setMinimumSize(30, 30)
        self.graph_color_frame.setMaximumSize(30, 30)
        self.graph_color_frame.setStyleSheet(frame_borders_style)
        self.graph_color_frame.setContentsMargins(0, 0, 0, 0)
        conceptual_network_widget_horizontal_inside_graph_color_layout.addWidget(color_graph_Label)
        conceptual_network_widget_horizontal_inside_graph_color_layout.addWidget(self.graph_color_frame)

        graph_color_selector_button = QPushButton("")
        graph_color_selector_button.setToolTip("Color de Nodo")
        graph_color_selector_button.setIcon(QIcon(resource_path("Icons/angulo-pequeno-hacia-abajo.png")))
        graph_color_selector_button.setStyleSheet(button_style_selection)
        graph_color_selector_button.setMaximumSize(50, 30)
        graph_color_selector_button.setContentsMargins(0, 0, 0, 0)
        graph_color_selector_button.clicked.connect(self.changeNodePalette)
        conceptual_network_widget_horizontal_inside_graph_color_layout.addWidget(graph_color_selector_button)
        #color_selecctor_layout.addWidget(color_frame2_widget)

        # Color Nodes For Graph

        graph_nodes_color_frame_widget = QWidget()
        conceptual_network_widget_horizontal_inside_graph_node_color_layout = QHBoxLayout()
        conceptual_network_widget_horizontal_inside_graph_node_color_layout.addWidget(graph_nodes_color_frame_widget)

        color_graph_node_Label = QLabel("Color de Aristas")
        color_graph_node_Label.setStyleSheet(label_style_title)
        self.graph_color_node_frame = QWidget()
        self.graph_color_node_frame.setMinimumSize(30, 30)
        self.graph_color_node_frame.setMaximumSize(30, 30)
        self.graph_color_node_frame.setStyleSheet(frame_borders_style)
        self.graph_color_node_frame.setContentsMargins(0, 0, 0, 0)
        conceptual_network_widget_horizontal_inside_graph_node_color_layout.addWidget(color_graph_node_Label)
        conceptual_network_widget_horizontal_inside_graph_node_color_layout.addWidget(self.graph_color_node_frame)

        graph_color_node_selector_button = QPushButton("")
        graph_color_node_selector_button.setToolTip("Color de Aristas")
        graph_color_node_selector_button.setIcon(QIcon(resource_path("Icons/angulo-pequeno-hacia-abajo.png")))
        graph_color_node_selector_button.setStyleSheet(button_style_selection)
        graph_color_node_selector_button.setMaximumSize(50, 30)
        graph_color_node_selector_button.setContentsMargins(0, 0, 0, 0)
        graph_color_node_selector_button.clicked.connect(self.changeEdgePalette)
        conceptual_network_widget_horizontal_inside_graph_node_color_layout.addWidget(graph_color_node_selector_button)
        # color_selecctor_layout.addWidget(color_frame2_widget)

        # Add Tools Layout to Vertical Layout
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_relation_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_select_typeword_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_graph_distro_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_distribution_layout) #FILTROS!!! Cambiar luego

        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_size_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_edge_weight_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_grade_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_no_words_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_graph_color_layout)
        conceptual_network_widget_vertical_layout.addLayout(conceptual_network_widget_horizontal_inside_graph_node_color_layout)

        self.create_conceptual_network_button = QPushButton("Crear Red")
        self.create_conceptual_network_button.setStyleSheet(button_style_normal)
        self.create_conceptual_network_button.setIcon(QIcon(resource_path("Icons/rodillo.png")))

        conceptual_network_widget_vertical_layout.addWidget(self.create_conceptual_network_button)


        self.export_graph_button = QPushButton("Exportar Grafo a Gephi")
        self.export_graph_button.setIcon(QIcon(resource_path("Icons/descargar.png")))
        self.export_graph_button.setToolTip("Exporta el grafo")
        self.export_graph_button.setStyleSheet(button_style_warming)
        self.export_graph_button.clicked.connect(self.exportGraphToGephi)

        conceptual_network_widget_vertical_layout.addWidget(self.export_graph_button)

        conceptual_network_widget_layout.addLayout(conceptual_network_widget_vertical_layout)

        #self.graphtype_combobox.currentIndexChanged.connect(self.conceptual_network_tab_manage)




        self.conceptual_network_widget.setLayout(conceptual_network_widget_layout)
        #create_conceptual_network_button.clicked.connect(self.conceptual_network)

        self.NodeGrade_txb.setEnabled(False)
        self.EdgeWeight_txb.setEnabled(False)
        self.NodeSize_txb.setEnabled(False)

        self.create_conceptual_network_button.clicked.connect(self.drawGraph)

        # ------------------------------Conceptual Network Tab End------------------------------------------

        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        self.tab_widget.setTabEnabled(4, False)

        self.setCentralWidget(self.central_widget)

    def update_img_progress(self):
        value = self.img_progress_bar.value()
        if value >= 100:
            self.loading_timer.stop()
        else:
            self.img_progress_bar.setValue(value + 1)

    def update_img_progress2(self):
        value = self.img_progress_bar2.value()
        if value >= 100:
            self.loading_timer2.stop()
        else:
            self.img_progress_bar2.setValue(value + 1)

    # Function that adds the files to the list
    def add_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt *.docx *.pdf)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.file_list.addItems(selected_files)
            self.update_graph_button_state()

    # Function that adds the URLs to the list
    def add_url_to_list(self):
        text = self.url_txb.text()
        if text:
            self.file_list.addItem(text)
            self.url_txb.clear()
            self.update_graph_button_state()

    # Function that take the file list and send it to process
    def create_graph(self):
        self.current_page = 1
        self.progressb_widget.setVisible(True)
        self.graph_thread = GraphThread(self.file_list, self.mainController)  # Here the thread is created
        self.graph_thread.update_signal.connect(self.update_progressbar)
        self.graph_thread.error_signal.connect(self.error_report)
        self.graph_thread.finished.connect(self.graph_thread_finished)
        self.graph_thread.start()


    # Action when the thread updates the progress bar
    def update_progressbar(self, file, progress):
        self.pbar_lb.setText(file)
        self.progress_bar.setValue(int(progress))

    # Function that remove a selected element of the list
    def remove_item(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.file_list.takeItem(self.file_list.row(item))
        self.update_graph_button_state()

    # Function that handle the select element event
    def update_remove_button(self):
        selected_items = self.file_list.selectedItems()
        self.remove_button.setEnabled(len(selected_items) > 0)

    def update_graph_button_state(self):
        if self.file_list.count() > 0:
            self.create_graph_btn.setEnabled(True)
        else:
            self.create_graph_btn.setEnabled(False)

    # Action when the thread finishes its job
    def graph_thread_finished(self):
        self.word_freq_dict = self.mainController.getStatistics()
        self.open_text_file()
        self.populate_table()
        self.fill_cites_list()
        # self.plot_bar_chart(word_freq_dict)
        self.tab_widget.setTabEnabled(1, True)
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setTabEnabled(3, True)
        self.tab_widget.setTabEnabled(4, True)
        alert = QMessageBox()
        alert.setWindowTitle("Proceso Terminado")
        alert.setText("¡Proceso Terminado!")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()
        self.pbar_lb.setText("Empezando Proceso")
        self.progress_bar.setValue(0)
        self.progressb_widget.setVisible(False)

    #  Function to manage the process files errors
    def error_report(self, error_message):
        alert = QMessageBox()
        alert.setWindowTitle("ERROR!")
        alert.setText(f"{error_message}")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()

    # Function that shows the dialog window, this window is to manage the ignore words in the files
    def open_dialog(self):
        self.ignore_words_dialog.show()

    # Dialog that shows information about the program
    def show_about_dialog(self):
        about_message_box = QMessageBox()
        about_message_box.setWindowTitle("Acerca de la Aplicación")
        about_message_box.setIcon(QMessageBox.Icon.Information)
        about_message_box.setText("Aplicación Creadora de Redes Conceptuales")
        about_message_box.setDetailedText(
            "Versión 1.0.1\n"
            "Conceptual Networks es un programa para la composición de redes conceptuales y su representación gráfica\n"
            "Fecha de Lanzamiento: 14 Setiembre, 2023\n"
            "TEC  | Instituto Tecnológico De Costa Rica\n"
            "UNED | Universidad Estatal a Distancia\n"
            "LIIT | Laboratorio de Investigación e Innovación Tecnológica\n"
            "Desarrollado por: Jose Arce Morales, Gerson Gorgona Vargas, Josué Barrientos Sandoval, Álvaro Moreira Villalobos, Ronaldo Vindas Barboza\n"
            "Agradecimientos:\n Rodolfo Mora Zamora - Profesor y Supervisor \n Adriana López Vindas - Supervisora"
        )
        about_message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        about_message_box.exec()

    # Function that input a map of words and frequency to introduce in the table
    def populate_table(self):
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        data_to_display = list(self.word_freq_dict.getStemWords().items())[start:end]
        self.table_info_widget.setRowCount(0)

        for i, (word, value) in enumerate(data_to_display):
            item_word = QTableWidgetItem(word)
            item_freq = QTableWidgetItem(str(value[1]))
            words = ", ".join(value[0].keys())
            words_item = QTableWidgetItem(words)
            item_percent = QTableWidgetItem(f"{(value[1] / self.word_freq_dict.count_words) * 100:.2f}%")

            self.table_info_widget.insertRow(i)
            self.table_info_widget.setItem(i, 0, item_word)
            self.table_info_widget.setItem(i, 1, words_item)
            self.table_info_widget.setItem(i, 2, item_freq)
            self.table_info_widget.setItem(i, 3, item_percent)

        self.setup_pagination()

    def export_table(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("CSV (*.csv)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                with open(file_path, mode='w', newline='') as archivo_csv:
                    try:
                        # Crear un objeto escritor CSV
                        writer_csv = csv.DictWriter(archivo_csv, fieldnames=['Raíz', 'Frecuencia'])
                        # Escribir la fila de encabezados (nombres de las columnas)
                        writer_csv.writeheader()
                        # Escribir los datos del diccionario como filas en el archivo CSV
                        for key, value in self.word_freq_dict.getStemWords().items():
                            row = {
                                'Raíz': key,
                                'Frecuencia': value[1]
                            }
                            writer_csv.writerow(row)
                    except Exception as e:
                        print(e)

            alert = QMessageBox()
            alert.setWindowTitle("Alerta")
            alert.setText("¡Tabla Exportada!")
            alert.setIcon(QMessageBox.Icon.Information)
            alert.exec()

    # Function that set up the information of the pages
    def setup_pagination(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1

        self.tpg_number_input.setValue(self.current_page)
        self.pageLabel2.setText(f" de {total_pages}")
        self.prevButton.setEnabled(self.current_page > 1)
        self.nextButton.setEnabled(self.current_page < total_pages)

    # Move to the previous page
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            # self.setup_pagination()

    # Move to the next page
    def next_page(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_table()
            # self.setup_pagination()

    # Validate the page number of the number input
    def validate_table_nav_text(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1
        current_page = self.tpg_number_input.value()
        if current_page <= total_pages:
            self.current_page = current_page
            self.populate_table()
        else:
            self.tpg_number_input.setValue(self.current_page)

    # Add the selected item of the table to the list of roots
    def add_item_to_root_list(self):
        selected_item = self.table_info_widget.currentItem()
        selected_column = self.table_info_widget.currentColumn()
        items = [self.root_list_list.item(i).text() for i in range(self.root_list_list.count())]
        if selected_column == 0:
            if selected_item:
                text = selected_item.text()
                if text not in items:
                    self.root_list_list.addItem(text)

    # Delete the selected item of the list of roots
    def remove_item_from_root_list(self):
        selected_item = self.root_list_list.currentItem()
        if selected_item:
            self.root_list_list.takeItem(self.root_list_list.row(selected_item))

    # Update the root remove botton
    def update_root_remove_button(self):
        selected_items = self.root_list_list.selectedItems()
        self.remove_root_button.setEnabled(len(selected_items) > 0)

    def combine_roots(self):
        items = []
        filecount = self.root_list_list.count()
        for i in range(filecount):
            items.append(self.root_list_list.item(i).text())
        try:
            self.mainController.combine_roots(items)
        except Exception as e:
            alert = QMessageBox()
            alert.setWindowTitle("Alerta")
            alert.setText(f"¡Warming! la raiz {e} se agrego mas de una vez \n Puede que ocurriera un error al combinarlas")
            alert.setIcon(QMessageBox.Icon.Information)
            alert.exec()
            self.root_list_list.clear()
            self.populate_table()
        alert = QMessageBox()
        alert.setWindowTitle("Alerta")
        alert.setText("¡Palabras Combinadas!")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()
        self.root_list_list.clear()
        self.populate_table()

    # Color Palette dialog
    def changePalette(self):
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("Colores de la Nube")
        current_color = self.color_frame.palette().color(QPalette.ColorRole.Window)
        color_dialog.setCurrentColor(current_color)

        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            self.update_color(selected_color)

    def update_color(self, color):
        palette = self.color_frame.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.color_frame.setAutoFillBackground(True)
        self.color_frame.setPalette(palette)
        self.cloudParameters['color'] = color.getRgb()[:-1]

    def changeBGPalette(self):
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("Colores del Fondo Nube")
        current_color = self.color_frame2.palette().color(QPalette.ColorRole.Window)
        color_dialog.setCurrentColor(current_color)

        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            self.update_BGcolor(selected_color)


    def update_BGcolor(self, color):
        palette = self.color_frame2.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.color_frame2.setAutoFillBackground(True)
        self.color_frame2.setPalette(palette)
        self.cloudParameters['background_color'] = color.getRgb()[:-1]

    # Function to generate the word in the word cloud function randomly
    def random_color(self, word, font_size, position, orientation, random_state=None, **kwargs):
        if self.random_colors_chkbox.isChecked():
            return f"rgb({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})"

        else:
            return f"rgb{self.cloudParameters['color']}"

    # To convert the background of the cloud transparent

    def transparent_background(self):
        if self.transparent_colors_chkbox.isChecked():
            return None

        else:
            return self.cloudParameters['background_color']




    # Generate a concept cloud
    def generate_word_cloud(self):
        self.create_word_cloud_button.setEnabled(False)
        wordcloud_params = {
            'font_path': self.fonts[self.cloudParameters['font']],
            'width': self.cloudParameters['width'],
            'height': self.cloudParameters['height'],
            'background_color': self.transparent_background(),
            'mask': self.cloudParameters['mask'],
            'mode': 'RGBA',
            'color_func': self.random_color,
        }
        plt.close(plt.figure(1))
        dpi = 160
        figsize = (wordcloud_params['width'] / dpi, wordcloud_params['height'] / dpi)
        plt.figure(1,figsize=figsize, dpi=dpi)
        self.cloud_thread = CloudThread(wordcloud_params, self.mainController, self.num_func_words)  # Here the thread is created
        self.cloud_thread.finished.connect(self.cloud_thread_finish)
        self.cloud_thread.start()
        self.image_progress_bar.setVisible(True)
        self.loading_timer.start(50)
        # self.svg_image.setPixmap(QPixmap(resource_path("wordcloud.png")))

    def cloud_thread_finish(self):
        self.loading_timer.stop()
        self.image_progress_bar.setVisible(False)
        wordcloud_path = os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks'))
        self.load_image(wordcloud_path + "/wordcloud.png")
        self.create_word_cloud_button.setEnabled(True)

    # Load the image to the scene
    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.scene.clear()

        # Agregar la imagen a la escena como QGraphicsPixmapItem
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(pixmap_item)

        # Configurar la vista para permitir el arrastre de la imagen
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.info_label.setText(f"Dimensiones: {pixmap.width()}x{pixmap.height()}")

    # Export the png to a selected location
    def exportwordcloud(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("PNG (*.png);;JPEG (*.jpg);;SVG (*.svg)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]

                # Export the image to the selected format using matplotlib
                plt.figure(1).savefig(file_path, bbox_inches='tight', pad_inches=0, transparent=True)

            alert = QMessageBox()
            alert.setWindowTitle("Alerta")
            alert.setText("¡Imagen Guardada!")
            alert.setIcon(QMessageBox.Icon.Information)
            alert.exec()

    # Filter of the table
    def onFilterComboBoxActivated(self):
        selected_index = self.filterComboBox.currentIndex()
        if selected_index == 0:
            self.mainController.alphabeticSort()
        else:
            self.mainController.weigthSort()
        self.populate_table()

    # Conceptual network manage
    def conceptual_network(self, show_lables=1, type_graph=1, nodeSize=50, edgeWeight=550, nodeGrade = 1, relation=1, type_word = 1, node_color = 0, edge_color = 0):
        '''print(
            "par1 : " + str(show_lables) +
            " par2 : " + str(type_graph) +
            " par3 : " + str(nodeSize) +
            " par4 : " + str(edgeWeight) +
            " par5 : " + str(nodeGrade) +
            " par6 : " + str(relation)
        )'''
        try:
            plt.close(plt.figure(2))
            plt.figure(2)
            self.network_thread = NetworkThread(self.mainController, show_lables, type_graph, nodeSize, edgeWeight, nodeGrade, relation, type_word, node_color, edge_color)
            self.network_thread.finished.connect(self.network_thread_finish)
            self.network_thread.start()
        except Exception as e:
            print(e)


    def network_thread_finish(self):
        self.loading_timer2.stop()
        self.image_progress_bar2.setVisible(False)
        alert = QMessageBox()
        alert.setWindowTitle("Proceso Terminado")
        alert.setText("¡Proceso Terminado!")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()
        self.create_conceptual_network_button.setEnabled(True)
        self.mainController.delete_graph()
        plt.figure(2).show()


    # Fill the font combo box with the system fonts
    def fill_font_combobox(self):
        font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        for font_path in font_list:
            font_properties = matplotlib.font_manager.FontProperties(fname=font_path)
            self.fonts[font_properties.get_name()] = font_path
            self.font_combobox.addItem(font_properties.get_name())
        self.cloudParameters['font'] = self.font_combobox.currentText()

    # Combobox functions
    def onFontComboboxActivated(self):
        currentFont = self.font_combobox.currentText()
        self.cloudParameters['font'] = currentFont

    def onFuncWordComboboxActivated(self):
        currentI = self.word_func_combobox.currentIndex()
        self.num_func_words = currentI

    def onZiseComboboxActivivated(self):
        currentText = self.shapeComboBox.currentText()
        sizes = currentText.split('x')
        self.cloudParameters['width'] = int(sizes[0])
        self.cloudParameters['height'] = int(sizes[1])

    # Open a dialog to choose an image to use like a mask in the creation of the concept cloud
    def selectMask(self):
        file_dialog_mask = QFileDialog()
        file_dialog_mask.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog_mask.setNameFilter("Text files (*.png *.jpg *.jpeg)")
        if file_dialog_mask.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog_mask.selectedFiles()[0]
            shape_img_label_icon = QIcon(resource_path(selected_files))
            self.shape_img_label.setPixmap(shape_img_label_icon.pixmap(50, 50))
            self.cloudParameters['mask'] = np.array(Image.open(resource_path(selected_files)))

    def deleteselectMask(self):
        shape_img_label_icon = QIcon(resource_path("Icons/imagen-de-archivo.png"))
        self.shape_img_label.setPixmap(shape_img_label_icon.pixmap(50, 50))
        self.cloudParameters['mask'] = None

    # Control the zoom of the word cloud visualizer
    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    def zoom_out(self):
        self.view.scale(1 / 1.2, 1 / 1.2)

    def network_relations_checkbok_manage(self):
        self.general_network_graph_Checkbox.setChecked(False)
        self.weight_network_graph_Checkbox.setChecked(False)
        self.size_network_graph_Checkbox.setChecked(False)
        self.grade_network_graph_Checkbox.setChecked(False)

    def displaySlidervalueNodeSize(self, value):
        self.node_size_value_label.setText(f"Valor: {value}")
        # self.node_size_value_label.adjustSize()            # Ajusta el tamaño del label de acuerdo al tamaño del numero

    def displaySlidervalueEdgeWeight(self, value):
        self.edge_weight_label.setText(f"Valor: {value}")

    def displaySlidervalueNodeGrade(self, value):
        self.node_grade_value_label.setText(f"Valor: {value}")

    def network_checkbox_management(self, state):
        if state == 2:  # Si se marca un QCheckBox
            self.mainController.set_network_data()
            self.mainController.create_network()
            relation_selection = int(self.relation_combobox.currentText())
            self.mainController.create_relation(relation_selection)

            if not self.filter_network_graph_Checkbox.isChecked():  # General Seleccionado
                self.filter_network_graph_Checkbox.setEnabled(False)

                self.NodeSize_txb.setText("")
                self.NodeGrade_txb.setText("")
                self.EdgeWeight_txb.setText("")

                self.NodeSize_txb.setEnabled(False)
                self.NodeGrade_txb.setEnabled(False)
                self.EdgeWeight_txb.setEnabled(False)



                #self.node_size_slider.setEnabled(False)
                #self.edge_weight_slider.setEnabled(False)
                #self.node_grade_slider.setEnabled(False)

                #self.size_network_graph_Checkbox.setEnabled(True)
                #self.grade_network_graph_Checkbox.setEnabled(True)

            elif self.filter_network_graph_Checkbox.isChecked():  # Filtro
                try:
                    #self.general_network_graph_Checkbox.setEnabled(False)

                    self.node_size_value_label.setText("Valor Máximo Posible: " + str(int(self.mainController.get_weight_of_heaviest_node())))
                    self.NodeSize_txb.setEnabled(True)

                    self.edge_weight_label.setText("Valor Máximo Posible: " + str(int(self.mainController.get_weight_of_heaviest_edge())))
                    self.EdgeWeight_txb.setEnabled(True)

                    self.node_grade_value_label.setText("Valor Máximo Posible: " + str(int(self.mainController.get_weight_of_heaviest_grade())))

                    self.NodeGrade_txb.setEnabled(True)

                    self.mainController.delete_graph()

                    #self.node_size_slider.setEnabled(True)
                    #self.edge_weight_slider.setEnabled(False)
                    #self.node_grade_slider.setEnabled(False)

                except Exception as e:
                        print(e)

        else:  # Si se desmarca un QCheckBox
            #self.general_network_graph_Checkbox.setEnabled(True)
            self.filter_network_graph_Checkbox.setEnabled(True)

            try:
                self.mainController.delete_graph()
            except Exception as e:
                print(e)

    def exportGraphToGephi(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("GEPHI (*.gexf)")

        file_path = ''
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                print(file_path)
                self.mainController.set_network_data()
                self.mainController.create_network()
                relation_selection = int(self.relation_combobox.currentText())
                self.mainController.create_relation(relation_selection)
                type_word_selection = (self.typeword_combobox.currentIndex()) + 1
                graph = self.mainController.get_graph(type_word_selection)
                nx.write_gexf(graph, file_path)

            alert = QMessageBox()
            alert.setWindowTitle("Alerta")
            alert.setText("¡Grafo Exportado!")
            alert.setIcon(QMessageBox.Icon.Information)
            alert.exec()



    def drawGraph(self):
        self.image_progress_bar2.setVisible(True)
        self.loading_timer2.start(50)

        self.create_conceptual_network_button.setEnabled(False)
        relation_selection = self.relation_combobox.currentText()
        type_word_selection = (self.typeword_combobox.currentIndex()) + 1
        graph_distro_selection = self.graph_distro_combobox.currentIndex()
        #print("GOKU3"+ str(graph_distro_selection))
        no_words_flag = "null"
        #distribution_selection = "null"
        node_size_selection = 0
        edge_weight_selection = 0
        node_grade_selection = 0
        #print("111")

        if self.no_words_network_graph_Checkbox.isChecked():
            no_words_flag = 1
        else:
            no_words_flag = 0

        if not self.filter_network_graph_Checkbox.isChecked():  # Filtro No Seleccionado
            #distribution_selection = 1
            try:
                self.mainController.delete_graph()
                self.conceptual_network(int(no_words_flag), graph_distro_selection, 0, 0, 0, int(relation_selection), type_word_selection, self.graphcolor, self.nodeColor)
            except Exception as e:
                print(e)
        elif self.filter_network_graph_Checkbox.isChecked():  # Filtro Seleccionado
            print("222")
            try:
                # distribution_selection = 2
                node_size_selection = int(self.NodeSize_txb.text())
                edge_weight_selection = int(self.EdgeWeight_txb.text())
                node_grade_selection = int(self.NodeGrade_txb.text())

                if node_size_selection < 0 or edge_weight_selection < 0 or node_grade_selection < 0 or str(node_size_selection) == '' or str(edge_weight_selection) == '' or str(node_grade_selection) == '':
                    self.error_report("Parámetros no pueden ser menores a 0.")
                else:
                    self.mainController.delete_graph()
                    self.conceptual_network(int(no_words_flag), 1, node_size_selection, edge_weight_selection, node_grade_selection, int(relation_selection), type_word_selection,  self.graphcolor, self.nodeColor)
            except Exception as e:
                print(e)

    ##########################################################################################################
    def changeNodePalette(self):
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("Colores de Grafo")
        current_color = self.graph_color_frame.palette().color(QPalette.ColorRole.Window)
        color_dialog.setCurrentColor(current_color)

        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            self.update_node_color(selected_color)

    def update_node_color(self, color):
        palette = self.graph_color_frame.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.graph_color_frame.setAutoFillBackground(True)
        self.graph_color_frame.setPalette(palette)
        self.graphcolor = color.name()
        print("GOKUUUUU" + str(self.graphcolor))

    def changeEdgePalette(self):
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("Colores de Nodo")
        current_color = self.graph_color_node_frame.palette().color(QPalette.ColorRole.Window)
        color_dialog.setCurrentColor(current_color)

        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            self.update_edge_color(selected_color)

    def update_edge_color(self, color):
        palette = self.graph_color_node_frame.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.graph_color_node_frame.setAutoFillBackground(True)
        self.graph_color_node_frame.setPalette(palette)
        self.nodeColor = color.name()
        print("GOKUUUUU2" + str(self.nodeColor))



    ##########################################################################################################

    def open_text_file(self):
        try:
            self.text_browser.setPlainText(self.mainController.get_text2())
        except Exception as e:
            self.text_browser.setPlainText("Error al abrir el archivo:\n" + str(e))

    def search_text(self):
        keyword = self.search_input.text()
        if keyword:
            # Obtener el documento del QTextBrowser
            doc = self.text_browser.document()

            # Crear un QTextCursor para el documento completo
            cursor = QTextCursor(doc)

            # Establecer el formato de selección vacía para eliminar cualquier resaltado anterior
            format = QTextCharFormat()
            format.setBackground(Qt.GlobalColor.white)  # Fondo blanco para desmarcar
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(format)

            # Luego, realizar la nueva búsqueda
            cursor = doc.find(keyword)
            while not cursor.isNull():
                format = QTextCharFormat()
                format.setBackground(Qt.GlobalColor.yellow)  # Fondo amarillo para resaltar
                cursor.mergeCharFormat(format)
                cursor = doc.find(keyword, cursor)

    def on_double_click_cites_list_item(self, item):
        keyword = item.text()
        if keyword:
            # Obtener el documento del QTextBrowser
            doc = self.text_browser.document()

            # Crear un QTextCursor para el documento completo
            cursor = QTextCursor(doc)

            # Establecer el formato de selección vacía para eliminar cualquier resaltado anterior
            format = QTextCharFormat()
            format.setBackground(Qt.GlobalColor.white)  # Fondo blanco para desmarcar
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(format)

            # Luego, realizar la nueva búsqueda
            cursor = doc.find(keyword)
            if not cursor.isNull():
                format = QTextCharFormat()
                format.setBackground(Qt.GlobalColor.yellow)  # Fondo amarillo para resaltar
                cursor.mergeCharFormat(format)
                self.text_browser.setTextCursor(cursor)

                # Asegurarse de que el texto encontrado sea visible en la vista
                self.text_browser.ensureCursorVisible()


    def fill_cites_list(self):
        self.cites_qlist.clear()
        cites = self.mainController.get_phrases()
        webs = self.mainController.get_web_pages()
        cites.extend(webs)
        for i in cites:
            self.cites_qlist.addItem(i)



app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
