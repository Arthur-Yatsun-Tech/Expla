import sys

from fbs_runtime.application_context.PySide2 import ApplicationContext

from layouts.windows.main import MainWindow


def main():
    expla = ApplicationContext()
    window = MainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = expla.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()