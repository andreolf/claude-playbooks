# Example Pack

This is a sample pack demonstrating the playbook pack structure.

## Structure

```
examples/
├── meta/
│   └── manifest.json      # Pack metadata and configuration
├── playbooks/
│   └── hello_world.md     # Example playbook template
└── README.md              # This file
```

## Manifest

The `manifest.json` file defines the pack:

```json
{
  "name": "examples",
  "version": "1.0.0",
  "description": "Example pack demonstrating pack structure",
  "playbooks": ["hello_world"],
  "requires_license": false
}
```

### Required Fields
- `name` - Pack name (should match directory name)
- `version` - Semantic version (MAJOR.MINOR.PATCH)
- `playbooks` - Array of playbook names (without .md extension)

### Optional Fields
- `description` - Pack description
- `author` - Pack author/maintainer
- `requires_license` - Whether pack requires license key (default: false)
- `license_env` - Environment variable name for license (default: PLAYBOOK_LICENSE_KEY)
- `license_url` - URL where users can obtain license

## Usage

List playbooks in this pack:
```bash
playbook list --pack examples
```

Run a playbook from this pack:
```bash
playbook run hello_world --pack examples \
  --vars name="Alice" \
  --vars language="Spanish"
```

## Creating Your Own Pack

Use `playbook init` to scaffold a new pack:

```bash
playbook init my-pack --with-pack my-pack
```

This creates:
- `packs/my-pack/meta/manifest.json`
- `packs/my-pack/playbooks/example.md`

Then:
1. Edit the manifest with your pack details
2. Add your playbook templates to `playbooks/`
3. Update the `playbooks` array in manifest.json
4. Test with `playbook run <playbook> --pack my-pack`

## License Requirements

To require a license for your pack:

```json
{
  "requires_license": true,
  "license_env": "MY_PACK_LICENSE",
  "license_url": "https://example.com/license"
}
```

Users must then set the environment variable:
```bash
export MY_PACK_LICENSE="license-key-here"
playbook run my_playbook --pack my-pack
```

## Distribution

Distribute your pack by:
1. Sharing the pack directory
2. Users copy it to their `packs/` directory
3. Playbooks become available via `--pack` flag

For monetization, use `requires_license` and distribute license keys separately.
