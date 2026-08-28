#!/usr/bin/env bash
# overnight_noise_floor.sh — réplicas del mismo prompt para medir el piso de ruido.
#
# Cada corrida repite un prompt YA corrido, sobre los mismos 30 videos, con el
# mismo World Model de Stage 1 en caché. La diferencia verdadera entre dos
# corridas es cero por construcción, así que lo que midan es ruido de la API.
#
# El orden importa: si la cuota se agota a mitad de camino, lo que ya corrió
# alcanza para responder la pregunta principal. Las tres primeras son réplicas
# del prompt de producción; la cuarta cambia de prompt para verificar que el
# piso de ruido no dependa de cuál se use.
#
#   bash scripts/ablation/overnight_noise_floor.sh            # solo corre
#   bash scripts/ablation/overnight_noise_floor.sh --poweroff # y apaga al terminar
#
# Es reanudable: cada réplica tiene su propio checkpoint, así que si algo se
# corta, volver a lanzar el script retoma solo los videos que faltan.
set -uo pipefail

cd "$(dirname "$0")/../.." || exit 1
PY=.venv/bin/python
STAMP=$(date +%Y-%m-%d_%H%M)
LOG="reports/ablation/overnight_${STAMP}.log"
mkdir -p reports/ablation

POWEROFF=0
[[ "${1:-}" == "--poweroff" ]] && POWEROFF=1

# prompt|réplica
#
# Tres réplicas del prompt de producción. Con la corrida que ya existe en
# reports/ablation son cuatro ejecuciones del mismo texto sobre el mismo panel,
# o sea seis comparaciones nulas — suficiente para dibujar la banda de ruido.
#
# Quedaron afuera, por si algún día sobra cuota: una réplica de
# stage2_v0_baseline__cell8.txt (verificaría que el piso de ruido no sea propio
# del prompt de producción) y una quinta réplica de producción.
JOBS=(
  "stage2_v6_corrected__cell9.txt|2"
  "stage2_v6_corrected__cell9.txt|3"
  "stage2_v6_corrected__cell9.txt|4"
)

say() { echo -e "$*" | tee -a "$LOG"; }

say "=== cola de réplicas iniciada $(date -Is) ==="
say "jobs: ${#JOBS[@]} × 30 llamadas = $(( ${#JOBS[@]} * 30 )) llamadas Stage 2"
say "log: $LOG\n"

FAILED=""
for job in "${JOBS[@]}"; do
  prompt="${job%%|*}"
  rep="${job##*|}"
  say "\n--- $(date +%H:%M:%S)  $prompt  réplica $rep ---"
  $PY scripts/ablation/rerun_panel.py \
      --prompt "$prompt" --panel 30 --replicate "$rep" >>"$LOG" 2>&1
  code=$?
  if [[ $code -ne 0 ]]; then
    # Salida 2 = panel incompleto (cuota agotada o 503 persistente). Seguir con la
    # próxima solo gastaría llamadas contra la misma pared, y el checkpoint ya
    # guardó lo hecho.
    say "!! $prompt rep$rep terminó con código $code — corto la cola acá."
    say "   Volvé a lanzar el mismo script cuando se renueve la cuota: retoma donde quedó."
    FAILED="$prompt rep$rep"
    break
  fi
  say "   ok"
done

say "\n--- $(date +%H:%M:%S) análisis del piso de ruido ---"
$PY scripts/ablation/measure_noise_floor.py 2>&1 | tee -a "$LOG"

say "\n=== cola terminada $(date -Is) ${FAILED:+(incompleta: $FAILED)} ==="

if [[ $POWEROFF -eq 1 ]]; then
  say "Apagando en 60 s. Cancelá con Ctrl-C si estás mirando."
  sleep 60
  systemctl poweroff || say "systemctl poweroff falló — la PC queda encendida."
fi
