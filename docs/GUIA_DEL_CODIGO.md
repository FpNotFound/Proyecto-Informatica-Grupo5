# Guía del código — Sprint 2

Esta guía explica cómo está organizado el código y cómo viajan los datos de
un archivo a otro. **Cada línea de código lleva además un comentario** (las
líneas que empiezan por `#`) que explica qué hace. Lee primero esta guía y
después abre los archivos en el orden del apartado 4.

---

## 1. Lo mínimo de Python para entender el código

| Lo que ves | Qué significa |
|---|---|
| `# texto` | Comentario. Python lo ignora; es solo para personas. |
| `"""texto"""` | Comentario largo al principio de un archivo o función. |
| `x = 5` | Guarda el valor 5 con el nombre `x` (una *variable*). |
| `import json` / `from a import b` | Trae herramientas de otro archivo o de Python. |
| `def nombre(datos):` | Define una *función*: un bloque de pasos con nombre que se puede usar muchas veces. |
| `return x` | La función termina y entrega `x` a quien la llamó. |
| `class Local:` | Un *molde* que describe qué datos tiene una cosa (un local, un usuario...). |
| `self.nombre` | Un dato que pertenece a ese objeto concreto ("el nombre de *este* local"). |
| `if ...:` / `elif ...:` / `else:` | "Si pasa esto... / si no, si pasa esto otro... / si no...". |
| `for x in lista:` | Repite los pasos de dentro una vez por cada elemento de la lista. |
| `[]` | Lista vacía. `lista.append(x)` añade `x` al final. |
| `{"clave": valor}` | Diccionario: parejas nombre → valor. Es lo que se guarda en el JSON. |
| `None` | "Nada". Se usa cuando algo no existe o ha fallado. |
| `not x` | Verdadero si `x` está vacío, es `None` o es `False`. |
| `f"Hola {nombre}"` | Texto que mete dentro el valor de `nombre`. |
| `try:` / `except:` | "Intenta esto; si da este error, haz esto otro". |
| La sangría (espacios a la izquierda) | Indica qué líneas están *dentro* de un `if`, `for`, `def` o `class`. |

---

## 2. Arquitectura MVC

El proyecto separa el código en tres capas para que cada archivo haga una sola cosa:

```
 VISTA (views/)          CONTROLADOR (controllers/)        MODELO (models/)
 Lo que se ve      ───►  Comprueba datos y permisos  ───►  Guarda y lee
 (botones, cajas)  ◄───  y decide qué hacer          ◄───  los archivos .json
```

- **Modelo**: describe los datos (`Usuario`, `Local`) y los lee/escribe en JSON.
- **Controlador**: las reglas. Por ejemplo, "solo la Autoridad puede borrar" o "el aforo debe ser un número".
- **Vista**: dibuja la pantalla con Flet y, cuando se pulsa un botón, llama al controlador.

Una vista **nunca** abre un archivo JSON y un modelo **nunca** dibuja nada.

---

## 3. Estructura de carpetas

```
main.py                         Arranca la aplicación
src/
├── app.py                      Cambia de pantalla y recuerda quién ha entrado
├── models/
│   ├── archivo_json.py         ★ NUEVO · Lee y escribe CUALQUIER archivo JSON
│   ├── usuario.py              Usuario + roles (ahora con código de negocio / ID policial)
│   ├── local.py                ★ NUEVO · Local (bar, restaurante...)
│   ├── ids_policiales.json     ★ NUEVO · Lista oficial de IDs policiales válidos
│   ├── usuarios.json           Se crea solo (no se sube a GitHub)
│   └── locales.json            ★ NUEVO · Se crea solo (no se sube a GitHub)
├── controllers/
│   ├── user_controller.py      Crea y busca usuarios, protege contraseñas
│   ├── login_controller.py     Registro (con reglas por rol) e inicio de sesión
│   └── local_controller.py     ★ NUEVO · CRUD de locales + permisos por rol
└── views/
    ├── login_view.py           Pantalla de inicio de sesión
    ├── register_view.py        Registro (el campo extra cambia según el rol)
    ├── main_view.py            Pantalla principal según el rol
    ├── locales_view.py         ★ NUEVO · Lista de locales con botones según el rol
    └── local_form_view.py      ★ NUEVO · Formulario para crear / editar un local
docs/
├── ROLES.md                    Documentación de los roles
└── GUIA_DEL_CODIGO.md          Este documento
```

---

## 4. Orden recomendado de lectura

1. `src/models/archivo_json.py`: cómo se lee y escribe un JSON (dos funciones).
2. `src/models/local.py` y `src/models/usuario.py`: qué datos tiene cada cosa.
3. `src/controllers/user_controller.py`: crear y buscar usuarios.
4. `src/controllers/local_controller.py`: el CRUD y los permisos.
5. `src/controllers/login_controller.py`: las reglas del registro por rol.
6. `src/app.py`: cómo se pasa de una pantalla a otra.
7. Las vistas, empezando por `register_view.py` y `locales_view.py`.

---

## 5. Lectura y escritura en JSON

Un archivo JSON es texto con un formato fijo que Python puede convertir en
listas y diccionarios. Así se ve `locales.json`:

```json
[
  {
    "codigo": "NEG-001",
    "nombre": "Bar Demo",
    "direccion": "Calle Ferraz 10",
    "tipo": "Bar",
    "aforo": 80
  }
]
```

Todo pasa por **dos funciones** de `archivo_json.py`:

| Función | Qué hace |
|---|---|
| `leer_json("locales.json")` | Abre el archivo y devuelve su contenido como lista. Si no existe, devuelve `[]`. |
| `escribir_json("locales.json", datos)` | Sustituye el contenido del archivo por `datos`. |

Cada modelo las usa con su propio archivo y convierte entre **diccionario**
(lo que va al JSON) y **objeto** (lo que usa el resto del código):

```
locales.json  ──leer_json──►  lista de diccionarios  ──Local(...)──►  lista de objetos Local
locales.json  ◄─escribir_json─ lista de diccionarios ◄─a_diccionario()─ lista de objetos Local
```

Para **cambiar** un dato siempre se hace lo mismo: leer la lista entera →
cambiarla en memoria → escribir la lista entera.

---

## 6. CRUD de locales

| Letra | Operación | Función en `local_controller.py` | Quién puede |
|---|---|---|---|
| C | Crear | `crear()` | Autoridad |
| R | Leer | `listar()`, `buscar()` | Todos |
| U | Actualizar | `modificar()` | Autoridad (todos) / Propietario (el suyo) |
| D | Borrar | `eliminar()` | Autoridad |

Cada operación sigue los mismos pasos:
1. **Permiso**: llama a `puede_crear` / `puede_editar` / `puede_eliminar`.
2. **Limpieza**: quita espacios y pone el código en mayúsculas.
3. **Validación**: `validar()` comprueba que no falten datos y que el aforo sea un número mayor que 0.
4. **Guardar**: lee la lista, la cambia y la vuelve a escribir.
5. **Respuesta**: devuelve `(local, "")` si ha ido bien o `(None, "mensaje de error")` si no.

Los permisos se comprueban **en el controlador**, no solo escondiendo botones
en la vista. Así, aunque alguien llamase a la función directamente, la regla se cumple.

---

## 7. Recorridos completos

### Registrar a un propietario

```
RegisterView                          LoginController.registrar()             Modelo
───────────                           ───────────────────────────             ──────
Elige rol "Propietario"
 └─ cambiar_rol() muestra la caja
    "Código de negocio"
Pulsa "Registrarme" ───────────────►  comprobaciones comunes
                                      ¿código vacío?           → error
                                      LocalController.buscar() ──────────────► locales.json
                                      ¿no existe?              → error
                                      buscar_por_codigo_negocio() ───────────► usuarios.json
                                      ¿ya tiene dueño?         → error
                                      crear_usuario(..., codigo_negocio) ───► usuarios.json
app.entrar(usuario)  ◄──────────────  (usuario, "")
```

El registro de la **Autoridad** es igual, pero comprueba el ID contra
`ids_policiales.json` y lo guarda en `id_policial`.

### Editar un local

```
LocalesView: botón "Editar" (solo si puede_editar)
  └─ app.ir_a_editar_local(local)
       └─ LocalFormView con las cajas rellenas (código bloqueado)
            └─ "Guardar" → LocalController.modificar()
                              ├─ puede_editar()   (vuelve a comprobar el permiso)
                              ├─ validar()
                              └─ guardar_locales() ──► locales.json
            └─ si va bien → app.ir_a_locales() (lista actualizada)
```

---

## 8. Cómo probarlo

```bash
python -m pip install -r requirements.txt
python main.py
```

Usuarios de prueba y códigos: ver [`ROLES.md`](ROLES.md#usuarios-de-prueba).

> Si vienes del Sprint 1 y ya tenías `src/models/usuarios.json`, bórralo para
> que se vuelva a crear con los usuarios de prueba nuevos (el propietario de
> prueba necesita estar unido al local `NEG-001`).
