# Guía del código — Sensores, alertas policiales y cierres

Esta parte de la aplicación añade:

1. **Sensores simulados en todos los bares** (temperatura, humedad y calidad del aire), guardados en JSON con su **historial**.
2. **Semáforo** en cada local: 🟢 verde, 🟡 amarillo o 🔴 rojo.
3. **LEDs de alerta**: 🔴 rojo por temperatura, 🔵 azul por humedad y 🟢 verde por calidad del aire.
4. **Ventilador**, que se enciende con más de 30 °C **y** el aire «Malo» a la vez.
5. **Alertas a la policía** cuando un bar llega a niveles peligrosos.
6. **Cierre temporal** de un bar por la policía, que antes tiene que escribir el motivo.
7. **Log de incidencias** de cada bar.
8. **Notificaciones** al propietario cuando cierran su bar, con el motivo.
9. **Reclamaciones**: el propietario reclama y la policía decide si el cierre fue justificado o no.

El código sigue el mismo estilo que el resto del proyecto: **MVC**, comentarios en cada bloque y lo más sencillo posible. Si no sabes nada de Python, lee primero los apartados 1 y 2 de `docs/GUIA_DEL_CODIGO.md`.

---

## 1. Cómo probarlo

Desde la carpeta `Proyecto-Informatica-Grupo5`:

```bash
python main.py
```

Se abre la aplicación de siempre (con el mismo login y los mismos usuarios), con el panel de sensores como pantalla principal. Usuarios de prueba (contraseña `1234`):

| Rol | Correo | Qué ver |
|---|---|---|
| Autoridad | `ayto@arguelles.es` | Alertas, cerrar bares, reclamaciones, bares cerrados |
| Propietario | `bar@arguelles.es` (local `NEG-001`) | «Mi local», avisos de cierre, botón de reclamación |
| Vecino | `vecino@arguelles.es` | Todos los bares con sus sensores |

**Prueba completa paso a paso:**

1. Entra como **Autoridad** → *Ver sensores e incidencias* en «Bar Demo» → **Forzar alerta** → pulsa **Actualizar medidas** 3 o 4 veces. Los valores suben, los LEDs se encienden, el semáforo se pone rojo y el ventilador se enciende.
2. **Volver** al panel: aparece una notificación y el bar sale en «Alertas de niveles peligrosos».
3. Pulsa **Cerrar temporalmente**, escribe el motivo (mínimo 20 letras) y confirma.
4. **Cerrar sesión** y entra como **Propietario**: verás el aviso del cierre con el motivo y el botón **Presentar reclamación**.
5. Escribe la reclamación, cierra sesión y entra otra vez como **Autoridad**: aparece en «Reclamaciones pendientes». Elige **Justificado** (el bar sigue cerrado) o **No justificado** (el bar se reabre). El propietario recibe la respuesta.
6. En el detalle del bar, el **Log de incidencias** muestra todo lo ocurrido.

---

## 2. Archivos

Todos están en `src`, junto al resto del código, y **ninguno se llama igual que un archivo que ya existía**:

```
main.py                               Arranca AppSensores
src/
├── app_sensores.py                   AppSensores: la App de siempre + pantallas nuevas
├── models/                           MODELO (datos y JSON)
│   ├── sensor.py                     Sensores, historial y UMBRALES
│   ├── simulador_sensores.py         Se inventa las medidas
│   ├── vigilancia.py                 Incidencias, cierres y notificaciones
│   ├── sensores.json                 Último valor de cada sensor (historial previo)
│   ├── historial_sensores.json       Lecturas de las últimas 24 horas (historial previo)
│   ├── incidencias.json              Log de incidencias (historial previo)
│   └── notificaciones.json           Avisos (historial previo)
├── controllers/                      CONTROLADOR (reglas)
│   ├── sensor_controller.py          Semáforo, LEDs, ventilador, medidas
│   └── vigilancia_controller.py      Alertas, cierres, reclamaciones, notificaciones
└── views/                            VISTA (pantallas)
    ├── piezas_sensores.py            Piezas repetidas: semáforo, LED, cartel, ventanita
    ├── panel_sensores_view.py        Panel principal según el rol
    ├── bar_sensores_view.py          Detalle de un bar
    └── locales_estado_view.py        Lista de locales de siempre + semáforo
```

**Orden recomendado de lectura:** `models/sensor.py` → `models/simulador_sensores.py` → `models/vigilancia.py` → `controllers/sensor_controller.py` → `controllers/vigilancia_controller.py` → `app_sensores.py` → las vistas.

### Cómo se une con el código que ya existía

De lo que ya existía solo cambian dos líneas de `main.py` (ahora arranca `AppSensores` en vez de `App`). Lo nuevo **usa** lo que ya había:

| Lo nuevo… | …usa lo que ya existía |
|---|---|
| Todos los modelos nuevos | `src/models/archivo_json.py` (`leer_json` / `escribir_json`) |
| `sensor_controller.py` | `src/models/local.py` (lista de locales: cada local tiene sensores) |
| `AppSensores` | **Hereda** de `App` (`src/app.py`): login, registro y formularios de locales |
| `LocalesEstadoView` | **Hereda** de `LocalesView`: mismos botones Editar/Eliminar, más el semáforo |
| `panel_sensores_view.py` | Textos de `src/views/main_view.py` |
| Permisos | Los roles de `usuario.py` (`Autoridad`, `Propietario`, `Vecino`) |

*Heredar* (`class AppSensores(App):`) significa «haz todo lo que hace `App` y cambia solo lo que yo diga». `super()` llama a la versión original.

Si se crea un local nuevo con el CRUD, al pulsar *Actualizar medidas* se le crean automáticamente sus 3 sensores. Si se elimina, sus sensores desaparecen.

---

## 3. Los archivos JSON (en `src/models`)

Todos los datos son **listas de diccionarios**, como `locales.json`.

| Archivo | Qué guarda | Ejemplo de un elemento |
|---|---|---|
| `sensores.json` | El **último** valor de cada sensor | `{"local": "NEG-001", "tipo": "temperatura", "valor": 23.4, "fecha": "2026-11-13 21:30"}` |
| `historial_sensores.json` | **Todas** las medidas anteriores (máx. 1500) | igual que el anterior |
| `incidencias.json` | El **log** de cada bar | `{"local": "NEG-001", "fecha": "...", "tipo": "Cierre temporal", "autor": "Ayuntamiento Demo (POL-0001)", "descripcion": "..."}` |
| `cierres.json` | Los cierres de la policía y su reclamación | `{"local": "NEG-001", "fecha": "...", "policia": "...", "motivo": "...", "activo": true, "reclamacion": "...", "estado_reclamacion": "Pendiente", "respuesta": ""}` |
| `notificaciones.json` | Avisos para la policía o para un propietario | `{"para": "Autoridad", "fecha": "...", "titulo": "...", "mensaje": "...", "leida": false}` |

- **Historial previo:** el proyecto ya trae `sensores.json`, `historial_sensores.json` (75 lecturas inventadas del Bar Demo: una por hora de las últimas 24 horas de cada sensor), `incidencias.json` (una alerta a medianoche y su normalización) y `notificaciones.json` (el aviso a la policía). Cada medida nueva se añade a estos archivos.
- Un bar que no tenga sensores (por ejemplo, uno creado con el CRUD) recibe automáticamente su **historial de 24 horas** (una medida por hora). Entre las 23:00 y la 01:59 el bar está lleno, así que en esas horas salen valores peligrosos.
- `cierres.json` no viene hecho: se crea solo cuando la policía cierra un bar.
- En `notificaciones.json`, `"para"` vale `"Autoridad"` (lo ven todos los policías) o un código de local como `"NEG-001"` (lo ve su propietario).

---

## 4. Reglas: semáforo, LEDs y ventilador (`sensor_controller.py`)

Todos los números están al principio de `models/sensor.py`. Si hay que cambiarlos, solo se cambian ahí.

| Sensor | 🟢 Verde | 🟡 Amarillo (precaución) | 🔴 Rojo (peligro) | LED |
|---|---|---|---|---|
| Temperatura | hasta 27 °C | de 27 a 30 °C | **más de 30 °C** | 🔴 rojo |
| Humedad | 35 % a 65 % | 30–35 % o 65–70 % | **menos de 30 % o más de 70 %** | 🔵 azul |
| Calidad del aire (CO2) | «Buena»: menos de 800 ppm | «Moderada»: 800–1199 ppm | **«Mala»: 1200 ppm o más** | 🟢 verde |

- **Semáforo del bar** = el peor color de sus 3 sensores.
- **LED**: se enciende cuando su sensor está en rojo.
- **Ventilador**: se enciende con temperatura > 30 °C **y** aire «Mala» (las dos cosas a la vez).

| Función | Qué devuelve |
|---|---|
| `color_sensor(tipo, valor)` | `"verde"`, `"amarillo"` o `"rojo"` |
| `color_bar(codigo)` | El color del bar |
| `leds(codigo)` | `{"rojo": True, "azul": False, "verde": True}` |
| `ventilador(codigo)` | `True` o `False` |
| `medir_todos()` | Toma una medida nueva en todos los bares |
| `forzar_alerta(codigo)` / `volver_normal(codigo)` | Hace que las próximas medidas de ese bar suban a peligro o vuelvan a lo normal |

Las medidas **no cambian solas**: cambian al iniciar sesión y cada vez que se pulsa **Actualizar medidas**. Los valores van cambiando poco a poco, como en un sensor real.

---

## 5. Policía, cierres y reclamaciones (`vigilancia_controller.py`)

Igual que `LocalController`, las funciones que cambian algo devuelven `""` si ha ido bien, o el texto del error. **Los permisos se comprueban aquí**, no solo escondiendo botones.

| Función | Quién | Qué hace |
|---|---|---|
| `revisar_alertas()` | Automático, tras cada medida | Si un bar pasa a **rojo**: lo apunta en su log y **avisa a la policía**. Si vuelve a la normalidad, lo apunta también. Solo avisa una vez por alerta. |
| `cerrar_local(usuario, codigo, motivo)` | Autoridad | Exige un **motivo de 20 letras como mínimo**. Guarda el cierre, lo apunta en el log y **avisa al propietario con el motivo**. |
| `reabrir_local(usuario, codigo, nota)` | Autoridad | Reabre el bar y avisa al propietario. |
| `reclamar(usuario, codigo, texto)` | Propietario de ese bar | Una reclamación por cierre. Queda «Pendiente» y **avisa a la policía**. |
| `resolver_reclamacion(usuario, codigo, justificado, respuesta)` | Autoridad | **Justificado**: el bar sigue cerrado. **No justificado**: el bar se reabre. El propietario recibe la respuesta. |
| `incidencias_de(codigo)` | Todos | El log del bar, lo más nuevo primero. |
| `notificaciones_de(usuario)` / `marcar_leidas(usuario)` | Autoridad y Propietario | Sus avisos. |

Recorrido de un cierre con reclamación:

```
Sensores en ROJO ─► revisar_alertas() ─► log "Nivel peligroso" + aviso a la POLICÍA
                                                     │
Policía: "Cerrar temporalmente" + motivo ─► cerrar_local() ─► log "Cierre temporal"
                                                     └──────► aviso al PROPIETARIO (con el motivo)
                                                                     │
Propietario: "Presentar reclamación" ─► reclamar() ─► log "Reclamación" + aviso a la POLICÍA
                                                                     │
Policía: "Justificado" ──────► sigue cerrado ─┐
Policía: "No justificado" ───► se reabre ─────┴► log "Resolución" + aviso al PROPIETARIO
```

---

## 6. Las pantallas

| Pantalla | Archivo | Quién | Qué tiene |
|---|---|---|---|
| Panel principal | `panel_sensores_view.py` | Todos | Botones *Gestionar locales* y *Actualizar medidas*; tarjetas de **todos los bares** con semáforo, valores, LEDs y ventilador |
| | | Autoridad | + Notificaciones, **Alertas de niveles peligrosos** (botón *Cerrar temporalmente*), **Reclamaciones pendientes**, **Bares cerrados** (botón *Reabrir*) |
| | | Propietario | + Notificaciones y **Mi local** (motivo del cierre y botón *Presentar reclamación*) |
| Detalle de un bar | `bar_sensores_view.py` | Todos | LEDs, ventilador, los 3 sensores con su historial, **log de incidencias** y simulador de pruebas. La policía también tiene aquí *Cerrar* y *Reabrir* |
| Lista de locales | `locales_estado_view.py` | Todos | La de siempre (CRUD) + semáforo, cartel de cerrado y botón *Ver sensores* |

`piezas_sensores.py` tiene `ventana_texto(...)`: la ventanita donde se escribe el motivo, la reclamación o la respuesta. Si el controlador devuelve un error (por ejemplo, un motivo demasiado corto), lo muestra en rojo y la ventana no se cierra.

`AppSensores.recargar()` vuelve a dibujar la pantalla que se está viendo después de cada acción.
