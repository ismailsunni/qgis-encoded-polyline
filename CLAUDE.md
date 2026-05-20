# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A QGIS 3 plugin that decodes Google/OSM-style encoded polylines and loads them as in-memory vector layers. It is loaded by QGIS, not run standalone — there is no `pip install`, no test suite, and no entry point besides QGIS calling `classFactory(iface)` in `__init__.py`.

## Common commands

- **Package for distribution / QGIS plugin install**: `./package.sh` — produces `encoded-polyline.zip` from the current `HEAD` via `git archive` (so commit changes before packaging; uncommitted files are not included).
- **Local install for development**: symlink or copy the repo directory into the QGIS plugins folder, e.g. `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/encoded-polyline`, then enable "Encoded Polyline" in QGIS' Plugin Manager. Use the *Plugin Reloader* plugin to pick up code changes without restarting QGIS.

## Architecture

Three-file core, each with a clear role:

- `__init__.py` — QGIS plugin entry point. `classFactory(iface)` returns `EncodedPolylinePlugin`, which registers a single toolbar action. The dialog is imported lazily inside `open_main_dialog` so QGIS startup stays cheap.
- `main_dialog.py` — `MainDialog` (QDialog) loaded from `main_dialog.ui` via `uic.loadUiType`. Owns all UI logic: reads the encoded string + precision from the form, calls `polyline.decode`, builds a `QgsVectorLayer` (memory provider, LineString, EPSG:4326), adds a single `QgsFeature` with a `QgsGeometry.fromPolylineXY([QgsPointXY(lon, lat), ...])`, applies `redLineStyle.qml`, and adds the layer to `QgsProject.instance()`. The module-level `EXAMPLES` list populates the sample dropdown.
- `polyline.py` — vendored copy of https://github.com/frederickjansen/polyline (`PolylineCodec` + module-level `decode`/`encode`), de-`six`-ified for Python 3 only. Coordinates returned as `(lat, lon)` tuples unless `geojson=True`. Do not refactor casually — keep upstream-compatible.

Coordinate ordering is the easiest place to introduce a bug: `polyline.decode` returns `(lat, lon)`, but `QgsPointXY` takes `(x, y) = (lon, lat)`. Any code touching the decode → geometry path must swap.

## Supporting files

- `main_dialog.ui` — Qt Designer form. Edit in Designer; do not hand-edit unless the change is trivial.
- `redLineStyle.qml` — QGIS layer style applied to every created layer.
- `metadata.txt` — QGIS plugin manifest (name, version, `qgisMinimumVersion`). Bump `version=` here when releasing.
- `encodedPolyline.svg` — toolbar icon, referenced by both `__init__.py` and `metadata.txt`.

## Conventions

- Precision: Google Maps uses 5, OpenStreetMap/Valhalla uses 6. The dialog exposes this; don't hardcode.
- Python is QGIS' bundled interpreter; the plugin runs on QGIS 3 (Qt5) and QGIS 4 (Qt6). Always import Qt classes via `qgis.PyQt.*` (never `PyQt5.*` directly) and use the scoped enum form (e.g. `QDialogButtonBox.StandardButton.Reset`, not `QDialogButtonBox.Reset`) so the same code works on both. `metadata.txt` declares `supportsQt6=True`.
