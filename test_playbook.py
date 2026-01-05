#!/usr/bin/env python3
"""
Test suite for Claude Playbooks

Run with: python3 test_playbook.py
"""

import unittest
import tempfile
import os
import json
import sys
from pathlib import Path

# Import playbook module
sys.path.insert(0, str(Path(__file__).parent))
import playbook

class TestVariableSubstitution(unittest.TestCase):
    """Test template variable substitution."""

    def test_basic_substitution(self):
        """Basic {{var}} substitution works."""
        template = "Hello {{name}}"
        result = playbook.render(template, {"name": "World"})
        self.assertEqual(result, "Hello World")

    def test_multiple_variables(self):
        """Multiple variables substitute correctly."""
        template = "{{greeting}} {{name}}!"
        result = playbook.render(template, {"greeting": "Hi", "name": "Alice"})
        self.assertEqual(result, "Hi Alice!")

    def test_unknown_variable_unchanged(self):
        """Unknown variables remain as {{var}}."""
        template = "Hello {{name}}, your {{title}} is {{unknown}}"
        result = playbook.render(template, {"name": "Bob", "title": "role"})
        self.assertEqual(result, "Hello Bob, your role is {{unknown}}")

    def test_alphanumeric_underscore_variables(self):
        """Variables support alphanumeric and underscore."""
        template = "{{var_1}} {{var2}} {{VarName}}"
        result = playbook.render(template, {
            "var_1": "A",
            "var2": "B",
            "VarName": "C"
        })
        self.assertEqual(result, "A B C")

    def test_empty_dict(self):
        """Empty vars_dict leaves all variables unchanged."""
        template = "{{a}} {{b}} {{c}}"
        result = playbook.render(template, {})
        self.assertEqual(result, "{{a}} {{b}} {{c}}")

class TestParseVars(unittest.TestCase):
    """Test variable parsing from command line."""

    def test_basic_parse(self):
        """Basic key=value parsing."""
        result = playbook.parse_vars(["key=value"])
        self.assertEqual(result, {"key": "value"})

    def test_multiple_vars(self):
        """Multiple variables parse correctly."""
        result = playbook.parse_vars(["a=1", "b=2", "c=3"])
        self.assertEqual(result, {"a": "1", "b": "2", "c": "3"})

    def test_value_with_equals(self):
        """Values containing = parse correctly."""
        result = playbook.parse_vars(["url=http://example.com?a=b"])
        self.assertEqual(result, {"url": "http://example.com?a=b"})

    def test_whitespace_trimmed(self):
        """Whitespace is trimmed from keys and values."""
        result = playbook.parse_vars(["  key  =  value  "])
        self.assertEqual(result, {"key": "value"})

    def test_invalid_format(self):
        """Invalid format raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            playbook.parse_vars(["invalid"])
        self.assertIn("Use key=value", str(ctx.exception))

    def test_empty_key(self):
        """Empty key raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            playbook.parse_vars(["=value"])
        self.assertIn("Key is empty", str(ctx.exception))

    def test_empty_list(self):
        """Empty list returns empty dict."""
        result = playbook.parse_vars([])
        self.assertEqual(result, {})

class TestPackManagement(unittest.TestCase):
    """Test pack loading and validation."""

    def setUp(self):
        """Create temporary pack structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.orig_packs_dir = playbook.PACKS_DIR
        playbook.PACKS_DIR = Path(self.temp_dir)

        # Create sample pack
        pack_dir = playbook.PACKS_DIR / "test-pack"
        pack_dir.mkdir()
        (pack_dir / "meta").mkdir()
        (pack_dir / "playbooks").mkdir()

        # Create manifest
        self.manifest = {
            "name": "test-pack",
            "version": "1.0.0",
            "playbooks": ["test_playbook"]
        }
        (pack_dir / "meta" / "manifest.json").write_text(json.dumps(self.manifest))

        # Create playbook
        (pack_dir / "playbooks" / "test_playbook.md").write_text("Test {{var}}")

    def tearDown(self):
        """Clean up temporary files."""
        playbook.PACKS_DIR = self.orig_packs_dir
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_manifest(self):
        """Manifest loads and parses correctly."""
        manifest = playbook.load_manifest("test-pack")
        self.assertEqual(manifest["name"], "test-pack")
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(manifest["playbooks"], ["test_playbook"])

    def test_load_manifest_not_found(self):
        """Loading nonexistent pack raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            playbook.load_manifest("nonexistent-pack")

    def test_validate_manifest_valid(self):
        """Valid manifest passes validation."""
        # Should not raise
        playbook.validate_manifest(self.manifest, "test-pack")

    def test_validate_manifest_missing_field(self):
        """Missing required field raises ValueError."""
        invalid_manifest = {"name": "test"}
        with self.assertRaises(ValueError) as ctx:
            playbook.validate_manifest(invalid_manifest, "test-pack")
        self.assertIn("missing required field", str(ctx.exception))

    def test_validate_manifest_invalid_playbooks_type(self):
        """Non-array playbooks field raises ValueError."""
        invalid_manifest = {
            "name": "test",
            "version": "1.0.0",
            "playbooks": "not-an-array"
        }
        with self.assertRaises(ValueError) as ctx:
            playbook.validate_manifest(invalid_manifest, "test-pack")
        self.assertIn("must be an array", str(ctx.exception))

    def test_check_license_not_required(self):
        """License check passes when not required."""
        manifest = {"requires_license": False}
        # Should not raise or exit
        playbook.check_license(manifest, "test-pack")

    def test_check_license_required_missing(self):
        """License check exits when required but missing."""
        manifest = {
            "requires_license": True,
            "license_env": "TEST_LICENSE_KEY"
        }
        # Remove env var if exists
        os.environ.pop("TEST_LICENSE_KEY", None)

        with self.assertRaises(SystemExit):
            playbook.check_license(manifest, "test-pack")

    def test_check_license_required_present(self):
        """License check passes when required and present."""
        manifest = {
            "requires_license": True,
            "license_env": "TEST_LICENSE_KEY"
        }
        os.environ["TEST_LICENSE_KEY"] = "test-key"

        try:
            # Should not raise or exit
            playbook.check_license(manifest, "test-pack")
        finally:
            os.environ.pop("TEST_LICENSE_KEY", None)

    def test_discover_packs(self):
        """Pack discovery finds available packs."""
        packs = playbook.discover_packs()
        self.assertIn("test-pack", packs)

class TestPlaybookLoading(unittest.TestCase):
    """Test playbook loading from core and packs."""

    def setUp(self):
        """Set up test environment."""
        self.orig_playbooks_dir = playbook.PLAYBOOKS_DIR
        self.orig_packs_dir = playbook.PACKS_DIR

    def tearDown(self):
        """Restore original paths."""
        playbook.PLAYBOOKS_DIR = self.orig_playbooks_dir
        playbook.PACKS_DIR = self.orig_packs_dir

    def test_load_core_playbook(self):
        """Loading core playbook works."""
        # Use actual playbooks directory
        content = playbook.load_playbook("audit_contract")
        self.assertIn("SYSTEM", content)
        self.assertIn("smart contract auditor", content)

    def test_load_nonexistent_playbook(self):
        """Loading nonexistent playbook raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            playbook.load_playbook("nonexistent_playbook_xyz")

def run_tests():
    """Run all tests."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())
