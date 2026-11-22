# Changelog

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
