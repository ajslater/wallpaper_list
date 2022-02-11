#!/usr/bin/env python3
"""Display paths to the current desktop wallpapers."""
# https://discussions.apple.com/message/23522465#23522465

import sqlite3
import subprocess
from pathlib import Path

DBPATH = Path.home() / "Library/Application Support/Dock/desktoppicture.db"
WP_ROOT_SQL = "SELECT data.value FROM data ORDER BY rowid LIMIT 1 OFFSET 0"
NUM_DESKTOPS_SQL = 3
IMAGES_SQL_TMPL = (
    "SELECT data.value FROM data ORDER BY rowid DESC LIMIT {NUM_DESKTOPS_SQL}"
)


def query_db():
    """Get the information from the database."""
    images_sql = IMAGES_SQL_TMPL.format(NUM_DESKTOPS_SQL=NUM_DESKTOPS_SQL)
    with sqlite3.connect(DBPATH) as conn:
        cur = conn.cursor()
        wp_root = cur.execute(WP_ROOT_SQL).fetchone()[0]
        images = cur.execute(images_sql).fetchall()
    wp_root = Path(wp_root).expanduser().resolve()
    return wp_root, images


def get_paths():
    """Create full paths for the images and dereference symlinks."""
    wp_root, imgs = query_db()
    paths = []
    for img in imgs:
        img_path = Path(img[0])
        img_path = img_path.expanduser()
        if not img_path.is_absolute():
            img_path = wp_root / img_path
        img_path = img_path.resolve()
        print(img_path)
        paths += [img_path]

    return paths


def main():
    """Get the images from the DB, print the paths and open them."""
    paths = get_paths()
    subprocess.call(["/usr/bin/open"] + paths)


if __name__ == "__main__":
    main()
