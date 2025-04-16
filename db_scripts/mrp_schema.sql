CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE materiales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL
);

CREATE TABLE producto_material (
    producto_id INT REFERENCES productos(id),
    material_id INT REFERENCES materiales(id),
    cantidad DECIMAL NOT NULL,
    PRIMARY KEY (producto_id, material_id)
);

CREATE TABLE inventario (
    material_id INT PRIMARY KEY REFERENCES materiales(id),
    stock DECIMAL NOT NULL,
    stock_minimo DECIMAL NOT NULL
);