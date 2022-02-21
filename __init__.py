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

import os
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon


def classFactory(iface):
    return EncodedPolylinePlugin(iface)


class EncodedPolylinePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "encodedPolyline.svg")
        )
        action_icon = QIcon(icon_path)
        self.main_action = QAction(
            action_icon, "Encoded Polygon", self.iface.mainWindow()
        )
        self.main_action.triggered.connect(self.open_main_dialog)
        self.iface.addToolBarIcon(self.main_action)

    def unload(self):
        self.iface.removeToolBarIcon(self.main_action)
        del self.main_action

    def open_main_dialog(self):
        from .main_dialog import MainDialog

        dialog = MainDialog(parent=self.iface.mainWindow(), iface=self.iface)
        dialog.exec_()  # modal
