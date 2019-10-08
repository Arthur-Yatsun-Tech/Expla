from PySide2.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout


class Groups:
    def __init__(self, main_window):
        self.main_window = main_window

    def create_top_left_group_box(self):
        number_of_experiments_label = QLabel("Введите коло-во серий экспериментов")
        number_of_factors_label = QLabel("Введите коло-во факторов")

        layout_1 = QVBoxLayout()
        layout_1.addWidget(number_of_factors_label)
        layout_1.addWidget(number_of_experiments_label)

        layout_2 = QVBoxLayout()
        layout_2.addWidget(self.main_window.number_of_factors)
        layout_2.addWidget(self.main_window.number_of_experiments)

        layout = QHBoxLayout()
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)

        self.main_window.top_left_group.setLayout(layout)

    def create_top_right_group_box(self):
        levels_label = QLabel('Введите коло-во уровней')

        radio_group_layout = QHBoxLayout()
        radio_group_layout.addWidget(self.main_window.level_2)
        radio_group_layout.addWidget(self.main_window.level_3)
        radio_group_layout.addWidget(self.main_window.level_5)

        layout = QVBoxLayout()
        layout.addWidget(levels_label)
        layout.addLayout(radio_group_layout)

        self.main_window.top_right_group.setLayout(layout)

    def create_bottom_left_group_box(self):
        self.main_window.columns[0].addWidget(QLabel(''))
        self.main_window.columns[0].addWidget(QLabel('x'))
        self.main_window.columns[0].addWidget(QLabel('d1'))
        self.main_window.column0_d2_label = QLabel('d2')
        self.main_window.columns[0].addWidget(self.main_window.column0_d2_label)

        [self.main_window._add_widgets_into_column(
                self.main_window.columns[column],
                f'{column}',
                self.main_window.rows_edit_x[column - 1],
                self.main_window.rows_edit_d1[column - 1],
                self.main_window.rows_edit_d2[column - 1]
            ) for column in range(1, 10)
        ]
        [self.main_window.bottom_left_layout.addLayout(self.main_window.columns[column]) for column in range(10)]

        self.main_window.bottom_left_group.setLayout(self.main_window.bottom_left_layout)

    def create_bottom_right_group_box(self):
        self.main_window.import_table_button.setEnabled(False)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.main_window.import_table_button)
        layout1.addWidget(self.main_window.export_table_button)

        layout = QVBoxLayout()
        layout.addWidget(self.main_window.open_table_button)
        layout.addLayout(layout1)

        self.main_window.bottom_right_group.setLayout(layout)