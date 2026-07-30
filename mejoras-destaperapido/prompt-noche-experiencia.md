# Prompt de noche — carril EXPERIENCIA (el robot guía y el dueño nuevo)

> **Hermano de `prompt-noche.md`, que es el del carril BACKEND.** Elige UNO para la noche:
> los dos escriben en el mismo molde y se pisarían en los commits. Si de verdad quieres
> los dos a la vez, el segundo trabaja en un árbol aparte:
> `git -C ~/SaSS/DIXDY/dixdybot worktree add /tmp/dixdybot-noche -b noche-experiencia`.

**Cómo se lanza** (en una terminal que puedas dejar abierta):

```bash
cd ~/SaSS/DIXDY/clientes/destaperapido
claude982 --permission-mode bypassPermissions      # o claude98, la cuenta con cupo
```

Dentro: `/model fable` y pegar el prompt de abajo tal cual. `bypassPermissions` es lo que
evita que se quede pegado a las 3 AM esperando un permiso; la red de seguridad no es el
permiso, es que **cada pieza va en su propio commit con los tests verdes**.

---

## El prompt (copiar de aquí para abajo)

/loop Trabajas solo toda la noche en dixdybot. Nadie te va a contestar hasta la mañana: si
algo necesita una decisión de Alejandro, NO preguntes — anótalo en el diario y sigue con lo
siguiente.

ARRANQUE (una sola vez): corre `bash mejoras-destaperapido/briefing.sh --tests` y lee
`mejoras-destaperapido/RETOMAR-AQUI.md`, `mejoras-destaperapido/onboarding-dueno-nuevo.md` y
`mejoras-destaperapido/auditoria-ux-29jul/informe.md`. Tu carril es EXPERIENCIA DEL DUEÑO
NUEVO.

LA IDEA MADRE, en una frase: el panel tiene que sentirse como un juego que te enseña a
jugar, con un robot 🤖 que acompaña, explica y destaca — pensado para una persona que no
sabe nada de tecnología y quiere que su WhatsApp atienda solo. La Fase A ya está en vivo
(robot flotante con memoria propia, su mano para llevarte y destacar vistas, bienvenida por
vista, y la limpieza de palabras técnicas). Falta la B y la C.

ORDEN DE TRABAJO — una cosa por vuelta, en este orden, sin inventar otras:

1. **Fase B · el celular de verdad** (lo medí con navegador a 390px; es lo más urgente):
   a) el menú son 8 iconos SIN texto → barra inferior tipo app con etiquetas (Hoy · Chats ·
      Agentes · Caminos · Más), respetando que en pantalla ancha nada cambie;
   b) **la ficha del chat en móvil no tiene la cara del Agente**: desde el teléfono no se
      puede hablar con el agente ni resolver la duda inline. Es lo más grave del carril,
      porque el celular es donde el dueño ayuda al bot;
   c) el hero/estreno de Agentes queda invisible detrás de la lista en pantalla chica;
   d) el hilo tiene que abrir pegado al último mensaje.
2. **Fase C · personalizar dixdy conversando** (nada técnico para el dueño):
   a) la conversación «cuéntame de tu negocio» donde el robot ESCRIBE los ajustes por él
      (nombre del negocio, primer agente, tono) — con el patrón de manos que ya existe;
   b) las 3 misiones (contrata → simula → conecta) tomando el centro de Hoy cuando el
      negocio está recién nacido, con su progreso real;
   c) celebración corta al completar una misión y al aprender el primer camino;
   d) las novedades contadas por el personaje **PORTANDO** el sistema «novedades ✨» que ya
      existe en `panel-cliente/` del maestro — no lo reinventes;
   e) el texto que explica las 2 conexiones de WhatsApp (rápida gratis vs oficial de Meta) y
      la primera prueba guiada del simulador.
3. Si sobra noche: lo de «quitar para que abrume menos» y las animaciones sobrias del §
   correspondiente del informe de UX, de menor a mayor riesgo.

LEY DE CADA PIEZA:
- Pasos chicos. Cada pieza terminada = su propio commit, con mensaje en español que explique
  el PORQUÉ (no el qué).
- `pnpm exec tsc --noEmit`, `pnpm exec vitest run` y los 6 `node panel/pwa/_probar-*.cjs` en
  VERDE o no hay commit. Todo lo que agregues lleva su test.
- **Verifica el celular DE VERDAD**: navegador a 390×844, captura, y míralas antes de decir
  que algo quedó listo. Nada de «debería verse bien».
- Respeta `prefers-reduced-motion` en toda animación nueva, y los tokens de `tokens.css`
  (nada de tamaños ni duraciones escritos a mano: los verificadores lo cazan).
- Si algo queda rojo y no lo arreglas en 3 intentos: revierte esa pieza, anótalo en el diario
  y pasa a la siguiente.
- Nunca termines una vuelta con el repo sucio: o commiteas, o reviertes.
- Reinicia los dos paneles SOLO con el candado verde
  (`launchctl kickstart -k "gui/$(id -u)/com.dixdy.dixdybot-panel"` y `…-panel-dixdy`) y
  comprueba con `curl` que responden antes de seguir.

PROHIBIDO, sin excepciones:
- Escribirle a un cliente real. Para probar, SOLO el canal `sim:` del simulador.
- Responder o decidir las dudas abiertas (`prjst`, `baffe`, `ockbe`): son decisiones de plata
  de Alejandro.
- Tocar `~/SaSS/destaperapido/whatsapp-bot/` (el bot que vende hoy).
- Tocar lo del OTRO carril (`auditoria-backend-2026-07-30.md`, `puntos_restauracion`, la
  vista de Precios, `core/config.ts`): hay otra sesión trabajando ahí.
- Agregar columnas a tablas existentes de `src/db/esquema.sql` (tablas NUEVAS sí).
- `git push`, borrar datos de cualquier instancia, comprar o contratar nada, tocar la API key.
- Cambiar ajustes reales de destaperapido (precios, tarifario, horarios).

DIARIO — es lo primero que Alejandro va a leer en la mañana. Al terminar CADA pieza actualiza
`mejoras-destaperapido/diario-noche-experiencia.md`, en simple y sin tecnicismos: qué quedó
funcionando y cómo lo comprobaste (con la captura), qué quedó a medias y por qué, qué necesita
su decisión, y en qué commit quedó cada cosa. Que se lea como el parte de un colega que
trabajó de noche, no como un log.

Registra lo hecho con `python3 ~/SaSS/DIXDY/scripts/actividad.py`. Cuando termines el orden
completo, para y cierra el diario con un resumen de una página.
