#
import sys
#
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
#
import Globals as glb


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setTabStopWidth(40)  # half of original / 4 spaces now
        self.init_actions()
        self.init_menubar()
        self.init_toolbar()
        self.init_formatbar()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.setGeometry(150, 150, 700, 600)
        self.setWindowTitle('My Editor')
        self.setWindowIcon(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'icon.png'))
        self.show()


    def test(self):
        cursor = self.textEdit.textCursor()
        textblockformat = cursor.blockFormat()
        textblockformat.setAlignment(QtCore.Qt.AlignRight)
        cursor.mergeBlockFormat(textblockformat)
        self.textEdit.setTextCursor(cursor)

    def init_actions(self):
        #file

        self.newfile = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'new.png'),'New File', self)
        self.newfile.setShortcut('Ctrl+N')
        self.newfile.setStatusTip('Create a new file')
        self.newfile.triggered.connect(self.new_file_action)

        self.openfile = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'open.png'), 'Open a file', self)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip('Open a new file')
        self.openfile.triggered.connect(self.open_file_action)

        self.savefile = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'save.png'), 'Save file', self)
        self.savefile.setShortcut('Ctrl+S')
        self.savefile.setStatusTip('Save the file')
        self.savefile.triggered.connect(self.save_file_action)

        self.printfile = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'print.png'),'Print the file', self)
        self.printfile.setShortcut('Ctrl+P')
        self.printfile.setStatusTip('Print the file')
        self.printfile.triggered.connect(self.print_file_action)

        self.quitfile = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'exit.png'),'Exit', self)
        self.quitfile.setShortcut('Esc')
        self.quitfile.setStatusTip('Quit the application')
        self.quitfile.triggered.connect(self.closeEvent)

        # edit
        self.undo = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'undo.png'),'Undo', self)
        self.undo.setShortcut('Ctrl+Z')
        self.undo.setStatusTip('Undo the last action')
        self.undo.triggered.connect(self.textEdit.undo)

        self.redo = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'redo.png'),'Redo', self)
        self.redo.setShortcut('Ctrl+Y')
        self.redo.setStatusTip('Redo the last action')
        self.redo.triggered.connect(self.textEdit.redo)

        self.cut = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'cut.png'),'Cut', self)
        self.cut.setShortcut('Ctrl+X')
        self.cut.setStatusTip('Cut the text to the clipboard')
        self.cut.triggered.connect(self.textEdit.cut)

        self.copy = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'copy.png'),'Copy', self)
        self.copy.setShortcut('Ctrl+C')
        self.copy.setShortcut('Copy the text to the clipboard')
        self.copy.triggered.connect(self.textEdit.copy)

        self.paste = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'paste.png'),'Paste', self)
        self.paste.setShortcut('Ctrl+V')
        self.paste.setStatusTip('Paste the text from the clipboard')
        self.paste.triggered.connect(self.textEdit.paste)

        # format

        self.changefont = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'font.png'), 'Change Font', self)
        self.changefont.setStatusTip('Change the font')
        self.changefont.triggered.connect(self.change_font_action)

        # bold

        self.bold = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'bold.png'), 'Bold the text', self)
        self.bold.setShortcut('Ctrl+B')
        self.bold.setStatusTip('Bold the text')
        self.bold.setCheckable(True)

        self.bold.triggered[bool].connect(self.bold_text_action)

        # italic

        self.italic = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'italic.png'), 'Italic the text', self)
        self.italic.setShortcut('Ctrl+I')
        self.italic.setStatusTip('Italic the text')
        self.italic.setCheckable(True)

        self.italic.triggered[bool].connect(self.italic_text_action)

        # underline

        self.underline = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'underline.png'), 'Italic the text', self)
        self.underline.setShortcut('Ctrl+U')
        self.underline.setStatusTip('Underline the text')
        self.underline.setCheckable(True)

        self.underline.triggered[bool].connect(self.underline_text_action)

        # align left

        self.align_left = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'align_left.png'), 'Align left the text', self)
        self.align_left.setShortcut('Ctrl+L')
        self.align_left.setStatusTip('Align left the text')
        self.align_left.setCheckable(True)

        self.align_left.triggered[bool].connect(self.align_left_text_action)

        # align right

        self.align_right = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'align_right.png'), 'Align right the text', self)
        self.align_right.setShortcut('Ctrl+R')
        self.align_right.setStatusTip('Align right the text')
        self.align_right.setCheckable(True)

        self.align_right.triggered[bool].connect(self.align_right_text_action)

        # align center

        self.align_center = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'align_center.png'), 'Align center the text', self)
        self.align_center.setShortcut('Ctrl+G')
        self.align_center.setStatusTip('Align center the text')
        self.align_center.setCheckable(True)

        self.align_center.triggered[bool].connect(self.align_center_text_action)

        # ordered list

        self.ordered_list = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'ordered_list.png'), 'Insert a bullet list', self)
        self.ordered_list.setStatusTip('Make a bullet list')
        self.ordered_list.setCheckable(True)

        self.ordered_list.triggered[bool].connect(self.ordered_list_action)

        # numbered list

        self.numbered_list = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'numbered_list.png'), 'Insert a numbered list', self)
        self.numbered_list.setStatusTip('Maike a numbered list')
        self.numbered_list.setCheckable(True)

        self.numbered_list.triggered[bool].connect(self.numbered_list_action)

        # background text color

        self.text_background_color = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'text_background_color.png'), 'Set text background color', self)
        self.text_background_color.setStatusTip('Set text background color')

        self.text_background_color.triggered.connect(self.text_background_color_action)

        # text color

        self.text_color = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'text_color.png'), 'Set text color', self)
        self.text_color.setStatusTip('Set text color')

        self.text_color.triggered.connect(self.text_color_action)

        # search

        self.search = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'search.png'), 'Search the text', self)
        self.search.setStatusTip('Search the document')
        self.search.setShortcut('Ctrl+F')
        self.search.triggered.connect(self.search_action)

        # help
        self.help = QtWidgets.QAction(QtGui.QIcon(glb.TEXT_EDITOR_RESOURCES_FILEPATH + 'help.png'), 'Help', self)
        self.help.setStatusTip('Help')
        self.help.triggered.connect(self.help_action)

    def init_menubar(self):

        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('&File')
        self.file_menu.addAction(self.newfile)
        self.file_menu.addAction(self.openfile)
        self.file_menu.addAction(self.savefile)
        self.file_menu.addAction(self.printfile)
        self.file_menu.addAction(self.quitfile)

        self.edit_menu = self.menubar.addMenu('&Edit')
        self.edit_menu.addAction(self.undo)
        self.edit_menu.addAction(self.cut)
        self.edit_menu.addAction(self.copy)
        self.edit_menu.addAction(self.paste)
        self.edit_menu.addAction(self.redo)

        self.format_menu = self.menubar.addMenu('&Format')
        self.format_menu.addAction(self.changefont)

        self.help_menu = self.menubar.addMenu('&Help')
        self.help_menu.addAction(self.help)

    def init_toolbar(self):

        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(self.newfile)
        self.toolbar.addAction(self.openfile)
        self.toolbar.addAction(self.savefile)
        self.toolbar.addAction(self.printfile)
        self.toolbar.addAction(self.search)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.copy)
        self.toolbar.addAction(self.paste)
        self.toolbar.addAction(self.cut)
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.align_left)
        self.toolbar.addAction(self.align_center)
        self.toolbar.addAction(self.align_right)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.ordered_list)
        self.toolbar.addAction(self.numbered_list)

        self.addToolBarBreak()

    def init_formatbar(self):

        self.font_sizes = ['6', '7', '8', '9', '10', '11', '12', '13', '14',
                     '15', '16', '18', '20', '22', '24', '26', '28',
                     '32', '36', '40', '44', '48', '54', '60', '66',
                     '72', '80', '88', '96']

        self.formatbar = self.addToolBar('FormatBar')

        self.font_style_dropdown = QtWidgets.QFontComboBox(self)
        self.font_style_dropdown.currentFontChanged.connect(self.quick_font_action)

        self.font_size_dropdown = QtWidgets.QComboBox(self)
        self.font_size_dropdown.setEditable(True)

        for i in self.font_sizes:
            self.font_size_dropdown.addItem(i)

        self.font_size_dropdown.activated.connect(self.change_font_size_action)
        self.formatbar.addWidget(self.font_style_dropdown)
        self.formatbar.addWidget(self.font_size_dropdown)

        self.formatbar.addSeparator()

        self.formatbar.addAction(self.bold)
        self.formatbar.addAction(self.italic)
        self.formatbar.addAction(self.underline)

        self.formatbar.addSeparator()

        self.formatbar.addAction(self.text_color)
        self.formatbar.addAction(self.text_background_color)


    def new_file_action(self):

        if self.textEdit.toPlainText():
            reply = self.prompt()
            if reply == QtWidgets.QMessageBox.Yes:
                self.save_file_action()
                self.textEdit.setText('')
            elif reply == QtWidgets.QMessageBox.No or reply == QtWidgets.QMessageBox.Cancel:
                self.textEdit.setText('')

    def open_file_action(self):

        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '/home')
            with open(fname, 'r') as f:
                data = f.read()
                self.textEdit.setText(data)
        except:
            pass

    def save_file_action(self):

        try:
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '/home')
            with open(fname, 'w') as f:
                f.write(self.textEdit.toPlainText())
                f.close()
        except:
            pass

    def print_file_action(self):
        dialog = QtWidgets.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.textEdit.document().print_(dialog.printer())

    def change_font_action(self):
        font, ok = QtWidgets.QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

    def quick_font_action(self, font):
        if font:
            self.textEdit.setFont(font)

    def change_font_size_action(self, size):
        self.textEdit.setFontPointSize(int(size))

    def bold_text_action(self, pressed):

        if pressed:
            self.textEdit.setFontWeight(QtGui.QFont.Bold)
        else:
            self.textEdit.setFontWeight(QtGui.QFont.Normal)

    def italic_text_action(self, pressed):

        if pressed:
            self.textEdit.setFontItalic(True)
        else:
            self.textEdit.setFontItalic(False)

    def underline_text_action(self, pressed):

        if pressed:
            self.textEdit.setFontUnderline(True)
        else:
            self.textEdit.setFontUnderline(False)

    def align_left_text_action(self):

        cursor = self.textEdit.textCursor()
        textblockformat = cursor.blockFormat()
        textblockformat.setAlignment(QtCore.Qt.AlignLeft)
        cursor.mergeBlockFormat(textblockformat)
        self.textEdit.setTextCursor(cursor)


    def align_right_text_action(self):

        cursor = self.textEdit.textCursor()
        textblockformat = cursor.blockFormat()
        textblockformat.setAlignment(QtCore.Qt.AlignRight)
        cursor.mergeBlockFormat(textblockformat)
        self.textEdit.setTextCursor(cursor)


    def align_center_text_action(self):

        cursor = self.textEdit.textCursor()
        textblockformat = cursor.blockFormat()
        textblockformat.setAlignment(QtCore.Qt.AlignCenter)
        cursor.mergeBlockFormat(textblockformat)
        self.textEdit.setTextCursor(cursor)

    def ordered_list_action(self, pressed):

        if pressed:
            cursor = self.textEdit.textCursor()
            list = QtGui.QTextListFormat()
            list.setStyle(QtGui.QTextListFormat.ListDisc)  # listFormat.setStyle(QTextListFormat::ListDisc);
            cursor.insertList(list)

    def numbered_list_action(self, pressed):

        if pressed:
            cursor = self.textEdit.textCursor()
            list = QtGui.QTextListFormat()
            list.setStyle(QtGui.QTextListFormat.ListDecimal)
            cursor.insertList(list)

    def text_background_color_action(self):
        color = QtWidgets.QColorDialog.getColor()

        if color:
            self.textEdit.setTextBackgroundColor(color)

    def text_color_action(self):
        color = QtWidgets.QColorDialog.getColor()

        if color:
            self.textEdit.setTextColor(color)

    def search_action(self):
        string, ok = QtWidgets.QInputDialog.getText(self, 'Search', 'Type in a search word')


    def help_action(self):

        QtWidgets.QMessageBox.information(self, 'Help',
                                  'No help needed here I guess :)')


    def closeEvent(self, event):

        if self.textEdit.toPlainText():
            reply = self.prompt()

            if reply == QtWidgets.QMessageBox.Yes:
                self.save_file_action()
                event.accept()
            elif reply == QtWidgets.QMessageBox.No:
                sys.exit()
            else:
                event.ignore()

        else:
            sys.exit()

    def prompt(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                           'Do you want to save the file ?',
                                           QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No |
                                           QtWidgets.QMessageBox.Cancel,
                                           QtWidgets.QMessageBox.No)
        return reply

def main():
    app = QtWidgets.QApplication(sys.argv)
    m = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()