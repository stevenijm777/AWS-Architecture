#!/bin/bash
# Run all three Cloudscape Streamlit architecture explorers on different ports

# Terminate background processes on script exit
trap "kill \$PID1 \$PID2 \$PID3 2>/dev/null; exit" INT TERM EXIT

echo "Starting Cloudscape Explorers..."

# Start Standard Explorer (Gemini)
.venv/bin/streamlit run cloudscape_explorer/explorer_gemini.py --server.port 8501 --server.address localhost &
PID1=$!

# Start Parsimonious Explorer
.venv/bin/streamlit run cloudscape_explorer/explorer_parsimonious.py --server.port 8502 --server.address localhost &
PID2=$!

# Start Ground Truth Explorer
.venv/bin/streamlit run cloudscape_explorer/explorer_gt.py --server.port 8503 --server.address localhost &
PID3=$!

echo "Explorers started successfully:"
echo "  * Gemini Standard (Standard):     http://localhost:8501"
echo "  * Gemini Parsimonious (Parsim.):  http://localhost:8502"
echo "  * Ground Truth (Manual GT):       http://localhost:8503"
echo ""
echo "Press Ctrl+C to stop all servers."

# Wait for all background processes to finish
wait
