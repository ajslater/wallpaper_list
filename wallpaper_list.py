#!/usr/bin/env python3
"""Display paths to the current desktop wallpapers."""
# https://discussions.apple.com/message/23522465#23522465

import os
import sqlite3
import subprocess

HOME = os.getenv("HOME")
DBPATH = "{}/Library/Application Support/Dock/desktoppicture.db".format(HOME)
WP_ROOT_SQL = "SELECT data.value FROM data ORDER BY rowid LIMIT 1 OFFSET 0"
# NUM_DESKTOPS_SQL = "(SELECT data.value FROM data" \
#    " ORDER BY rowid LIMIT 1 OFFSET 2)"
NUM_DESKTOPS_SQL = 3
IMAGES_SQL_TMPL = "SELECT data.value FROM data ORDER BY rowid " \
    f"DESC LIMIT {NUM_DESKTOPS_SQL}"


def get_wp_root(cur):
    """Get the wallpaper root directory."""
    path = cur.execute(WP_ROOT_SQL).fetchone()[0]
    if os.path.islink(path):
        path = os.readlink(path)
    return path.replace("~", HOME)


def get_images(cur):
    """Get the images from the database."""
    return cur.execute(IMAGES_SQL_TMPL).fetchall()


def query_db():
    """Get the information from the database."""
    with sqlite3.connect(DBPATH) as conn:
        cur = conn.cursor()
        wp_root = get_wp_root(cur)
        images = get_images(cur)
        cur.close()
    return wp_root, images


def get_paths(wp_root, imgs):
    """Create full paths for the images and dereference symlinks."""
    paths = []
    for img in imgs:
        img = os.path.join(wp_root, img[0])
        if os.path.islink(img):
            img = os.readlink(img)
        paths += [img]

    return paths


def main():
    """Get the images from the DB, print the paths and open them."""
    wp_root, imgs = query_db()
    paths = get_paths(wp_root, imgs)
    print(" ".join(paths))
    subprocess.call(["/usr/bin/open"] + paths)


if __name__ == "__main__":
    main()
