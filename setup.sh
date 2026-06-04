#!/usr/bin/env bash
# ============================================================
# setup.sh — Cloud Architecture Extractor: Environment Setup
# ============================================================
# Detects distro (Arch/CachyOS vs Debian/Ubuntu) and installs
# system deps + Python venv + CUDA-enabled PyTorch + project deps
# ============================================================
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"

# ----------------------------------------------------------
# 1. Detect distro & install system dependencies
# ----------------------------------------------------------
install_system_deps() {
    log "Detecting Linux distribution..."

    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID="${ID:-unknown}"
        DISTRO_LIKE="${ID_LIKE:-}"
    else
        err "Cannot detect distribution. /etc/os-release not found."
    fi

    # Arch-based (CachyOS, Manjaro, EndeavourOS, etc.)
    if [[ "$DISTRO_ID" == "arch" || "$DISTRO_LIKE" == *"arch"* || "$DISTRO_ID" == "cachyos" ]]; then
        log "Arch-based distro detected ($DISTRO_ID). Using pacman..."
        sudo pacman -Syu --noconfirm --needed \
            python python-pip \
            ffmpeg \
            git \
            cuda cudnn          # NVIDIA CUDA toolkit

    # Debian-based (Ubuntu, Pop!_OS, Linux Mint, etc.)
    elif [[ "$DISTRO_ID" == "ubuntu" || "$DISTRO_ID" == "debian" || "$DISTRO_LIKE" == *"debian"* || "$DISTRO_LIKE" == *"ubuntu"* ]]; then
        log "Debian-based distro detected ($DISTRO_ID). Using apt..."
        sudo apt update
        sudo apt install -y \
            python3 python3-pip python3-venv \
            ffmpeg \
            git \
            nvidia-cuda-toolkit     # CUDA compiler + runtime

    else
        warn "Unknown distro: $DISTRO_ID (like: $DISTRO_LIKE)"
        warn "Please install manually: python3, pip, ffmpeg, git, cuda"
    fi

    ok "System dependencies installed."
}

# ----------------------------------------------------------
# 2. Create Python virtual environment
# ----------------------------------------------------------
create_venv() {
    if [ -d "$VENV_DIR" ]; then
        warn "Virtual environment already exists at $VENV_DIR"
        log "To recreate, delete it first:  rm -rf $VENV_DIR"
    else
        log "Creating virtual environment at $VENV_DIR ..."
        python3 -m venv "$VENV_DIR"
        ok "Virtual environment created."
    fi

    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
    log "Activated venv: $(which python)"
}

# ----------------------------------------------------------
# 3. Install PyTorch with CUDA support
# ----------------------------------------------------------
install_torch() {
    log "Installing PyTorch with CUDA 12.4 support (RTX 5070 Ti)..."
    pip install --upgrade pip
    pip install torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu124
    ok "PyTorch + CUDA installed."
}

# ----------------------------------------------------------
# 4. Install project Python dependencies
# ----------------------------------------------------------
install_python_deps() {
    log "Installing project dependencies from requirements.txt ..."
    pip install -r "${PROJECT_DIR}/requirements.txt"
    ok "All Python dependencies installed."
}

# ----------------------------------------------------------
# 5. Verify installation
# ----------------------------------------------------------
verify() {
    log "Verifying installation..."
    echo ""

    python -c "
import torch, whisper, yt_dlp, networkx as nx, google.genai
from PIL import Image

print('  ✓ PyTorch ........', torch.__version__)
print('  ✓ CUDA available .', torch.cuda.is_available())
if torch.cuda.is_available():
    print('  ✓ GPU ............', torch.cuda.get_device_name(0))
print('  ✓ Whisper ........', whisper.__version__)
print('  ✓ yt-dlp .........', yt_dlp.version.__version__)
print('  ✓ NetworkX .......', nx.__version__)
print('  ✓ google-genai ... OK')
print('  ✓ Pillow ......... OK')
"

    echo ""
    ffmpeg_ver=$(ffmpeg -version 2>/dev/null | head -1 || echo "NOT FOUND")
    echo "  ✓ FFmpeg ......... $ffmpeg_ver"
    echo ""
    ok "All checks passed! 🚀"
}

# ----------------------------------------------------------
# 6. Create .env template
# ----------------------------------------------------------
create_env_template() {
    ENV_FILE="${PROJECT_DIR}/.env"
    if [ ! -f "$ENV_FILE" ]; then
        log "Creating .env template..."
        cat > "$ENV_FILE" << 'EOF'
# ============================================================
# Cloud Architecture Extractor — Environment Variables
# ============================================================

# Google Gemini API Key (required for vision analysis)
GEMINI_API_KEY=your-api-key-here

# Whisper model size: tiny, base, small, medium, large, turbo
WHISPER_MODEL=turbo

# Frame extraction interval in seconds
FRAME_INTERVAL_SEC=10

# Video output quality for yt-dlp
VIDEO_FORMAT=bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]
EOF
        ok ".env template created. Edit it with your GEMINI_API_KEY."
    else
        warn ".env already exists — skipping."
    fi
}

# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║  Cloud Architecture Extractor — Setup               ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""

    install_system_deps
    create_venv
    install_torch
    install_python_deps
    create_env_template
    verify

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Setup complete! To activate the environment:"
    echo ""
    echo "    source ${VENV_DIR}/bin/activate"
    echo ""
    echo "  Then run the pipeline:"
    echo ""
    echo "    python main.py --url 'https://youtube.com/watch?v=...'"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

main "$@"
