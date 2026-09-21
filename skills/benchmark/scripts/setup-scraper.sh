#!/bin/bash
# ============================================================
# setup-scraper.sh — One-time Crawl4AI installation
# Run once on your machine to enable full JS rendering
# Usage: bash .claude/skills/benchmark/scripts/setup-scraper.sh
# ============================================================

set -e

echo "=== Benchmark — Scraper Setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from https://python.org/downloads/"
    exit 1
fi

echo "✅ Python found: $(python --version 2>&1)"

# Install Crawl4AI (use 'python' not 'python3' — on Windows, python3 may be the Store stub)
echo ""
echo "📦 Installing Crawl4AI..."
python -m pip install crawl4ai

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers (required for JS rendering)..."
python -m crawl4ai.cli setup || python -m playwright install chromium

# Verify
echo ""
echo "🔍 Verifying installation..."
python -c "
import crawl4ai
print('Crawl4AI installed OK')
"

echo ""
echo "=== Setup complete ==="
echo "Crawl4AI is now available for the benchmark skill."
echo "The skill will automatically detect and use it for JS-heavy pricing pages."
