from PyQt6.QtWidgets import *
from gui import *
from random import *


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # these are not the defaults. Defaults are 10, 10, and 13
        self.rows = 1
        self.cols = 1
        self.bombs = 1
        self.board = [[]]
        self.board_nums = []
        self.set_button(0, 0)
        self.generate_board()
        self.button_gen.clicked.connect(lambda: self.generate_board())





    def set_button(self, row, col):
        # This shit creates a button widget at space (row, col) in the grid layout. Also saves button to .board 2d
        # list for future fuckery
        self.button = QtWidgets.QPushButton(parent=self.frame_game)
        self.button.setMaximumSize(QtCore.QSize(40, 40))
        self.button.setMinimumSize(QtCore.QSize(40, 40))
        self.button.setObjectName(f"button{row}_{col}")
        self.gridLayout.addWidget(self.button, row, col)
        self.board[row].append(self.button)
        self.button.clicked.connect(lambda: self.button_pressed(self.board[row][col]))






    def button_pressed(self, space):
        # This shit is retarded
        if self.radio_flag.isChecked():
            self.flag(space)
        elif self.radio_click.isChecked():
            self.sweep(space)


    def sweep(self, space):
        """
        Todo: If a space is clicked, and it's not a bomb, disable it with .setEnabled(False) and change its text to the number in board_nums.

        Todo: If it is a bomb, disable all spaces and change the bomb spaces text to an X. I'll find a bomb image later.

        Todo: If a space is flagged, do nothing
        """
        clicked_button = self.sender()

        row, col = self.get_button_position(space)

        if self.board_nums[row][col] == 'F':
            return
        
        if self.board_nums[row][col] == 'x':
            for row in self.board:
                for button in row:
                    button.setEnabled(False)
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board_nums[row][col] == 'x':
                        self.board[row][col].setText('x')
        else:
            space.setEnabled(False)
            num = self.board_nums[row][col]
            if num > 0:
                space.setText(str(num))
    
    def get_button_position(self, button):
        pos = self.gridLayout.getItemPosition(self.gridLayout.indexOf(button))
        return pos[0], pos[1]



    def flag(self, space):
        """
        Todo: Make it so you can flag and un-flag a space. For now just change the space text to 'F'. I'll get a flag image later
        """
        space.setText('F')


    def generate_board(self):
        # This shit uses temp vars to see if the inputs are ints that are > 1. If they are it clears the board list,
        # destroys all the button widgets in the frame_game frame, and creates a new board with .set_button()
        try:
            temp_r = int(self.input_row.text())
            temp_c = int(self.input_col.text())
            temp_b = int(self.input_bomb.text())
            if temp_r < 1 or temp_c < 1 or temp_b < 1:
                raise TypeError

            for row in range(self.rows):

                for col in range(self.cols):
                    self.board[row][col].setParent(None)
            self.board.clear()
            self.board_nums.clear()

            self.rows = temp_r
            self.cols = temp_c
            self.bombs = temp_b

            for row in range(self.rows):
                self.board.append([])
                self.board_nums.append([])

                for col in range(self.cols):
                    self.set_button(row, col)
                    self.board_nums[row].append(0)

            # This shit is bomb creation
            for i in range(self.bombs):
                rand_row = randint(0, self.rows - 1)
                rand_col = randint(0, self.cols - 1)
                while self.board_nums[rand_row][rand_col] == 'x':
                    rand_row = randint(0, self.rows - 1)
                    rand_col = randint(0, self.cols - 1)

                self.board_nums[rand_row][rand_col] = 'x'
                # This shit is temp
                self.board[rand_row][rand_col].setIcon(QtGui.QIcon('Dizzy Face Emoji.png'))




            self.input_row.setText('')
            self.input_col.setText('')
            self.input_bomb.setText('')
            self.generate_nums()
            self.hide_numbers()


        except ValueError:
            # This shit is temp
            self.button_gen.setText('XXX')

        except TypeError:
            # This too
            self.button_gen.setText('OOO')

    def hide_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].setText('')


    def generate_nums(self):
        """
        Todo: This shit should generate the numbers. Make a double for loop to cycle through every space in board_nums.
        Should look like this:          x 0 x
                                        0 # 0 = 3
                                        x 0 0
        If the space in the middle is an x then just continue.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board_nums[row][col] != 'x':
                    num_bombs = self.count_neighboring_bombs(row, col)
                    self.board_nums[row][col] = num_bombs

        self.update_button_texts()


    def count_neighboring_bombs(self, row, col):
    #THis shit was toxic bitch
        bomb_count = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j

                #Checks the neighboring space to see if its within the board boundaries
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    if self.board_nums[new_row][new_col] == 'x':
                        bomb_count += 1

        return bomb_count

    def update_button_texts(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].setText(str(self.board_nums[row][col]))
