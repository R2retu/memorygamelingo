# Guía técnica Flet (0.80.5) para un Agente
## Proyecto base: Memory Game (Cloud Run + assets locales)

### Entorno confirmado
- **Python:** 3.13.11  
- **Flet:** 0.80.5  
- **Audio:** `flet-audio` 0.80.5  
- **Deploy:** Google Cloud (Cloud Run), ejecutando por `PORT` y `host=0.0.0.0`  
- **Assets locales:** `assets_dir="assets"` con rutas relativas:
  - Imágenes: `imagesp/*.png`
  - Audio: `audio/*.mp3`

---

## 1) Regla operativa del agente

### 1.1 No introducir cambios no solicitados
**Regla fija**
- Si el usuario pide “Ajusta X”, el agente **NO** debe modificar Y/Z “por mejora” sin autorización.
- Si un cambio es necesario para que funcione (bug), el agente debe:
  1) explicar el motivo,
  2) proponer el cambio mínimo,
  3) **pedir confirmación** si toca lógica del juego.

### 1.2 Cambios de lógica del juego: pedir permiso SIEMPRE
- Cambios de reglas (turnos, repetición, puntuación, IA) **siempre requieren confirmación** del usuario.

**Regla fija definida por el usuario (inmodificable):**
- Regla clásica memory: **si haces pareja, repites turno**; si fallas, pierdes el turno.
- Aplica para humano y Robokob.
- **Nunca se cambia.**

---

## 2) Entry-point correcto (Cloud Run)

**Nunca romper esto**
```py
import os
import flet as ft

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    ft.run(
        main,
        assets_dir="assets",
        host="0.0.0.0",
        port=port,
    )
```

**Regla**
- Los assets se referencian **solo** por rutas relativas a `assets/` (nunca rutas absolutas de Windows).

---

## 3) Routing / Views: “pantalla negra”

### Síntoma
- Se abre la app pero queda “negra” o sin contenido, sin traceback.

### Causa típica
- Uso de `page.views` sin render inicial estable.
- `page.go("/")` no siempre dispara el evento como se espera en ciertos runtimes.

### Solución estable
- Implementar `render_route(route: str)` y llamarlo al inicio.

Patrón:
- `page.on_route_change = route_change`
- `route_change -> render_route(e.route)`
- Al final: `render_route(page.route or "/")`

---

## 4) Error: “Control must be added to the page first”

### Síntoma
```
RuntimeError: ... Control must be added to the page first
```

### Causa
- Acceder a `self.page` dentro de `__init__()` de una `View` o control antes de estar montado.

### Soluciones
- Pasar `page` explícito: `GameView(page=page, ...)` y usar `self.page_ref`.
- O retrasar lógica dependiente de `page` (por ejemplo, en `page.on_resized`).

---

## 5) Compatibilidad Flet 0.80.5: atributos que fallan

### 5.1 `ft.alignment.center` no existe
- Usar `ft.Alignment(0, 0)`.

### 5.2 `ft.ImageFit` no existe
- Usar `fit="cover"` (string), o `ft.BoxFit.CONTAIN` donde aplique.

Regla del agente:
- Ante `AttributeError: module 'flet' has no attribute ...`,
  - preferir strings y clases básicas (`Alignment`, `BoxFit`),
  - evitar enums no disponibles.

---

## 6) Audio: “Unknown control: Audio”

### Síntoma
- Banner rojo “Unknown control: Audio” y/o no suena.

### Lección del proyecto original
- El original creaba instancias `fta.Audio(autoplay=True, src=...)` y **guardaba referencias** (lista) para evitar GC.

### Recomendación
- Respetar el patrón probado del proyecto (no “inventar” otra inserción del control) sin autorización.
- Si hay audios “montados”, primero ajustar tiempos; si persiste, proponer “stop previous before play” y pedir confirmación.

---

## 7) Consistencia de interfaces (contratos entre archivos)

### Problemas encontrados
- `Deck.build_from_items` inexistente.
- `AssetItem` inexistente.
- `Card` sin campo `key`.
- `AudioService` sin `play()`.
- `ResultsView` con firma distinta (no aceptaba `state=`).

### Regla del agente
- Definir y mantener contratos estables:
  - `AssetService.get_items(category) -> List[AssetItem]`
  - `Deck.build_from_items(items)`
  - `Card(id, key, image_src, audio_src, ...)`
  - `AudioService.play(src)`
  - `ResultsView(state, on_play_again, on_home)`

Checklist antes de correr:
- imports existen,
- firmas coinciden,
- rutas de assets relativas,
- `assets_dir="assets"` intacto.

---

## 8) Robokob: tiempos + regla clásica (inmodificable)

### 8.1 Tiempos del original (para audio y UX)
- Entre carta 1 y 2 de Robokob: **1.0 s**
- Mantener pausas para que el audio no se “encime”.

### 8.2 Regla fija del usuario
- Robokob repite turno **solo** si hace pareja.
- Nunca cambiar sin permiso (y el usuario fijó que es inmodificable).

---

## 9) UI HomeView: temas y paginación

### Requisito probado
- Mostrar 4 temas a la vez.
- Flechas muestran el siguiente “bloque” de 4 (paginación).
- No depender de scroll táctil si falla en desktop.

---

## 10) Reglas de oro para el agente
- Mantener `assets_dir="assets"` y rutas relativas.
- Mantener compatibilidad Cloud Run (host/port).
- No reescribir UI sin pedido.
- No cambiar reglas de Robokob sin confirmación (y la regla clásica es fija).
- Si hay discrepancia “original vs refactor”, priorizar el original.
- Validar contratos entre archivos antes de ejecutar.
