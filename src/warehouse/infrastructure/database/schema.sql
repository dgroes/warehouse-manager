/* Clase categoría */
CREATE TABLE IF NOT EXISTS  category(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE
);

/* Clase producto */
CREATE TABLE IF NOT EXISTS  product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    barcode TEXT NOT NULL UNIQUE,
    active INTEGER NOT NULL DEFAULT 1, -- Por defecto será 1, SQLite no tiene el tipo BOOLEAN
    FOREIGN KEY (category_id) REFERENCES category(id)
);