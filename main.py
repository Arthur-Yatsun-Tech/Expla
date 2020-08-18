import sys

from fbs_runtime.application_context.PySide2 import ApplicationContext

from layouts.windows import MainWindow


if __name__ == '__main__':
    application = ApplicationContext()
    window = MainWindow()
    window.show()
    sys.exit(application.app.exec_())
