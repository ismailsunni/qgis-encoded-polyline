import importlib.util
import os

_POLYLINE_PATH = os.path.join(os.path.dirname(__file__), "..", "polyline.py")
_spec = importlib.util.spec_from_file_location("polyline", _POLYLINE_PATH)
polyline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(polyline)

decode = polyline.decode
encode = polyline.encode


GOOGLE_EXAMPLE_ENCODED = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
GOOGLE_EXAMPLE_COORDS = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]


def test_decode_google_example():
    assert decode(GOOGLE_EXAMPLE_ENCODED) == GOOGLE_EXAMPLE_COORDS


def test_encode_google_example():
    assert encode(GOOGLE_EXAMPLE_COORDS) == GOOGLE_EXAMPLE_ENCODED


def test_roundtrip_precision_5():
    coords = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]
    assert decode(encode(coords)) == coords


def test_roundtrip_precision_6():
    coords = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]
    encoded = encode(coords, precision=6)
    assert decode(encoded, precision=6) == coords


def test_decode_geojson_swaps_to_lon_lat():
    result = decode(GOOGLE_EXAMPLE_ENCODED, geojson=True)
    assert result == [(lon, lat) for (lat, lon) in GOOGLE_EXAMPLE_COORDS]


def test_decode_empty_string():
    assert decode("") == []
