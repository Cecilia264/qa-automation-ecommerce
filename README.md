# QA Automation — e-Commerce

Framework de automatización de pruebas para una plataforma de comercio electrónico, construido en Python con **pytest**, **Playwright** y **requests**. El proyecto cubre pruebas de interfaz de usuario, validaciones a nivel de API y flujos end-to-end, con una estructura pensada para escalar y para integrarse en un pipeline de CI/CD.

---

## 1. Objetivo

Proveer una base mantenible, legible y reproducible para automatizar la validación funcional y de regresión del e-Commerce, reduciendo el esfuerzo de prueba manual y entregando retroalimentación temprana sobre la calidad del producto.

## 2. Alcance

### Incluido

| Área | Descripción |
| --- | --- |
| **UI / E2E** | Flujos de navegación, autenticación, catálogo, búsqueda, carrito y checkout mediante Playwright en Chromium, Firefox y WebKit. |
| **API** | Validación de contratos, códigos de estado, esquemas de respuesta y reglas de negocio usando `requests`. |
| **Integración** | Verificación de coherencia entre lo mostrado en la UI y los datos devueltos por la API. |
| **Regresión** | Suite etiquetada por criticidad (`smoke`, `regression`) ejecutable en cada release. |
| **Reportes** | Salida en consola, log por ejecución y resultados JUnit XML compatibles con CI. |

### Excluido (por ahora)

- Pruebas de rendimiento, carga y estrés (se recomienda Locust o k6 en una iniciativa aparte).
- Pruebas de seguridad y penetración.
- Compatibilidad con dispositivos móviles nativos.
- Automatización de back-office o paneles administrativos.
- Validación visual por comparación de imágenes (puede incorporarse más adelante).

## 3. Stack tecnológico

| Herramienta | Versión | Rol |
| --- | --- | --- |
| Python | 3.11+ | Lenguaje base |
| pytest | ≥ 8.0, < 10.0 | Runner y framework de aserciones |
| pytest-playwright | ≥ 0.6, < 1.0 | Fixtures de navegador y gestión de Playwright |
| Playwright | Última estable | Automatización de navegadores |
| requests | ≥ 2.32, < 3.0 | Cliente HTTP para pruebas de API |

## 4. Estructura del proyecto

```text
Proyecto QA Automation e-Commerce/
├── pages/
│   └── login_page.py        # Page Object Model de la pantalla de login
├── tests/
│   ├── conftest.py          # Fixtures compartidas (api_session)
│   ├── test_smoke.py        # Prueba de humo de referencia
│   ├── api/
│   │   └── test_auth_api.py # Login exitoso/fallido contra reqres.in
│   └── ui/
│       └── test_login_ui.py # Login de SauceDemo con Playwright
├── reports/                 # Logs y artefactos de ejecución (generado)
├── pytest.ini               # Configuración central de pytest y Playwright
├── requirements.txt         # Dependencias del proyecto
├── .gitignore
└── README.md
```

Patrón de diseño:

- **Page Object Model (POM):** cada pantalla se representa con una clase en `pages/` que expone acciones de negocio (`login`, `open`) y aserciones reutilizables (`expect_error`, `expect_successful_login`). Los tests no contienen selectores ni detalles del DOM.

Convenciones de nombres:

- Archivos: `test_<módulo>.py`
- Clases: `Test<Componente>`
- Funciones: `test_<comportamiento_esperado>`
- Marcadores: `smoke`, `ui`, `api`, `e2e`, `slow`, `regression`

A medida que el suite crezca, se sugiere incorporar:

```text
pages/      # Page Object Model (una clase por pantalla)
api/        # Clientes y helpers de la API
utils/      # Utilidades transversales (datos, fechas, generadores)
data/       # Datos de prueba y fixtures estáticos
```

## 5. Requisitos previos

- Python 3.11 o superior.
- Git (opcional, para control de versiones).
- Acceso de red al entorno bajo prueba.

## 6. Instalación

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Descargar los binarios de los navegadores
playwright install
```

> En servidores de CI se recomienda `playwright install --with-deps chromium` para reducir tiempos de ejecución.

## 7. Ejecución de pruebas

```bash
# Suite completa
pytest

# Solo pruebas de humo
pytest -m smoke

# Capas por separado
pytest tests/api
pytest tests/ui

# Solo pruebas de API
pytest -m api

# Excluir pruebas lentas
pytest -m "not slow"

# Ejecutar un archivo o una prueba puntual
pytest tests/test_smoke.py
pytest tests/test_smoke.py::test_login_page_is_available

# Cambiar el entorno bajo prueba
pytest --base-url https://staging.example.com

# Ejecutar en varios navegadores
pytest --browser chromium --browser firefox --browser webkit

# Modo con navegador visible (útil para depurar)
pytest --headed --slowmo 250

# Trazar la ejecución para el Playwright Inspector
pytest --tracing on
```

## 8. Configuración

La configuración central vive en `pytest.ini`:

| Clave | Valor por defecto | Descripción |
| --- | --- | --- |
| `testpaths` | `tests` | Directorio de descubrimiento |
| `base_url` | `https://www.saucedemo.com` | Entorno bajo prueba (sobrescribible con `--base-url`) |
| `addopts` | `-v --strict-markers --tb=short` | Salida detallada y marcadores estrictos |

El navegador se selecciona por línea de comandos (`--browser`); Playwright usa `chromium` por defecto.

Los marcadores personalizados están registrados en `pytest.ini`; usar un marcador no declarado provoca un error gracias a `--strict-markers`.

## 9. Reportes y evidencias

- **Consola:** resumen detallado de cada prueba.
- **Log:** `reports/pytest.log` (nivel INFO).
- **JUnit XML:** `pytest --junitxml=reports/junit.xml`, consumible por Jenkins, GitLab CI o GitHub Actions.
- **Trazas de Playwright:** `pytest --tracing on`; los archivos se guardan en `test-results/`.

Ejemplo de integración en CI:

```yaml
- name: Run test suite
  run: |
    pip install -r requirements.txt
    playwright install --with-deps chromium
    pytest -m "smoke or api" --junitxml=reports/junit.xml
```

## 10. Buenas prácticas del proyecto

1. **Independencia:** cada prueba debe poder ejecutarse de forma aislada y en cualquier orden.
2. **Determinismo:** evitar dependencias de datos cambiantes; preparar y limpiar el estado vía fixtures.
3. **Selectores estables:** priorizar `data-testid`, roles accesibles y etiquetas visibles antes que XPath o CSS frágil.
4. **Esperas explícitas:** usar las aserciones autoesperadas de Playwright (`expect`) en lugar de `sleep`.
5. **Datos sensibles:** nunca versionar credenciales; usar variables de entorno o gestores de secretos.
6. **Trazabilidad:** toda prueba debe mapear a un requisito o caso de prueba identificable.
7. **Revisión:** los cambios en el suite se revisan mediante pull request, igual que el código de producto.

## 11. Roadmap

- [x] Implementar Page Object Model para las pantallas principales.
- [ ] Añadir capa de clientes de API con validación de esquemas.
- [ ] Parametrizar datos de prueba por entorno.
- [ ] Integrar reporte HTML (`pytest-html`) y publicación de artefactos.
- [ ] Ejecución paralela con `pytest-xdist`.
- [ ] Pipeline de CI con ejecución nocturna de regresión.

## 12. Contribución

1. Crear una rama descriptiva: `feature/<area>-<descripcion>`.
2. Añadir o actualizar las pruebas junto con su documentación.
3. Ejecutar localmente `pytest -m smoke` antes de abrir el pull request.
4. Solicitar revisión a un miembro del equipo de QA.

## 13. Licencia

Uso interno del equipo de Quality Assurance. Todos los derechos reservados.
