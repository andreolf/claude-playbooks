#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing Claude Playbooks...${NC}"
echo ""

# Detect script location
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.local/bin"

# Create target directory
mkdir -p "$TARGET"

# Create launcher
cat > "$TARGET/playbook" <<EOF
#!/usr/bin/env bash
exec "$ROOT_DIR/playbook.py" "\$@"
EOF

# Make executable
chmod +x "$ROOT_DIR/playbook.py"
chmod +x "$TARGET/playbook"

echo -e "${GREEN}✓${NC} Installed playbook to: $TARGET/playbook"

# Check if directory is in PATH
if [[ ":$PATH:" == *":$TARGET:"* ]]; then
    echo -e "${GREEN}✓${NC} $TARGET is in your PATH"
    echo ""
    echo -e "${GREEN}Installation complete!${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠${NC}  $TARGET is not in your PATH"
    echo ""

    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        bash)
            RCFILE="$HOME/.bashrc"
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS uses .bash_profile for login shells
                RCFILE="$HOME/.bash_profile"
            fi
            echo "Add this line to $RCFILE:"
            echo ""
            echo -e "  ${BLUE}export PATH=\"\$PATH:$TARGET\"${NC}"
            echo ""
            echo "Then run:"
            echo -e "  ${BLUE}source $RCFILE${NC}"
            ;;
        zsh)
            RCFILE="$HOME/.zshrc"
            echo "Add this line to $RCFILE:"
            echo ""
            echo -e "  ${BLUE}export PATH=\"\$PATH:$TARGET\"${NC}"
            echo ""
            echo "Then run:"
            echo -e "  ${BLUE}source $RCFILE${NC}"
            ;;
        fish)
            echo "Run this command:"
            echo ""
            echo -e "  ${BLUE}fish_add_path $TARGET${NC}"
            ;;
        *)
            echo "Add $TARGET to your PATH in your shell configuration file."
            ;;
    esac

    echo ""
    echo "Or restart your terminal."
fi

echo ""
echo -e "${GREEN}Test your installation:${NC}"
echo -e "  ${BLUE}playbook list${NC}"
echo ""
echo -e "${GREEN}Get started:${NC}"
echo -e "  ${BLUE}playbook run audit_contract --vars project=\"MyProject\" --vars chain=\"Ethereum\" --input contract.sol${NC}"
echo ""
echo -e "${GREEN}For help:${NC}"
echo -e "  ${BLUE}playbook --help${NC}"
echo -e "  ${BLUE}playbook run --help${NC}"
echo ""
