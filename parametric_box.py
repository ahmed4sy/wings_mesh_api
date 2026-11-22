"""Example Wings 3D Shape from Script using the higher-level API."""
from wings import Mesh, Parameter, Derived, ParameterCore

CORE = ParameterCore(
    parameters=[
        Parameter("Width", 2.0, 0.05, 100.0, 0.05),
        Parameter("Depth", 2.0, 0.05, 100.0, 0.05),
        Parameter("Height", 2.0, 0.05, 100.0, 0.05),
    ],
    derived=[
        Derived("HalfWidth", ("Width",), lambda p: p["Width"] / 2.0),
        Derived("HalfDepth", ("Depth",), lambda p: p["Depth"] / 2.0),
        Derived("HalfHeight", ("Height",), lambda p: p["Height"] / 2.0),
    ],
)


def build_box(params, params_by_key, extra_params):
    values = CORE.resolve({
        "Width": params_by_key.get("Width", 2.0),
        "Depth": params_by_key.get("Depth", 2.0),
        "Height": params_by_key.get("Height", 2.0),
    })
    x, y, z = values["HalfWidth"], values["HalfDepth"], values["HalfHeight"]

    mesh = Mesh("ParametricBox")
    vertices = [
        mesh.add_vertex((-x, -y, -z)),
        mesh.add_vertex(( x, -y, -z)),
        mesh.add_vertex(( x,  y, -z)),
        mesh.add_vertex((-x,  y, -z)),
        mesh.add_vertex((-x, -y,  z)),
        mesh.add_vertex(( x, -y,  z)),
        mesh.add_vertex(( x,  y,  z)),
        mesh.add_vertex((-x,  y,  z)),
    ]
    # Outward-facing quads. Vertex indices are zero-based.
    for face in (
        (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
        (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ):
        mesh.add_face(face)

    mesh.validate(require_closed=True)
    return mesh.create(prefix="ParametricBox")


w3d_main_function = build_box
