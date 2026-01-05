#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.local/bin"
mkdir -p "$TARGET"

# Create a tiny launcher called playbook
cat > "$TARGET/playbook" <<EOF
#!/usr/bin/env bash
exec "$ROOT_DIR/playbook.py" "\$@"
EOF

chmod +x "$ROOT_DIR/playbook.py"
chmod +x "$TARGET/playbook"

echo "Installed: $TARGET/playbook"
echo "Make sure $TARGET is in your PATH."
echo "Try: playbook ship_blog --vars topic=\"...\" --vars audience=\"...\""
