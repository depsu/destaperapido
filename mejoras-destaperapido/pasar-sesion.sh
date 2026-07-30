#!/bin/bash
# pasar-sesion.sh — pasa UNA conversación de Claude Code de una cuenta a la otra, en este
# mismo Mac, para seguirla donde quedó (no un resumen: la conversación entera).
#
# Por qué funciona: cada cuenta guarda sus conversaciones como archivos .jsonl sueltos en
# <config>/projects/<carpeta-del-proyecto>/<id>.jsonl. Copiar ese archivo a la otra cuenta
# la deja aparecer en su lista de /resume. El llavero del Mac ya recuerda las dos sesiones,
# así que no hay login de por medio.
#
#   bash mejoras-destaperapido/pasar-sesion.sh            # la última conversación de acá
#   bash mejoras-destaperapido/pasar-sesion.sh <id>       # una en particular
#
# CUÁNDO USARLO: para seguir la MISMA tarea a medio hacer (el otro chat despierta sabiendo
# todo lo hablado). Para empezar un trabajo nuevo conviene más el briefing: arranca limpio
# y con la mitad de contexto gastado. Los dos caminos son válidos, no compiten.
#
# OJO: copia lo que hay HASTA ESE SEGUNDO. Si la conversación de origen sigue viva, lo que
# hables después no viaja — vuelve a correrlo al terminar (sobrescribe, no duplica).
set -u

AQUI="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
case "$AQUI" in
  *".claude-ale98") OTRA="$HOME/.claude" ;;
  *)                OTRA="$HOME/.claude-ale98" ;;
esac
correo() { python3 -c "import json,sys;print(json.load(open(sys.argv[1]+'/.claude.json')).get('oauthAccount',{}).get('emailAddress','?'))" "$1" 2>/dev/null || echo '?'; }

# La carpeta del proyecto: la ruta actual con '/' y '.' vueltos '-' (así la nombra Claude Code)
PROY="$(pwd | sed 's|[/.]|-|g')"
DE="$AQUI/projects/$PROY"
A="$OTRA/projects/$PROY"
[ -d "$DE" ] || { echo "✗ Esta cuenta no tiene conversaciones guardadas de esta carpeta."; exit 1; }

if [ $# -ge 1 ]; then
  ORIGEN="$DE/$1.jsonl"
  [ -f "$ORIGEN" ] || { echo "✗ No encontré la conversación '$1' en esta cuenta."; exit 1; }
else
  ORIGEN="$(ls -t "$DE"/*.jsonl 2>/dev/null | head -1)"
  [ -n "$ORIGEN" ] || { echo "✗ No hay conversaciones guardadas de esta carpeta."; exit 1; }
fi
ID="$(basename "$ORIGEN" .jsonl)"

mkdir -p "$A"
cp "$ORIGEN" "$A/$ID.jsonl" || { echo "✗ No pude copiarla."; exit 1; }

echo "✓ Conversación copiada"
echo "   de : $(correo "$AQUI")"
echo "   a  : $(correo "$OTRA")"
echo "   id : $ID   ($(du -h "$ORIGEN" | cut -f1))"
echo
echo "Ahora, en una terminal nueva:"
case "$OTRA" in
  *".claude-ale98") echo "   claude98  --resume $ID --fork-session" ;;
  *)                echo "   claude982 --resume $ID --fork-session" ;;
esac
echo
echo "   (--fork-session le da un id nuevo: la conversación original queda intacta"
echo "    y las dos pueden seguir por su lado sin pisarse)"
