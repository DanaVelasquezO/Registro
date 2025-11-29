USE registro_auxiliar;

INSERT INTO Docente (Nombre_docente)
VALUES ('Roxana Salazar');

INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
VALUES ('rox.salazar', 'R0x@n4.2025', 'docente', LAST_INSERT_ID());
INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
VALUES ('SistemAdmin', '@Sis4dmin.', 'admin', NULL);
