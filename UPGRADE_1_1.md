# Upgrade from Wings Mesh API 1.0.0 to 1.1.0

1. Close Wings 3D.
2. Keep a backup copy of the currently installed `plugins/mesh_tools` folder if you have custom edits there.
3. Extract this release to a convenient folder.
4. Open a terminal in the extracted `wings_layer` directory and run:

   ```bash
   python3 install_flatpak.py
   ```

5. The installer copies the updated `wings` package (including `color.py` and `materials.py`) into the detected Flathub Wings plugin directory. The 1.0.0 import hook is recognized and is not duplicated.
6. Restart Wings 3D and run `examples/colored_cube.py` as a Shape Script.
7. In Wings, enable `View → Show Colors` and `View → Show Materials` to inspect the corresponding attributes.

The original `wpc_scripting_shapes_init/py/init.py` remains the scripting engine entry point. Do not replace it with the layer's `wings/__init__.py`.

## Quick external API check

From an ordinary terminal, the mesh, color, and material model can be checked without starting Wings:

```bash
cd wings_layer
PYTHONPATH=. python3 -c 'from wings import Mesh, Color, Material; m=Mesh("SmokeTest"); a=m.add_vertex((0,0,0)); b=m.add_vertex((1,0,0)); c=m.add_vertex((0,1,0)); m.add_face([a,b,c]); m.paint_vertex(a, Color("#FF0000")); m.assign_material(0, Material("RedMaterial", diffuse="#FF0000")); print(m.to_dict())'
```

`mesh.create()` itself requires the Wings scripting runtime because it returns the plugin's `NewShape` protocol object.
