DROP TABLE producto_pedido;
DROP TABLE inventario;
DROP TABLE pago;
DROP TABLE sucursal;
DROP TABLE pedido;
DROP TABLE producto;
DROP TABLE usuarios;
DROP TABLE estado_pedido;
DROP TABLE genero;
DROP TABLE estado_pago;
DROP TABLE marca;
DROP TABLE medio_pago;
DROP TABLE region;
DROP TABLE rol;
DROP TABLE tipo_producto;

DROP SEQUENCE seq_producto_id;
DROP SEQUENCE seq_id_pedido;
DROP SEQUENCE seq_producto_pedido;
DROP SEQUENCE seq_id_pago;

CREATE TABLE GENERO (
    id_genero INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE ESTADO_PEDIDO (
    id_estado_pedido INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE ROL (
    id_rol INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE MARCA (
    id_marca INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE TIPO_PRODUCTO (
    id_tipo_producto INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE ESTADO_PAGO (
    id_estado_pago INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE MEDIO_PAGO (
    id_medio_pago INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE REGION (
    id_region INTEGER PRIMARY KEY,
    descripcion VARCHAR2(50)
);

CREATE TABLE USUARIOS (
    rut_user VARCHAR2(10) PRIMARY KEY,
    nombre_user VARCHAR2(50),
    p_apellido VARCHAR2(50),
    s_apellido VARCHAR2(50),
    correo_user VARCHAR2(50),
    contrasena_user VARCHAR2(50),
    id_genero INTEGER,
    id_rol INTEGER,
    FOREIGN KEY (id_genero) REFERENCES GENERO(id_genero),
    FOREIGN KEY (id_rol) REFERENCES ROL(id_rol)
);

CREATE TABLE PRODUCTO (
    id_producto INTEGER PRIMARY KEY,
    nombre_producto VARCHAR2(50),
    precio_producto INTEGER,
    stock_producto INTEGER,
    imagenes VARCHAR(250),
    id_marca INTEGER,
    id_tipo_producto INTEGER,
    FOREIGN KEY (id_marca) REFERENCES MARCA(id_marca),
    FOREIGN KEY (id_tipo_producto) REFERENCES TIPO_PRODUCTO(id_tipo_producto)
);

CREATE TABLE PEDIDO (
    id_pedido INTEGER PRIMARY KEY,
    fecha_pedido DATE,
    cantidad_pedido INTEGER,
    subtotal_pedido INTEGER,
    rut_user VARCHAR2(10),
    id_estado_pedido INTEGER,
    FOREIGN KEY (rut_user) REFERENCES USUARIOS(rut_user),
    FOREIGN KEY (id_estado_pedido) REFERENCES ESTADO_PEDIDO(id_estado_pedido)
);

CREATE TABLE PAGO (
    id_pago INTEGER PRIMARY KEY,
    fecha_pago DATE,
    monto_pagar INTEGER,
    url_comprobante varchar2(100),
    id_medio_pago INTEGER,
    id_estado_pago INTEGER,
    id_pedido INTEGER,
    FOREIGN KEY (id_medio_pago) REFERENCES MEDIO_PAGO(id_medio_pago),
    FOREIGN KEY (id_estado_pago) REFERENCES ESTADO_PAGO(id_estado_pago),
    FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)
);

CREATE TABLE SUCURSAL (
    id_sucursal INTEGER PRIMARY KEY,
    direccion_sucursal VARCHAR2(50),
    id_region INTEGER,
    rut_user VARCHAR2(10),
    id_pago INTEGER,
    FOREIGN KEY (id_region) REFERENCES REGION(id_region),
    FOREIGN KEY (rut_user) REFERENCES USUARIOS(rut_user),
    FOREIGN KEY (id_pago) REFERENCES PAGO(id_pago)
);

CREATE TABLE INVENTARIO (
    id_inventario INTEGER PRIMARY KEY,
    ubicacion VARCHAR2(50),
    fecha_ultima_actualizacion DATE,
    id_producto INTEGER,
    id_sucursal INTEGER,
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto),
    FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal)
);

CREATE TABLE PRODUCTO_PEDIDO (
    id_producto_pedido INTEGER PRIMARY KEY,
    id_producto INTEGER,
    id_pedido INTEGER,
    cantidad_producto INTEGER,
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto),
    FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)
);

CREATE SEQUENCE seq_producto_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_id_pedido START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_producto_pedido START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_id_pago START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- GENERO
INSERT INTO genero VALUES (1, 'Masculino');
INSERT INTO genero VALUES (2, 'Femenino');
INSERT INTO genero VALUES (3, 'Otro');
INSERT INTO genero VALUES (4, 'Prefiere no decirlo');

-- ROL
INSERT INTO rol VALUES (1, 'Cliente');
INSERT INTO rol VALUES (2, 'Vendedor');
INSERT INTO rol VALUES (3, 'Bodeguero');
INSERT INTO rol VALUES (4, 'Contador');
INSERT INTO rol VALUES (5, 'Admin');

-- USUARIO ADMIN
INSERT INTO usuarios VALUES ('230963223', 'admin', 'admin', 'admin', 'admin@gmail.com', '1234', 1, 5);
insert into usuarios values('146957293', 'vendedor', 'vendedor', 'vendedor', 'vendedor@gmail.com', '1234', 2, 2);
insert into usuarios values('98323856', 'cliente', 'cliente', 'cliente', 'cliente@gmail.com', '1234', 1, 1);
insert into usuarios values('192353513', 'bodeguero', 'bodeguero', 'bodeguero', 'bodeguero@gmail.com', '1234', 1, 3);
insert into usuarios values('161713988', 'contador', 'contador', 'contador', 'contador@gmail.com', '1234', 1, 4);

-- MARCA
INSERT INTO marca VALUES (1, 'Dewalt');
INSERT INTO marca VALUES (2, 'Bauker');
INSERT INTO marca VALUES (3, 'Knipex');
INSERT INTO marca VALUES (4, 'Stanley');
INSERT INTO marca VALUES (5, 'Makita');
INSERT INTO marca VALUES (6, 'Telwin');

-- TIPO PRODUCTO
INSERT INTO tipo_producto VALUES (1, 'Herramienta Electrica');
INSERT INTO tipo_producto VALUES (2, 'Herramienta Manuales');
INSERT INTO tipo_producto VALUES (3, 'Herramienta Medicion');
INSERT INTO tipo_producto VALUES (4, 'Herramienta Corte');
INSERT INTO tipo_producto VALUES (5, 'Materiales de construccion');

-- ESTADO PEDIDO
INSERT INTO estado_pedido VALUES (1, 'Por pagar');
INSERT INTO estado_pedido VALUES (2, 'Pagado');
INSERT INTO estado_pedido VALUES (3, 'Aprobado');
INSERT INTO estado_pedido VALUES (4, 'Rechazado');
INSERT INTO estado_pedido VALUES (5, 'Entregado');
INSERT INTO estado_pedido VALUES (6, 'Preparado');
INSERT INTO estado_pedido VALUES (7, 'En preparacion');

-- MEDIO PAGO
INSERT INTO medio_pago VALUES (1, 'Paypal');
INSERT INTO medio_pago VALUES (2, 'Transferencia');

-- ESTADO PAGO
INSERT INTO estado_pago VALUES (1, 'Por aprobar');
INSERT INTO estado_pago VALUES (2, 'Aprobado');

-- PRODUCTO
INSERT INTO producto VALUES (1, 'Martillo', 15990, 100, 'imagenes_productos/martillo.png', 1, 1);
INSERT INTO producto VALUES (2, 'Taladro Inalambrico', 13990, 100, 'imagenes_productos/taladro_bosh.png', 2, 2);
insert into producto values(3,'Cierra electrica', 42000, 3, 'imagenes_productos/cierra_electrica.png', 2, 1);
insert into producto values(4,'Esmeril', 25000, 20, 'imagenes_productos/esmeril.png', 5, 1);
insert into producto values(5,'Lijadora', 49000, 15, 'imagenes_productos/lijadora.png', 1, 1);
insert into producto values(6,'Dremel', 39000, 10, 'imagenes_productos/dremel.png', 6, 1);
insert into producto values(7,'Saco cemento', 35000, 80, 'imagenes_productos/saco_cemento.png', 3, 5);
insert into producto values(8,'Cepillo electrico', 244000, 5, 'imagenes_productos/cepillo_electrico.png', 2, 1);
insert into producto values(9,'Cinta metrica', 14500, 30, 'imagenes_productos/cinta_metrica.png', 1, 2);
insert into producto values(10,'Caladora', 4990, 15, 'imagenes_productos/caladora.png', 2, 1);
insert into producto values(11,'Serrucho', 15500, 25, 'imagenes_productos/serrucho.png', 4, 4);
insert into producto values(12,'Set desatornillador', 35500, 20, 'imagenes_productos/desatornilladores.png', 5, 2);
insert into producto values(13,'Cierra circular', 57000, 17, 'imagenes_productos/cierra_circular.png', 6, 4);
insert into producto values(14,'Motosierra', 363000, 5, 'imagenes_productos/motosierra.png', 2, 4);
insert into producto values(15,'Alicate', 5500, 55, 'imagenes_productos/alicate.png', 1, 2);

COMMIT;