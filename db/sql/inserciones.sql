USE registro_auxiliar;

INSERT INTO Docente (Nombre_docente)
VALUES ('Roxana Salazar');

INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
VALUES ('rox.salazar', 'R0x@n4.2025', 'docente', LAST_INSERT_ID());
INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
VALUES ('SistemAdmin', '@Sis4dmin.', 'admin', NULL);


INSERT INTO Estudiante (Nombre_estudiante) VALUES
('Martín Alonso Chero'),
('Sofía Valentina Quispe'),
('Alejandro Rafael Dávila'),
('Valeria Nicole López'),
('Sebastián Juan Cruz'),
('Camila Andrea Rojas'),
('Diego Armando Torres'),
('Luciana Gabriela Ramos'),
('Adrián Mateo Vargas'),
('María Fernanda Huamán'),
('Gabriel Enrique Ríos'),
('Daniela Belén Soto'),
('Benjamín Andrés Castro'),
('Isabella Victoria Pinedo'),
('Joaquín Marcelo Peña'),
('Florencia Isabel Luyo'),
('Nicolás Jesús Paz'),
('Renata Lizbeth Mendoza'),
('Santiago David Huanca'),
('Mariana Sofía Flores'),
('Alonso Raúl Vidal'),
('Emilia Jimena Paredes'),
('Felipe Arturo Cárdenas'),
('Natalia Camila Ochoa'),
('Guillermo José Sotomayor'),
('Antonella Fabiana Chávez'),
('Ricardo Daniel Milla'),
('Catalina Estefanía Herrera'),
('Julio César Arana'),
('Alexandra Lucía Quispe');

INSERT INTO Competencias (Competencia) VALUES
('Se comunica oralmente en su lengua materna'),
('Se expresa correctamente en su lengua materna'),
('Escribe diversos tipos de textos en su lengua materna');

INSERT INTO Indicadores (Indicadores_competencias, Id_competencia) VALUES
('Exposición de pronombres', 1),
('Participación en clase', 1),
('Revisión de cuaderno', 2),
('Participación en clase', 2),
('Examen final', 3),
('Participación en clase', 3);

INSERT INTO REGISTRO_AUXILIAR
(Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso)
VALUES
('Secundaria', 'Juan Velasco Alvarado', 2025, 'Bimestre III', '3', 'B', 'Comunicación');
