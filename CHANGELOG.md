# Changelog

## 1.3.0 — Batch Modeling and Primitive API

### Added
- `Mesh.add_vertices()` for validated multi-vertex insertion and `Mesh.add_vertexs()` for the requested spelling plus shape presets (`sqr`, `rect`, `tri`, `circle`, `ngon`).
- Axis and in-plane rotation options for flat shape presets.
- Atomic `Mesh.add_faces()` and coordinate-based `Mesh.add_polygon()`.
- `Mesh.add_primitive()` generators for cube, box, plane, pyramid, cylinder, cone, sphere and torus.
- `Mesh.add_grid()` convenience method for subdivided planes.
- Explicit `Mesh.weld_vertices()` / `Mesh.remove_doubles()` with old-to-new vertex mapping, optional collapsed-face removal and face-attribute remapping.
- Primitive and batch API reference, upgrade notes and regression tests.

### Compatibility
- The 1.2.0 mesh, modeling, topology, color, material, texture and UV APIs remain available.
- Existing `add_vertex()` and `add_face()` behavior is unchanged.
- Batch insertion never silently merges coordinates; welding is explicit.

### Verification
- 57 unit tests pass with `python -m unittest discover -s tests -v`.
- Live Wings 3D GUI verification is still required on the target installation.


## 1.2.0 — Image Textures and UV

### Added
- `Texture.from_file()` image decoding via Pillow, RGB/RGBA pixel buffers, lower-left row orientation and process-lifetime raw-file transport.
- Basic texture processing: resize and repeat/tile copies.
- `Material.set_texture()` for the upstream-supported `diffuse` image-map channel.
- Per-face-corner UV authoring, validation, transforms and Planar/Box/Cylindrical/Spherical projection.
- E3D adapter mapping to `E3DImage`, `MaterialMaps`, `E3DMesh.tx`, and `E3DFace.tx`.
- Texture/UV tests, examples, and API documentation.

### Limits
- The inspected upstream `MaterialMaps.load_from()` reads `diffuse` only; normal/specular/roughness/metallic maps are not exposed.
- Automatic UV unwrap and island packing are not included.
- Topology-rebuilding operations clear UVs; the caller must re-project after editing.
- Pillow must be available in the Python environment used by Wings. A live GUI/rendering check remains necessary.

## 1.1.0 — Color and Material Support

### Added
- `Color`: immutable normalized RGBA values with hex, tuple, and positional constructors.
- `Material`: immutable E3D/OpenGL material definitions with diffuse, ambient, specular, emission, shininess, metallic, roughness, and vertex-color mode.
- `Mesh.paint_vertex()` and `Mesh.paint_face()`.
- `Mesh.add_material()` and `Mesh.assign_material()`.
- E3D serialization of the `E3DMesh.vc` RGB color table, per-corner `E3DFace.vc` indices, `NewShape.mat` material list, and `E3DFace.mat` references.
- Face style propagation through extrusion, inset, triangulation, and subdivision.
- Color/material rollback support and reference validation.

## 1.0.0 — Stable Core

- Mesh construction, geometry, topology, modeling, controls, selection, E3D adapter and Flatpak bootstrap installer.
