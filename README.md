# Wings Mesh API 1.3.0 — Batch Modeling and Primitives

A higher-level Python layer for the `wpc_scripting_shapes` extension. Version 1.3 adds batch vertex/face creation, flat shape presets, parametric primitives and explicit vertex welding while retaining the 1.2 texture/UV and 1.1 color/material APIs.

## Requirements

- Wings 3D with the supplied `wpc_scripting_shapes.tar` extension installed.
- Python 3.10+ selected by the scripting extension.
- Pillow in that same Python environment when loading/resizing/tiling images: `python3 -m pip install Pillow`.

## Install (Flathub)

Extract the release and run `python3 install_flatpak.py`, then restart Wings 3D. The installer copies the `wings` package into `plugins/mesh_tools/wings` and adds a managed, reversible import-path hook to the original scripting engine `init.py`. It does not replace the engine loader. Any external Shape Script can then use `from wings import Mesh`.

## Textured shape example

Place `brick_wall.png` beside the Shape Script, then run: the example's `w3d_main_function` builds a quad, loads the image, assigns it to the material's `diffuse` map, projects UVs, and returns the E3D shape.

```python
from pathlib import Path
from wings import Mesh, Material, Texture


def w3d_main_function(params, params_by_key, extra_params):
    texture = Texture.from_file(Path(__file__).with_name("brick_wall.png"))
    mesh = Mesh("TexturedQuad")
    for point in [(0, 0, 0), (4, 0, 0), (4, 3, 0), (0, 3, 0)]:
        mesh.add_vertex(point)
    mesh.add_face([0, 1, 2, 3])
    material = Material("BrickWall", roughness=0.85)
    material.set_texture(texture, channel="diffuse")
    mesh.assign_material(0, material)
    mesh.project_uv(method="planar", axis="z")
    return mesh.create(prefix="TexturedQuad")
```


## 1.3 batch modeling and primitive example

```python
from wings import Mesh

mesh = Mesh("QuickModel")
Vs = mesh.add_vertexs(shape="sqr", pos=(0, 0, 0), size=2)
mesh.add_face(Vs)
mesh.add_primitive("cube", pos=(3, 0, 0), size=2)
mesh.add_primitive("sphere", pos=(-3, 0, 0), radius=1)
mesh.add_grid(pos=(0, 3, 0), size=4, segments=(4, 4))
```

Use `add_vertices([...])` for explicit coordinate batches, `add_faces([...])` for multiple faces, and `add_primitive()` when the complete object topology should be generated. Batch insertion does not silently deduplicate coordinates; call `weld_vertices()` explicitly. See `docs/PRIMITIVES_API.md` for all presets, parameters and return values.

The release includes `examples/batch_model.py` as a complete 1.3 Shape Script example.

## 1.2 texture and UV features

- `Texture.from_file(path, keep_alpha=True, flip_y=True)` decodes image formats supported by Pillow, including PNG, JPEG, TGA and BMP.
- `Texture.resized((width, height))` and `Texture.tiled((repeat_x, repeat_y))` make processed copies.
- `Material.set_texture(texture, channel="diffuse")` links an image to the material.
- `mesh.set_face_uvs(face_id, coords)` sets one `(u, v)` pair per face corner.
- `mesh.project_uv(method=...)` supports `planar`, `box`, `cylindrical` and `spherical`.
- `mesh.transform_uvs(scale=..., rotation=..., offset=...)` adjusts UVs.

The adapter uses the source-defined `E3DImage`, `MaterialMaps`, `E3DMesh.tx` and `E3DFace.tx` fields. The supplied `MaterialMaps.load_from()` implementation handles only the `diffuse` key, so normal/specular/roughness/metallic maps are not claimed. Automatic UV unwrap and island packing are not included. Topology-changing operations clear UVs; project again after editing.

## Previous APIs retained

The release retains mesh construction, topology, geometry, modeling, local selection, parameter controls, the Flatpak bootstrap, vertex/face colors and E3D material properties from 1.0/1.1. See `docs/API.md`, `docs/COLOR_AND_MATERIAL_API.md` and `docs/TEXTURE_UV_API.md`.

## Tests and verification

Run `python3 -m pytest -q` or `python3 -m unittest discover -s tests -v` from this directory. Unit and adapter-contract tests pass locally. They do not replace a live Wings GUI check; image display still needs confirmation in the user's installed Wings build and Python environment.
