#!/usr/bin/env python
"""Display paths to the current desktop wallpapers."""
# https://discussions.apple.com/message/23522465#23522465
from __future__ import absolute_import, division, print_function

import os
import sqlite3
import subprocess

HOME = os.getenv("HOME")
DBPATH = "{}/Library/Application Support/Dock/desktoppicture.db".format(HOME)
WP_ROOT_SQL = "SELECT data.value FROM data ORDER BY rowid LIMIT 1 OFFSET 0"
NUM_DESKTOPS_SQL = "(SELECT data.value FROM data" \
                   " ORDER BY rowid LIMIT 1 OFFSET 2)"
IMAGES_SQL_TMPL = "SELECT data.value FROM data ORDER BY rowid " \
                  "DESC LIMIT {}".format(NUM_DESKTOPS_SQL)


def get_wp_root(cur):
    """get the wallpaper root directory."""
    path = cur.execute(WP_ROOT_SQL).fetchone()[0]
    if os.path.islink(path):
        path = os.readlink(path)
    return path.replace("~", HOME)


def get_images(cur):
    """get the number of images from the database equal to the number of
       desktops"""
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
    """create full paths for the images and dereference symlinks."""
    paths = []
    for img in imgs:
        img = os.path.join(wp_root, img[0])
        if os.path.islink(img):
            img = os.readlink(img)
        paths += [img]

    return paths


def main():
    """main"""
    wp_root, imgs = query_db()
    paths = get_paths(wp_root, imgs)
    print(' '.join(paths))
    subprocess.call(["/usr/bin/open"] + paths)


if __name__ == "__main__":
    main()
