# Upgrade from Wings Mesh API 1.1.0 to 1.2.0

1. Back up any local modifications to the installed `plugins/mesh_tools/wings` folder.
2. Extract this release and run `python3 install_flatpak.py` as before; the installer replaces the API package with 1.2.0 while keeping the original scripting engine bootstrap backup.
3. Ensure Pillow is available to the Python interpreter launched by Wings. `python3 -m pip install Pillow` is sufficient only when that is the same interpreter/environment.
4. Restart Wings 3D and test a small textured plane before applying textures to a large model.

Existing 1.0/1.1 mesh, color, material, geometry and modeling APIs remain available. New topology operations clear per-face UV assignments; call `project_uv()` after those operations. Only the diffuse image map is supported by the inspected source archive.
