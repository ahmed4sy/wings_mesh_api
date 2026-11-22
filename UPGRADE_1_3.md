# Upgrade from Wings Mesh API 1.2.0 to 1.3.0

1. Back up local changes to the installed `plugins/mesh_tools/wings` package.
2. Extract the 1.3.0 release and run `python3 install_flatpak.py` from the release folder.
3. Restart Wings 3D and verify a basic Shape Script.

## New APIs

- `Mesh.add_vertices(positions)` adds coordinate tuples in one validated batch.
- `Mesh.add_vertexs(shape=...)` creates ordered vertex presets. The spelling is retained as a convenience alias; `add_vertices()` is preferred for explicit coordinate data.
- `Mesh.add_faces(faces)` adds a face batch atomically.
- `Mesh.add_polygon(positions)` creates one face directly from coordinate tuples.
- `Mesh.add_primitive(shape, ...)` generates a complete parametric primitive.
- `Mesh.add_grid(...)` adds a subdivided plane.
- `Mesh.weld_vertices(...)` / `Mesh.remove_doubles(...)` explicitly merge near-coincident vertices.

## Compatibility

All 1.2.0 mesh, color, material, texture and UV APIs remain present. The default behavior of `add_vertex()` and `add_face()` is unchanged. Batch insertion does not automatically deduplicate vertices; call `weld_vertices()` explicitly when topology welding is desired.

For complete parameter defaults, return structures, errors and examples, see `docs/PRIMITIVES_API.md` and `docs/API.md`.
