# Pelican Bike — Claude ACP Edition

A self-contained Python/Pillow art project that renders a whimsical storybook scene: a pelican riding a red bicycle across a sunny path.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate

```bash
python draw_pelican_bike.py
```

The image is written to:

```text
output/pelican_bike_claude.png
```

## Notes

- Uses only Pillow.
- Renders at 2x resolution and downsamples for smoother edges.
- Final canvas: `1280x960`.
