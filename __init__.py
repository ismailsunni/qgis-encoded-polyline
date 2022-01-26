# -----------------------------------------------------------
# Copyright (C) 2022 Ismail Sunni
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox


def classFactory(iface):
    return PolylineLoaderPlugin(iface)


class PolylineLoaderPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction("Go!", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

        self.main_action = QAction("Open", self.iface.mainWindow())
        self.main_action.triggered.connect(self.open_main_dialog)
        self.iface.addToolBarIcon(self.main_action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeToolBarIcon(self.main_action)
        del self.action
        del self.main_action

    def run(self):
        QMessageBox.information(None, "Minimal plugin", "Do something useful here")

    def open_main_dialog(self):
        from .main_dialog import MainDialog

        dialog = MainDialog(parent=self.iface.mainWindow(), iface=self.iface)
        dialog.exec_()  # modal
