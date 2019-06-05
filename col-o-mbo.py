''' App de COL-O-MBO '''

import faces
import graph

IMAGE_PATH = 'suspects.jpg'

print("++++ Detectando sospechosos ++++")
faces.detect_export_faces(IMAGE_PATH)
print("++++ Generando escenario ++++")
graph.create_scenario()
