drop table genero;
drop table estado_pago;
drop table marca;
drop table medio_pago;
drop table region;
drop table rol;
drop table tipo_producto;
drop table producto;
drop table usuarios;
drop table pedido;
drop sequence seq_producto_id;
CREATE TABLE GENERO (
    id_genero INTEGER PRIMARY KEY,
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

CREATE TABLE PRODUCTO (
    id_producto INTEGER PRIMARY KEY,
    nombre_producto VARCHAR2(50),
    precio_producto INTEGER,
    stock_producto INTEGER,
    imagenes varchar(250), 
    id_marca INTEGER,
    id_tipo_producto INTEGER,
    FOREIGN KEY (id_marca) REFERENCES MARCA(id_marca),
    FOREIGN KEY (id_tipo_producto) REFERENCES TIPO_PRODUCTO(id_tipo_producto)
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

CREATE TABLE PAGO (
    id_pago INTEGER PRIMARY KEY,
    fecha_pago DATE,
    monto_pagar INTEGER,
    id_medio_pago INTEGER,
    id_estado_pago INTEGER,
    id_pedido INTEGER,
    FOREIGN KEY (id_medio_pago) REFERENCES MEDIO_PAGO(id_medio_pago),
    FOREIGN KEY (id_estado_pago) REFERENCES ESTADO_PAGO(id_estado_pago),
    FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)
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
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto),
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

CREATE TABLE PEDIDO (
    id_pedido INTEGER PRIMARY KEY,
    fecha_pedido DATE,
    cantidad_pedido INTEGER,
    subtotal_pedido INTEGER,
    rut_user VARCHAR2(10),
    FOREIGN KEY (rut_user) REFERENCES USUARIOS(rut_user)
);

insert into genero values(1, 'Masculino');
insert into genero values(2, 'Femenino');
insert into genero values(3, 'Otro');
insert into genero values(4, 'Prefiere no decirlo');

insert into rol values(1, 'Cliente');
insert into rol values(2, 'Vendedor');
insert into rol values(3, 'bodeguero');
insert into rol values(4, 'Contador');
insert into rol values(5, 'Admin');

insert into usuarios values('153654321', 'Pedro', 'Alamos', 'Contreras', 'pedro@gmail.com', '12345678', 1, 5);

insert into marca values(1, 'Dewalt');
insert into marca values(2, 'Bauker');
insert into marca values(3, 'Knipex');
insert into marca values(4, 'Stanley');
insert into marca values(5, 'Makita');
insert into marca values(6, 'Telwin');

insert into tipo_producto values(1, 'Herramienta Electrica');
insert into tipo_producto values(2, 'Herramienta Manuales');
insert into tipo_producto values(3, 'Herramienta Medicion');
insert into tipo_producto values(4, 'Herramienta Corte');
insert into tipo_producto values(5, 'Materiales de construccion');

create sequence seq_producto_id
start with 1 
increment by 1;
commit;










