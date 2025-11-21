USE registro_auxiliar;
-- =========================
-- Perfil Administrador
-- =========================
INSERT INTO Usuarios (usuario, clave, rol, codigo_docente)
VALUES ('SistemAdmin', '@Sis4dmin.', 'admin', NULL);
------------------------------------------------------
-- 1. INSERTAR DOCENTE
------------------------------------------------------
INSERT INTO Docente (Nombre_docente)
VALUES ('Roxana Salazar'); 
------------------------------------------------------
-- 2. INSERTAR ESTUDIANTES
------------------------------------------------------
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

------------------------------------------------------
-- 3. INSERTAR COMPETENCIAS
------------------------------------------------------
INSERT INTO Competencias (Competencia) VALUES
('Se comunica oralmente en su lengua materna'),
('Se expresa correctamente en su lengua materna'),
('Escribe diversos tipos de textos en su lengua materna');

------------------------------------------------------
-- 4. INSERTAR INDICADORES
------------------------------------------------------
INSERT INTO Indicadores (Indicadores_competencias) VALUES
('Exposición de pronombres'),
('Participación en clase'),
('Revisión de cuaderno'),
('Participación en clase'),
('Examen final'),
('Participación en clase');

------------------------------------------------------
-- 5. INSERTAR REGISTRO AUXILIAR
------------------------------------------------------
INSERT INTO REGISTRO_AUXILIAR 
(Nivel, Nombre_colegio, Año, Bimestre, Grado, Seccion, Curso)
VALUES
('Secundaria', 'Juan Velasco Alvarado', 2025, 'Bimestre III', '3', 'B', 'Comunicación');
