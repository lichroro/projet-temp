"""Crée temperatures.db à partir de schema.sql (à lancer une seule fois)."""
import sqlite3

with sqlite3.connect("temperatures.db") as conn:
    conn.executescript(open("schema.sql", encoding="utf-8").read())
print("Base temperatures.db initialisée.")
