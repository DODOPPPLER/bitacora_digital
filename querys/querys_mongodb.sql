create database bitacora_digital

create table rol(
	id_rol int generated always as identity primary key,
	nombre varchar(100) not null unique,
	descripcion text
)

create table usuario(
	id_usuario int generated always as identity primary key,
	nombre_usuario varchar(100) not null unique,
	email varchar(100) not null unique,
	contraseña varchar(128) Check (char_length(contraseña)>= 8),
	id_rol int not null unique,
	constraint fk_usuario_rol FOREIGN KEY (id_rol)
		references rol(id_rol)
		on update cascade
		on delete restrict
)

create table perfil(
	id_perfil int generated always as identity primary key,
	id_usuario int not null unique,
	nombre varchar(50) not null,
	apellido  varchar(50),
	bio text,
	foto_perfil varchar(255),
	constraint fk_perfil_usuario foreign key (id_usuario)
		references usuario(id_usuario)
		on update cascade
		on delete cascade
)

create table post(
	id_post int generated always as identity primary key,
	id_usuario int not null,
	titulo varchar (150) not null,
	contenido text not null,
	fecha_creacion timestamp not null default current_timestamp,
	fecha_actualizacion timestamp,
	constraint fk_perfil_usuario foreign key (id_usuario)
		references usuario(id_usuario)
		on update cascade
		on delete cascade
)


INSERT INTO rol (nombre, descripcion) VALUES
	('admin', 'Administrador con todos los permisos'),
	('usuario', 'Usuario estándar con permisos básicos'),
	('visitante', 'Solo puede ver los posts');

select * from rol
