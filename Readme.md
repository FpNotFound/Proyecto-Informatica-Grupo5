# Proyecto Informática - Grupo 5

## Descripción

Repositorio oficial del proyecto deinformatica del Grupo 5.

La gestión del proyecto se realiza siguiendo la metodología ágil Scrum y utilizando Git y GitHub como sistema de control de versiones.

---

## Estructura de ramas

El proyecto se organiza mediante las siguientes ramas:

### MAIN
Contiene únicamente las versiones estables de cada sprint y los tags asociados a las entregas.

### PRODUCTION
Contiene exclusivamente versiones publicadas provenientes de la rama MAIN.

### DEVELOPMENT
Rama principal de desarrollo e integración del proyecto. Todas las nuevas funcionalidades se integran aquí antes de pasar a MAIN.

### Ramas de los integrantes
Cada miembro del equipo dispone de una rama individual derivada de DEVELOPMENT para desarrollar sus tareas asignadas.

Ejemplos:

- Mariana
- Jimena
- Sara
- integrante-4

---

## Equipo de trabajo

| Integrante | Rol |
|------------|------|
| Mariana | Scrum Master |
| Jimena | Developer |
| Sara | Developer |

---

## Metodología de trabajo

1. Cada integrante trabaja en su propia rama.
2. Los cambios se integran en DEVELOPMENT mediante Pull Requests.
3. DEVELOPMENT se fusiona en MAIN al finalizar cada sprint.
4. MAIN se publica en PRODUCTION cuando la versión es estable.

---

## Sprint Actual

**Sprint 2**

Cada integrante dispone de un archivo identificativo con su nombre y la tarea asignada para este sprint.

---

## Tecnologías

- Python 3
- [Flet](https://flet.dev/) (interfaz gráfica responsive)
- Almacenamiento local en JSON
- Arquitectura Modelo-Vista-Controlador (MVC)
- Git y GitHub
- Metodología Scrum

---

## Aplicación — Sprint 1 (Estructura base y autenticación)

Aplicación del **Sistema de Monitorización Ambiental "Bajos de Argüelles"**.
Esta primera entrega implementa la estructura MVC, el registro e inicio de
sesión de usuarios con diferenciación por rol y la navegación básica entre
pantallas.

### Alcance cubierto

| Código | Requisito | Estado |
|--------|-----------|--------|
| RF-01 | Registro de usuarios | ✅ |
| RF-02 | Inicio de sesión | ✅ |
| RF-03 | Almacenamiento mediante JSON | ✅ |
| RF-04 | Navegación entre pantallas | ✅ |
| RF-05 | Arquitectura MVC | ✅ |
| RF-06 | Diseño inicial de interfaz gráfica | ✅ |
| RNF-05 | Seguridad básica (hash SHA-256) | ✅ |

### Estructura del proyecto (MVC)

```
Proyecto-Informatica-Grupo5/
├── main.py                       # Punto de entrada (arranca Flet)
├── requirements.txt
└── src/
    ├── app.py                    # Controlador de aplicación / enrutador de vistas
    ├── models/                   # MODELO
    │   ├── usuario.py            # Usuario, roles y lectura/escritura del JSON
    │   └── usuarios.json         # Almacén (se genera al arrancar)
    ├── controllers/              # CONTROLADOR
    │   ├── user_controller.py    # Alta y búsqueda de usuarios + hash SHA-256
    │   └── login_controller.py   # Lógica de registro e inicio de sesión
    └── views/                    # VISTA
        ├── login_view.py         # LoginView
        ├── register_view.py      # RegisterView
        └── main_view.py          # MainView
```

### Puesta en marcha

```bash
# 1. Instalar dependencias
python -m pip install -r requirements.txt

# 2. Ejecutar la aplicación
python main.py
```

Al arrancar por primera vez se crea `src/models/usuarios.json` con tres
usuarios de demostración (uno por rol). Credenciales de prueba:

| Rol | Correo | Contraseña |
|-----|--------|------------|
| Vecino | `vecino@arguelles.es` | `1234` |
| Propietario | `bar@arguelles.es` | `1234` |
| Autoridad | `ayto@arguelles.es` | `1234` |

También es posible registrar nuevos usuarios desde la propia aplicación.

> Los paneles (dashboards) específicos por rol con los datos de sensores se
> desarrollarán en el Sprint 3. En el Sprint 1 la pantalla principal muestra
> una bienvenida con el rol del usuario y un adelanto de dichos paneles.

---

## Aplicación — Sprint 2 (Roles, CRUD de locales y JSON)

### Alcance cubierto

| Tarea | Estado |
|-------|--------|
| Modificación de roles y funciones especiales | ✅ |
| Operaciones CRUD para la gestión de locales | ✅ |
| Lectura y escritura en JSON locales | ✅ |
| Documentación explícita de los roles | ✅ |

### Novedades

- **Registro por rol.** Los **Propietarios** deben introducir el *código de
  negocio* de su local, y la **Autoridad** su *ID de identificación policial*.
  Los Vecinos se registran igual que antes.
- **CRUD de locales.** La Autoridad crea, edita y elimina locales. El
  Propietario edita solo el suyo, y el Vecino solo puede verlos.
- **JSON.** Toda la lectura y escritura pasa por `src/models/archivo_json.py`.
  Los datos se guardan en `usuarios.json`, `locales.json` e `ids_policiales.json`.
- **Código comentado línea a línea** para que se entienda sin saber mucho Python.

### Documentación

- [`docs/ROLES.md`](docs/ROLES.md): qué pide y qué puede hacer cada rol, más los usuarios de prueba.
- [`docs/GUIA_DEL_CODIGO.md`](docs/GUIA_DEL_CODIGO.md): conceptos básicos de Python, arquitectura, JSON, CRUD y recorridos completos.

### Credenciales de prueba (Sprint 2)

| Rol | Correo | Contraseña | Código |
|-----|--------|------------|--------|
| Vecino | `vecino@arguelles.es` | `1234` | — |
| Propietario | `bar@arguelles.es` | `1234` | Negocio `NEG-001` |
| Autoridad | `ayto@arguelles.es` | `1234` | ID policial `POL-0001` |

IDs policiales libres para registrar nuevas autoridades: `POL-0002` a `POL-0005`.

> Si ya tenías `src/models/usuarios.json` del Sprint 1, bórralo para que se
> regenere con los nuevos usuarios de prueba.

---

## Repositorio

Proyecto académico desarrollado para la asignatura de Informática.
