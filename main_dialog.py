import os

from qgis.PyQt import QtCore, uic, Qt
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import (
    QgsMessageLog,
    Qgis,
    QgsVectorLayer,
    QgsFeature,
    QgsProject,
    QgsGeometry,
    QgsPointXY,
)

import polyline


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split("/"))
    ui_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ui_file))
    return uic.loadUiType(ui_file_path)[0]


FORM_CLASS = get_ui_class("main_dialog.ui")


class MainDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None, iface=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.load_polyline_button.clicked.connect(self.load_polyline)

    def load_polyline(self):
        polyline_string = self.polyline_text_edit.toPlainText()
        # polyline_string = 'ezeqxAi~kfMBjBHvBJrAZvCZrCnP~xA`DpYPdBJz@b@dEPdCPnB`@vFz@rKB`@`AjMdC|[v@nJvAnQ\\vE`BjU_@Fa@HaARui@rLLbBzAzR`@vF^|ElFpr@HfA'
        QgsMessageLog.logMessage(polyline_string, "Polyline Loader", level=Qgis.Info)
        coordinates = polyline.decode(polyline_string, precision=6, geojson=True)
        QgsMessageLog.logMessage(
            "%s coordinates" % len(coordinates), "Polyline Loader", level=Qgis.Info
        )
        QgsMessageLog.logMessage(
            "First coordinate: %s, %s" % coordinates[0],
            "Polyline Loader",
            level=Qgis.Info,
        )

        qgis_coords = [QgsPointXY(x, y) for x, y in coordinates]
        geom = QgsGeometry.fromPolylineXY(qgis_coords)

        # Create memory layer
        layer = QgsVectorLayer(
            "LineString?crs=epsg:4326&field=id:integer",
            self.layer_name_line_edit.text(),
            "memory",
        )
        pr = layer.dataProvider()
        feature = QgsFeature()
        feature.setAttributes([1])
        feature.setGeometry(geom)
        pr.addFeatures([feature])
        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)
