-- Datos iniciales para materiales
INSERT INTO materiales (nombre, unidad) VALUES
('Tornillos', 'unidades'),
('Madera', 'kg'),
('Pintura', 'litros'),
('Metal', 'kg');

-- Datos iniciales para productos
INSERT INTO productos (nombre) VALUES
('Silla'),
('Mesa'),
('Estante');

-- Relación productos-materiales (BOM)
INSERT INTO producto_material VALUES
(1, 1, 50),   -- Silla usa 50 tornillos
(1, 2, 5),     -- Silla usa 5kg de madera
(2, 2, 15),    -- Mesa usa 15kg de madera
(2, 1, 80),    -- Mesa usa 80 tornillos
(3, 2, 10),    -- Estante usa 10kg de madera
(3, 3, 2),     -- Estante usa 2 litros de pintura
(3, 4, 5);     -- Estante usa 5kg de metal

-- Inventario inicial
INSERT INTO inventario VALUES
(1, 1000, 500),   -- Tornillos: 1000 en stock, mínimo 500
(2, 200, 100),     -- Madera: 200kg en stock, mínimo 100kg
(3, 50, 20),       -- Pintura: 50 litros, mínimo 20
(4, 300, 200);     -- Metal: 300kg, mínimo 200kg