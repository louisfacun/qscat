from PyQt5.QtCore import QVariant

from qgis.testing import start_app
from qscat.core.layers import create_add_layer

from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.core import QgsWkbTypes

start_app()

def test_create_add_layer():
    """Test creating and adding of layer utility function."""

    project = QgsProject.instance()
    initial_layer_count = len(project.mapLayers())

    geometry_type = 'LineString'
    geometries = [
        QgsGeometry.fromPolylineXY([
            QgsPointXY(0, 0),
            QgsPointXY(1, 1),
        ]),
        QgsGeometry.fromPolylineXY([
            QgsPointXY(2, 2),
            QgsPointXY(3, 3),
        ]),
    ]
    name = 'test_layer'
    crs = 'EPSG:32651'
    fields = [
        {'name': 'field1', 'type':  QVariant.Double},
        {'name': 'field2', 'type':  QVariant.Double},
    ]
    values = [
        [1.0, 2.0],
        [3.0, 4.0],
    ]

    layer = create_add_layer(
        geometry_type, 
        geometries, 
        name,
        fields, 
        values,
    )
    # Project layer count
    assert len(project.mapLayers()) == initial_layer_count + 1

    # Layer properties
    assert layer.isValid()
    assert layer.featureCount() == 2
    assert layer.geometryType() == QgsWkbTypes.LineGeometry
    assert 'test_layer' in layer.name()
    assert [field.name() for field in layer.fields()] == ['id', 'field1', 'field2']

    # TODO: add crs if create_add_layer will accept crs

    # Layer features
    for feat, geometry, value in zip(layer.getFeatures(), geometries, values):
        assert feat.geometry().asPolyline() == geometry.asPolyline()
        assert feat['field1'] == value[0]
        assert feat['field2'] == value[1]