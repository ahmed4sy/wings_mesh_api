# Wings Mesh API 1.3.0 — Batch Modeling and Primitives

طبقة Python مستقرة فوق `wpc_scripting_shapes`، مع Bootstrap يُفعّل الاستيراد من أي مجلد سكربتات داخل محرك Wings.

الإصدار 1.3 يضيف واجهات دفعات ومولّدات أشكال ومجسمات جاهزة فوق الأساس المستقر للإصدارين 1.1 و1.2. هذه الطبقة تضيف واجهة Python أعلى إضافة `wpc_scripting_shapes` المرفقة من المستخدم. الفكرة هي فصل بناء المجسم والتحقق من سلامة بنيته والحسابات الرقمية عن بروتوكول Wings 3D، ثم تحويل النموذج إلى كائن `E3D` الذي تتوقعه الإضافة.

## ما الذي تتضمنه؟

- **Mesh:** إضافة الرؤوس والوجوه فردياً أو على دفعات، إنشاء الأشكال والمجسمات الجاهزة، دمج Mesh، التحقق من البنية، والتحويل إلى `new_shape`.
- **Batch API:** `add_vertices()` و`add_vertexs()` و`add_faces()` و`add_polygon()` لتقليل تكرار الكتابة.
- **Primitive Library:** مكعب وصندوق ومستوى وهرم وأسطوانة ومخروط وكرة وحلقة، مع تحكم في الأبعاد والتقسيمات.
- **Cleanup:** `weld_vertices()` و`remove_doubles()` لدمج الرؤوس المتقاربة بشكل صريح.
- **Topology:** استخراج الحواف، الوجوه المتصلة بكل حافة، الجوار، الحواف الحدودية وغير المتعددة.
- **Selection:** تحديد محلي للرؤوس والحواف والوجوه. هذا التحديد يعمل على كائن `Mesh` في Python.
- **Geometry:** normals، المساحات، المراكز، الأطوال، bounding box، المساحة السطحية والحجم، والتحويلات.
- **Modeling:** Extrude لوجه واحد، Inset لمضلع مستوٍ محدب، Bridge بين حلقتين متساويتين، Bevel لرأس مغلق، وتقسيم الوجوه إلى quads.
- **ParameterCore / Dial:** ضبط الحدود والدقة والخطوة، حساب القيم المشتقة بترتيب الاعتماديات، وتحويل موضع بكرة افتراضية أو عجلة الفأرة إلى قيمة رقمية.
- **WingsBackend:** غلاف لبعض الدوال الموجودة فعلياً في `w3d_we.py` داخل عملية الإضافة.
- **Color:** كائن ألوان immutable يدعم Hex وRGB وRGBA والقيم المعيارية.
- **Vertex / Face Colors:** تلوين الرؤوس والوجوه مع أولوية لون الوجه على لون الرأس عند التعارض.
- **Material:** تعريف مواد Wings/OpenGL وتعيينها للوجوه مع Diffuse وAmbient وSpecular وEmission وShininess وMetallic وRoughness.
- **Texture:** تحميل صور PNG/JPEG/TGA/BMP عبر Pillow وتحويلها إلى بيانات خام ينقلها بروتوكول `E3DImage`.
- **Material Maps:** ربط صورة بخامة عبر قناة `diffuse` المدعومة في نسخة `w3d_e3d.py` المرفقة.
- **UV:** تخزين إحداثيات UV لكل ركن وجه، وإسقاط Planar وBox وCylindrical وSpherical، وتحويل Scale/Rotation/Offset.
- **E3D Texture Adapter:** تحويل UV إلى `E3DMesh.tx` و`E3DFace.tx`، والصورة إلى `MaterialMaps` و`E3DImage`.

## المتطلبات

1. Wings 3D.
2. تثبيت إضافة `wpc_scripting_shapes` من ملف الأرشيف الأصلي `wpc_scripting_shapes.tar`.
3. Python **3.10 أو أحدث** وإتاحته للإضافة عبر `PATH`.
4. Pillow مطلوب فقط عند تحميل الصور: `python3 -m pip install Pillow` في بيئة Python التي تشغّل محرك Wings.
5. لا يحتاج هذا المشروع إلى Gauche عند استخدام Python فقط.

> نسخة الإضافة الأصلية تدعم تشغيل Python من خلال جسر السكربتات؛ أما هذه الطبقة فتستخدم ميزات Python الحديثة ولذلك تتطلب Python 3.10+.

## التثبيت في Wings 3D (Flathub / Ubuntu)

الإصدار المستقر يتضمن مُثبّتاً يكتشف مجلد بيانات Flathub ويضيف مسار الطبقة تلقائياً إلى محرك `wpc_scripting_shapes`. لذلك لن تحتاج إلى كتابة `sys.path` في كل سكربت، ولن تحتاج إلى نقل سكربتاتك إلى مجلد الإضافة.

1. ثبّت إضافة `wpc_scripting_shapes.tar` الأصلية في Wings 3D.
2. فك ضغط هذا المشروع في أي مجلد.
3. افتح Terminal داخل مجلد `wings_layer` وشغّل:

```bash
python3 install_flatpak.py
```

المُثبّت يبحث عن:

```text
~/.var/app/com.wings3d.WINGS/data/Wings3D/<version>/plugins/
```

ثم يثبت المكتبة في `plugins/mesh_tools/wings` ويضيف كتلة صغيرة مُدارة إلى:

```text
plugins/wpc_scripting_shapes_init/py/init.py
```

تُضاف الكتلة بعد `import sys`، وتكتشف مجلد `mesh_tools` انطلاقاً من موقع `init.py` نفسه؛ لذلك لا تعتمد على رقم إصدار Wings أو اسم المستخدم. ينشئ المُثبّت نسخة احتياطية باسم `init.py.wings-mesh-api.bak`، ويمكن تشغيله أكثر من مرة بأمان. لا يستبدل `init.py` ولا يغيّر منطق محمّل السكربتات الأصلي.

لعرض مسارات Wings المكتشفة:

```bash
python3 install_flatpak.py --list
```

إذا كان التثبيت في مسار مخصص:

```bash
python3 install_flatpak.py --plugins-dir "/absolute/path/to/plugins"
```

بعد ذلك أعد تشغيل Wings 3D. من الآن يمكن لأي ملف Shape Script، حتى لو كان في `~/Documents/wings/Scripts/shape/`، أن يبدأ مباشرةً بـ:

```python
from wings import Mesh
```

لا تضف `sys.path` يدوياً، ولا تنسخ مجلد `wings` بجوار كل سكربت. يظل `init.py` الأصلي تابعاً للإضافة؛ أما `wings/__init__.py` فهو مدخل واجهة المكتبة وليس مدخل محرك السكربتات.

لإزالة تفعيل الاستيراد دون حذف المكتبة:

```bash
python3 uninstall_flatpak.py
```

ولحذف المكتبة أيضاً:

```bash
python3 uninstall_flatpak.py --remove-package
```

## مثال الاستخدام — واجهات 1.3

```python
from wings import Mesh

mesh = Mesh("QuickModel")

# Create a square face with four vertices in one call
Vs = mesh.add_vertexs(shape="sqr", pos=(0, 0, 0), size=2)
mesh.add_face(Vs)

# Add complete ready-made objects
mesh.add_primitive("cube", pos=(3, 0, 0), size=2)
mesh.add_primitive("sphere", pos=(-3, 0, 0), radius=1)

# Add a grid with 4 by 4 quad cells
mesh.add_grid(pos=(0, 3, 0), size=4, segments=(4, 4))
```

لإضافة دفعة من الإحداثيات استخدم `mesh.add_vertices([...])`، ولإنشاء مجموعة وجوه استخدم `mesh.add_faces([...])`. لا تدمج الدوال الرؤوس المتطابقة تلقائياً؛ استخدم `mesh.weld_vertices(tolerance=0.001)` عند الحاجة إلى الدمج. راجع `docs/PRIMITIVES_API.md` لكل المعاملات والافتراضيات.

لإرسال الشكل من سكربت مستضاف داخل الإضافة، عرّف دالة الإدخال وأعد نتيجة `create()` منها:

```python
from wings import Mesh

def build_shape(params, params_by_key, extra_params):
    mesh = Mesh("Quad")
    v0 = mesh.add_vertex((0, 0, 0))
    v1 = mesh.add_vertex((1, 0, 0))
    v2 = mesh.add_vertex((1, 1, 0))
    v3 = mesh.add_vertex((0, 1, 0))
    mesh.add_face([v0, v1, v2, v3])
    return mesh.create(prefix="Quad")

w3d_main_function = build_shape
```

**مهم:** استدعاء `mesh.create()` وحده لا يرسل الشكل إذا لم تُعِد قيمته من دالة `w3d_main_function`. الإضافة تتولى تمرير القيمة المعادة عبر بروتوكول `new_shape`.

## الألوان والمواد — الإصدار 1.1

```python
from wings import Mesh, Color, Material

mesh = Mesh("ColoredCube")
# أنشئ الرؤوس والوجوه أولاً
mesh.paint_vertex(0, Color("#FF0000"))
mesh.paint_face(0, Color("#00FF00"))
red_material = Material(
    name="RedMaterial", diffuse="#FF0000", roughness=0.4, metallic=0.2
)
mesh.assign_material(1, red_material)
return mesh.create(prefix="ColoredCube")
```

راجع `docs/COLOR_AND_MATERIAL_API.md` للشرح الكامل. الألوان تُرسل إلى E3D؛ alpha لا ينتقل مع Vertex Colors لأن جدول E3D الأصلي يخزن RGB فقط. لإظهارها داخل Wings فعّل `View → Show Colors` و`View → Show Materials` بحسب نوع اللون. دعم الصور وUV أضيف في الإصدار 1.2.0، وتوسعت واجهة بناء الشبكات في 1.3.0، مع تفاصيله وحدوده في `docs/TEXTURE_UV_API.md`.

## Core المعاملات والبكرة

```python
from wings import Parameter, Derived, ParameterCore, Dial

core = ParameterCore(
    parameters=[Parameter("Radius", 1.0, 0.1, 10.0, step=0.05)],
    derived=[Derived("Diameter", ("Radius",), lambda p: 2 * p["Radius"])],
)
values = core.resolve({"Radius": 2.37})  # Radius يصبح 2.35 وDiameter يصبح 4.70

dial = Dial(core.parameters["Radius"])
new_value = dial.move(values["Radius"], wheel_ticks=3)
position = dial.to_position(new_value)
```

`Dial` هو محرك تحويل رقمي مستقل عن واجهة المستخدم: يستقبل موضعاً بين 0 و1 أو عدد درجات عجلة الفأرة. واجهة `.wscr` التجريبية الحالية تعرض حقولاً رقمية قياسية؛ لم أجد في ملفات الإضافة المرفقة دليلاً على Widget بكرة رسومية مخصصة، لذلك لا أدّعي وجود بكرة مرئية أصلية. يمكن لاحقاً وصل `Dial` بواجهة تفاعلية خارجية أو بواجهة Wings إذا وفّرت الإضافة Widget مناسباً.

## الخامات والصور وUV — الإصدار 1.2

```python
from wings import Mesh, Material, Texture

mesh = Mesh("TexturedQuad")
for point in [(0, 0, 0), (2, 0, 0), (2, 2, 0), (0, 2, 0)]:
    mesh.add_vertex(point)
mesh.add_face([0, 1, 2, 3])

texture = Texture.from_file("assets/brick_wall.png")
material = Material("BrickMaterial", roughness=0.85)
material.set_texture(texture, channel="diffuse")
mesh.assign_material(0, material)
mesh.project_uv(method="planar", axis="z", scale=(1, 1, 1))
return mesh.create(prefix="TexturedQuad")
```

الإسقاطات المتاحة: `planar` و`box` و`cylindrical` و`spherical`. يمكن تعديل UV بعد إنشائها باستخدام `mesh.transform_uvs(scale=(...), rotation=..., offset=(...))`. عمليات تغيير الطوبولوجيا مثل Extrude وInset وSplit وSubdivision تُبطل UV القديمة على mesh المعاد بناؤه؛ أعد الإسقاط بعدها لتجنب خريطة غير مطابقة لزوايا الوجوه.

**حدود النسخة 1.2:** مصدر الإضافة المرفق يعرّف `MaterialMaps` ويدعم تحميل مفتاح `diffuse` فقط؛ لا توجد واجهة مثبتة لقنوات normal/roughness/metallic أو آلية Unwrap تلقائي. كما يعتمد فك JPG/PNG/TGA/BMP على توفر Pillow داخل بيئة Python التي تشغّل Wings. تم اختبار إنشاء حمولة E3D بدوال وهمية تطابق حقول المصدر، لكن يجب إجراء تجربة GUI فعلية في Wings للتحقق من عرض الصورة في التثبيت الخاص بك.

## حدود التكامل المعروفة

- ملفات `callable.conf` و`w3d_we.py` توفر عدداً كبيراً من وظائف الهندسة والطوبولوجيا، لكن النسخة التي فُحصت لا تكشف getter موثقاً لقراءة التحديد الحالي. لذلك `Mesh.selection` تحديد محلي وليس قراءة مباشرة لتحديد Wings الحالي.
- `WingsBackend` يغلّف فقط الدوال التي تم التأكد من وجودها في واجهة الإضافة؛ لا يحاول تخمين أسماء دوال غير موجودة.
- `extrude_face`, `inset_face`, `bridge_loops` و`bevel_vertex` هي عمليات محلية على نموذج `Mesh`. ليست كل واحدة منها استدعاءً مقابلاً مباشراً في Wings.
- `inset_face` مصمم للمضلعات المستوية المحدبة. `bevel_vertex` يتطلب حلقة مجاورة مغلقة ومنتظمة؛ لا يطبق Edge-loop bevel.
- `subdivide_faces` تقسيم طوبولوجي إلى quads باستخدام نقاط منتصف الحواف ومركز الوجه، وليس Catmull–Clark smoothing.
- يجب أن يكون اتجاه الوجوه متسقاً قبل العمليات التي تتطلب مجسماً مغلقاً. عمليات التعديل داخل `transaction()` ترجع النموذج إلى حالته السابقة إذا فشل التحقق.
- تم اختبار التحويل إلى بنية `E3D` باستخدام وحدات Python الأصلية الموجودة في الأرشيف، لكن لم يتم تشغيل Wings 3D تفاعلياً في بيئة الاختبار هذه.

## الاختبارات

من جذر المجلد:

```bash
python -m unittest discover -s tests -v
```

الاختبارات تغطي تثبيت Flatpak واكتشاف المسار، وتكرارية وإزالة Bootstrap، والاستيراد من مجلد خارجي، وقراءة الصور وبيانات RGB/RGBA والإسقاطات وUV وخرائط E3D، بالإضافة إلى بناء Cube مغلق، التحقق من الوجوه والحواف، القياسات، التحويلات، الدمج، التقسيم، Extrude، Inset، Bridge، Bevel، التحديد المحلي، وحساب المعاملات والبكرة.

## الملفات

- `wings/`: واجهة Python ومحوّل E3D وBootstrap داخلي.
- `wings_installer.py`, `install_flatpak.py`, `uninstall_flatpak.py`: تثبيت وإزالة Bootstrap بطريقة آمنة وقابلة للتكرار.
- `examples/external_cube.py`: مثال Shape Script موجود خارج مجلد الإضافة ويستخدم `from wings import Mesh` مباشرة.
- `examples/batch_model.py`: مثال الإصدار 1.3 لإنشاء الأشكال المسطحة والمجسمات دفعة واحدة.
- `plugin_scripts/`: ملفات تسجيل مثال Parametric Box في قائمة Wings.
- `parametric_box.py` و`parametric_box.wscr`: مثال تشغيل منفصل عن حزمة القائمة.
- `docs/API.md`: مرجع الواجهة.
- `docs/PRIMITIVES_API.md`: توثيق الواجهات الجماعية والأشكال والمجسمات والدمج.
- `docs/TEXTURE_UV_API.md`: تحميل الصور، قنوات الخامات، إسقاطات UV وحدودها.
- `requirements.txt`: اعتماد Pillow الاختياري لعمليات الصور.
- `examples/textured_quad.py` و`examples/brick_wall.png`: مثال Shape Script كامل مع صورة خامة تجريبية مرفقة.
- `docs/ARCHITECTURE.md`: تصميم الجسر والتدفق.
- `tests/`: اختبارات الوحدة.
