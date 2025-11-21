CREATE DATABASE registro_auxiliar;
USE registro_auxiliar;

CREATE TABLE REGISTRO_AUXILIAR (
  Numero_de_registro INT AUTO_INCREMENT PRIMARY KEY,
  Nivel VARCHAR(15) NOT NULL, 
  Nombre_colegio VARCHAR(100) NOT NULL, 
  Año INT NOT NULL,
  Bimestre VARCHAR(15) NOT NULL, 
  Grado VARCHAR(10) NOT NULL, 
  Seccion VARCHAR(1) NOT NULL, 
  Curso VARCHAR(20) NOT NULL, 
  Promedio_curso DECIMAL(4, 2),
  Conclusiones_descriptivas TEXT
);

CREATE TABLE Docente (
  Codigo_docente INT AUTO_INCREMENT PRIMARY KEY,
  Nombre_docente VARCHAR(40) NOT NULL
);

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    clave VARCHAR(200) NOT NULL,
    rol ENUM('admin', 'docente') NOT NULL DEFAULT 'docente',
    codigo_docente INT NULL,
    FOREIGN KEY (codigo_docente) REFERENCES Docente(Codigo_docente)
);

CREATE TABLE Estudiante (
  Codigo_estudiante INT AUTO_INCREMENT PRIMARY KEY,
  Nombre_estudiante VARCHAR(40) NOT NULL
);

CREATE TABLE Competencias (
  Id_competencia INT AUTO_INCREMENT PRIMARY KEY,
  Competencia VARCHAR(150) NOT NULL
);

CREATE TABLE Indicadores (
  Id_indicador INT AUTO_INCREMENT PRIMARY KEY,
  Indicadores_competencias TEXT NOT NULL
);

CREATE TABLE Docente_Registro (
  Codigo_docente INT NOT NULL,
  Numero_de_registro INT NOT NULL,
  PRIMARY KEY (Codigo_docente, Numero_de_registro),
  FOREIGN KEY (Codigo_docente) REFERENCES Docente(Codigo_docente),
  FOREIGN KEY (Numero_de_registro) REFERENCES REGISTRO_AUXILIAR(Numero_de_registro)
);

CREATE TABLE Estudiante_Registro (
  Codigo_estudiante INT NOT NULL,
  Numero_de_registro INT NOT NULL,
  PRIMARY KEY (Codigo_estudiante, Numero_de_registro),
  FOREIGN KEY (Codigo_estudiante) REFERENCES Estudiante(Codigo_estudiante),
  FOREIGN KEY (Numero_de_registro) REFERENCES REGISTRO_AUXILIAR(Numero_de_registro)
);

CREATE TABLE Competencias_Registro (
  Id_competencia INT NOT NULL,
  Numero_de_registro INT NOT NULL,
  PRIMARY KEY (Id_competencia, Numero_de_registro),
  FOREIGN KEY (Id_competencia) REFERENCES Competencias(Id_competencia),
  FOREIGN KEY (Numero_de_registro) REFERENCES REGISTRO_AUXILIAR(Numero_de_registro)
);

CREATE TABLE Indicadores_Registro (
  Id_indicador INT NOT NULL,
  Numero_de_registro INT NOT NULL,
  PRIMARY KEY (Id_indicador, Numero_de_registro),
  FOREIGN KEY (Id_indicador) REFERENCES Indicadores(Id_indicador),
  FOREIGN KEY (Numero_de_registro) REFERENCES REGISTRO_AUXILIAR(Numero_de_registro)
);

CREATE TABLE Notas_Registro (
    Id_registro_nota INT AUTO_INCREMENT PRIMARY KEY,
    Numero_de_registro INT NOT NULL,
    Codigo_estudiante INT NOT NULL,
    Id_competencia INT NOT NULL,
    Id_indicador INT NOT NULL,
    Nota DECIMAL(4,2) NOT NULL,

    FOREIGN KEY (Numero_de_registro) REFERENCES REGISTRO_AUXILIAR(Numero_de_registro),
    FOREIGN KEY (Codigo_estudiante) REFERENCES Estudiante(Codigo_estudiante),
    FOREIGN KEY (Id_competencia) REFERENCES Competencias(Id_competencia),
    FOREIGN KEY (Id_indicador) REFERENCES Indicadores(Id_indicador)
);

ALTER TABLE REGISTRO_AUXILIAR AUTO_INCREMENT = 1001;
ALTER TABLE Docente AUTO_INCREMENT = 101;
ALTER TABLE Estudiante AUTO_INCREMENT = 2025001;
ALTER TABLE Competencias AUTO_INCREMENT = 1;
ALTER TABLE Indicadores AUTO_INCREMENT = 301;

