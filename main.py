#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI for Managing Front-matter in Markdown Files.
"""

import frontmatter
import argparse
import logging
import os
import pathlib
import shutil
import sys
import tempfile

def main(obsidian_vault_root, required_tags=None, dry_run=False):
    """
    CLI for Managing Front-matter in Markdown Files.

    """
    if dry_run:
        tmp_vault_root = os.path.join(tempfile.gettempdir(),
                'obsidian_tmp_vault_root')
        if os.path.exists(tmp_vault_root):
            logger.debug(f"dry-run: Cleaning up tmp vault copy dir at {tmp_vault_root}...")
            shutil.rmtree(tmp_vault_root)
        logger.debug(f"dry-run: Copying {obsidian_vault_root} to {tmp_vault_root}...")
        tmp_vault_root = shutil.copytree(obsidian_vault_root, tmp_vault_root,
                ignore=lambda d, ls: [f for f in ls if os.path.isdir(f) and f.startswith('.') or os.path.splitext(f)[1] != '.md'])
        logger.debug(f"Working with vault copy at {tmp_vault_root}")
    logger.debug(f"obsidian_vault_root: {obsidian_vault_root}")
    logger.debug(f"required_tags: {required_tags}")
    for rootdirpath, dirnames, filenames in os.walk(obsidian_vault_root, topdown=True):
        # prune uninteresting folders by modifying dirnames in place using slice assignment
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        logger.debug(f"walking root dir {rootdirpath}. Pruned dirs: {dirnames}")
        for filename in [f for f in filenames if os.path.splitext(f)[1] == '.md']:
            md = frontmatter.load(os.path.join(rootdirpath, filename))
            if 'tags' in md.keys():
                if all([t in md['tags'] for t in required_tags]):
                    logger.debug(f"\t{filename}: already has required_tags.")
                    continue
            else:
                md['tags'] = []
            if required_tags:
                md['tags'] = sorted(set(md['tags'] + required_tags))
            else:
                md['tags'] = sorted(set(md['tags']))
            # Write modified md object (front-matter + content) to temp file
            root = tmp_vault_root if dry_run else obsidian_vault_root
            # filename_to_write = os.path.join(root, filename)
            filename_to_write = os.path.join(root, rootdirpath, filename)
            with open(filename_to_write, 'wb') as f:
                frontmatter.dump(md, f)
            logger.debug(f"\t{filename}: {md['tags']}")
    logger.debug(f"Done.")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(os.path.splitext(__file__)[0])
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--obsidian-vault-root",
            required=True,
            action='store',
            type=pathlib.Path,
            help="Absolute path to root of Obsidian Vault to Manage")
    argparser.add_argument("--required-tags",
            action='store',
            nargs='+',
            help="List of tags required to be present in each md file.")
    argparser.add_argument("--dry-run",
            action='store_true',
            help="When True, operate on a temp copy of the vault root dir.")
    args = argparser.parse_args()
    main(args.obsidian_vault_root, required_tags=args.required_tags, dry_run=args.dry_run)
