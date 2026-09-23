#!/usr/bin/env python3
"""Fallback script to apply parameterized query fixes to routes/login.ts and routes/search.ts."""

import os
import sys


def fix_login():
    path = "routes/login.ts"
    if not os.path.exists(path):
        print(f"File {path} not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    vuln = "models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: UserModel, plain: true })"
    fix = "models.sequelize.query('SELECT * FROM Users WHERE email = :email AND password = :password AND deletedAt IS NULL', { replacements: { email: req.body.email || '', password: security.hash(req.body.password || '') }, model: UserModel, plain: true })"

    if vuln in content:
        content = content.replace(vuln, fix)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully applied parameterized query fix to {path}")
    else:
        print(f"Vulnerable string not found in {path} (already fixed or modified)")


def fix_search():
    path = "routes/search.ts"
    if not os.path.exists(path):
        print(f"File {path} not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    vuln = "models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)"
    fix = "models.sequelize.query('SELECT * FROM Products WHERE ((name LIKE :criteria OR description LIKE :criteria) AND deletedAt IS NULL) ORDER BY name', { replacements: { criteria: `%${criteria}%` } })"

    if vuln in content:
        content = content.replace(vuln, fix)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully applied parameterized query fix to {path}")
    else:
        print(f"Vulnerable string not found in {path} (already fixed or modified)")


def main():
    print("Applying fallback parameterized query fixes...")
    fix_login()
    fix_search()
    return 0


if __name__ == "__main__":
    sys.exit(main())
