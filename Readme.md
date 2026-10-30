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

**Sprint 1**

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
| RNF-05 | Seguridad básica (hash SHA-256 + salt) | ✅ |

### Estructura del proyecto (MVC)

```
Proyecto-Informatica-Grupo5/
├── main.py                       # Punto de entrada (arranca Flet)
├── requirements.txt
└── src/
    ├── app.py                    # Controlador de aplicación / enrutador de vistas
    ├── models/                   # MODELO
    │   ├── usuario.py            # Entidad Usuario + enum Rol
    │   └── usuarios.json         # Almacén (se genera al arrancar)
    ├── controllers/              # CONTROLADOR
    │   ├── user_controller.py    # Persistencia JSON + seguridad (hash/salt)
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

## Repositorio

Proyecto académico desarrollado para la asignatura de Informática.
