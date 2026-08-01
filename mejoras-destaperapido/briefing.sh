#!/bin/bash
# briefing.sh — ARRANQUE EN FRÍO de una sesión de Claude Code en dixdybot.
#
# Para qué: un chat nuevo (o otra cuenta del Mac) no sabe nada de lo anterior. Esto le
# pone en pantalla el estado VIVO en un solo comando — con qué cuenta corre, si los
# paneles respiran, qué se commiteó último, qué preguntas están esperando al dueño y
# dónde están los planes de cada carril. Lo escrito en los .md dice el rumbo; esto dice
# la realidad de este minuto.
#
# Uso:  bash mejoras-destaperapido/briefing.sh          (instantáneo)
#       bash mejoras-destaperapido/briefing.sh --tests   (además corre tsc + vitest)
set -u

MOLDE="$HOME/SaSS/DIXDY/dixdybot"
CLON="$HOME/SaSS/DIXDY/clientes/destaperapido"
DATOS="$HOME/SaSS/DIXDY/clientes/destaperapido/dixdybot-data"

echo "═══ dixdybot · briefing $(date '+%d-%m-%Y %H:%M') ═══"

# ── 1 · con qué cuenta se está corriendo (cada una tiene su memoria e historial) ──
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CUENTA=$(python3 - "$CFG" <<'PY' 2>/dev/null || echo "(desconocida)"
import json, sys
try:
    print(json.load(open(sys.argv[1] + '/.claude.json'))['oauthAccount']['emailAddress'])
except Exception:
    print('(desconocida)')
PY
)
echo "▸ Cuenta: $CUENTA   ·   config: $CFG"

# ── 2 · los dos paneles (mismo molde, dos instancias en vivo) ──
for PUERTO in 8793 8794; do
  SALUD=$(curl -s -m 3 "http://127.0.0.1:$PUERTO/api/salud" 2>/dev/null)
  if [ -z "$SALUD" ]; then
    SUFIJO=""; [ "$PUERTO" = 8794 ] && SUFIJO="-dixdy"
    echo "▸ Panel $PUERTO: ✗ NO RESPONDE  (arrancar: launchctl kickstart -k gui/$(id -u)/com.dixdy.dixdybot-panel$SUFIJO)"
  else
    # el resumen se arma en python por STDIN: con python3 -c el shell expande las
    # llaves del f-string y sale basura multiplicada (pasó de verdad)
    RESUMEN=$(printf '%s' "$SALUD" | python3 -c 'import json,sys
d = json.load(sys.stdin); b = d.get("db", {})
print("%s · %s chats · %s pedidos · %s dudas" % (d.get("negocio","?"),
      b.get("conversaciones",0), b.get("pedidos",0), b.get("dudas",0)))' 2>/dev/null)
    echo "▸ Panel $PUERTO: ✓ ${RESUMEN:-vivo}"
  fi
done

# ── 3 · lo que espera al dueño AHORA (las dudas vivas del cliente que paga) ──
if [ -f "$DATOS/bot.db" ]; then
  echo "▸ Preguntas esperándote en destaperapido:"
  # la pregunta vive DENTRO de payload (JSON), no en una columna suya
  sqlite3 "$DATOS/bot.db" \
    "SELECT '   · ' || id || ' (' || fase || ') · '
            || substr(coalesce(json_extract(payload, '\$.pregunta'), '?'), 1, 64)
       FROM dudas WHERE fase <> 'resuelta' ORDER BY creada_ts DESC LIMIT 6" 2>/dev/null \
    || echo "   (no pude leer la base)"
fi

# ── 4 · lo último que se hizo, en los dos carriles ──
echo "▸ Últimos commits del molde:"
git -C "$MOLDE" log --oneline -6 2>/dev/null | sed 's/^/   /'
SUCIO=$(git -C "$MOLDE" status --short -- src panel 2>/dev/null | head -5)
[ -n "$SUCIO" ] && { echo "▸ ⚠ Hay cambios SIN COMMITEAR en el molde (¿otra sesión trabajando?):"; echo "$SUCIO" | sed 's/^/   /'; }

# ── 5 · los planes: qué sigue en cada carril (el rumbo vive en los .md) ──
echo "▸ Planes vigentes (lee el que corresponda al carril que te toque):"
for DOC in RETOMAR-AQUI.md auditoria-backend-2026-07-30.md onboarding-dueno-nuevo.md \
           auditoria-ux-29jul/informe.md DIXDYBOT-ESTADO.md; do
  [ -f "$CLON/mejoras-destaperapido/$DOC" ] && echo "   · mejoras-destaperapido/$DOC"
done

# ── 6 · el candado: verde o no hay commit (opcional, ~20 s) ──
if [ "${1:-}" = "--tests" ]; then
  echo "▸ Corriendo el candado (tsc + vitest + verificadores del front)…"
  ( cd "$MOLDE" && pnpm exec tsc --noEmit && pnpm exec vitest run 2>&1 | grep -E "Tests |Test Files" )
  ( cd "$MOLDE/panel/pwa" && for f in _probar-*.cjs; do
      node "$f" >/dev/null 2>&1 && echo "   ✓ $f" || echo "   ✗ $f"; done )
else
  echo "▸ Candado sin correr. Para verlo: bash mejoras-destaperapido/briefing.sh --tests"
fi

echo "═══ fin del briefing ═══"
