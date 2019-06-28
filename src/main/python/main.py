import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QMainWindow

from ui.main_window import Ui_MainWindow


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        self.main_window.show()
        return self.app.exec_()                 # 3. End run() with this line

    @cached_property
    def main_window(self):
        return MainWindow(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ctx = ctx
        
        self.test_push_button.clicked.connect(self.button_clicked)
        version = self.ctx.build_settings['version']
        self.setWindowTitle("DART Plotting Tool v." + version)
        self.resize(250, 150)
    
    def button_clicked(self):
        self.test_push_button.setText("Button Clicked")
        print("Button clicked")

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
