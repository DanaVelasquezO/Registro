USE registro_auxiliar;

DELIMITER //
CREATE FUNCTION clasificacion_literal(p_promedio DECIMAL(4,2))
RETURNS CHAR(2)
DETERMINISTIC
BEGIN
    DECLARE v_literal CHAR(2);

    IF p_promedio >= 18.00 THEN
        SET v_literal := 'AD';
    ELSEIF p_promedio >= 14.00 THEN
        SET v_literal := 'A';
    ELSEIF p_promedio >= 11.00 THEN
        SET v_literal := 'B';
    ELSE
        SET v_literal := 'C';
    END IF;

    RETURN v_literal;
END //
DELIMITER ;
-- calcular promdio del curso
DELIMITER //
CREATE TRIGGER recalcular_promedio_curso
AFTER INSERT ON Notas_Registro
FOR EACH ROW
BEGIN
    DECLARE nuevo_prom DECIMAL(4,2);

    SELECT AVG(Nota) INTO nuevo_prom
    FROM Notas_Registro
    WHERE Numero_de_registro = NEW.Numero_de_registro;

    UPDATE REGISTRO_AUXILIAR
    SET Promedio_curso = nuevo_prom
    WHERE Numero_de_registro = NEW.Numero_de_registro;
END //
DELIMITER ;


-- Validar Rango de Nota

DELIMITER //
CREATE TRIGGER validar_rango_nota
BEFORE INSERT ON Notas_Registro
FOR EACH ROW
BEGIN
    IF NEW.Nota < 0 OR NEW.Nota > 20 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La nota debe estar entre 0 y 20.';
    END IF;
END //
DELIMITER ;


-- calcular PROMEDIOS DE COMPETENCIA
DELIMITER //
CREATE PROCEDURE promedio_competencia(IN p_registro INT, IN p_estudiante INT)
BEGIN
    SELECT 
        C.Id_competencia,
        C.Competencia,
        AVG(NR.Nota) AS Promedio_competencia,
        clasificacion_literal(AVG(NR.Nota)) AS Literal
    FROM Notas_Registro NR
    JOIN Indicadores I ON NR.Id_indicador = I.Id_indicador
    JOIN Competencias C ON NR.Id_competencia = C.Id_competencia
    WHERE NR.Numero_de_registro = p_registro
      AND NR.Codigo_estudiante = p_estudiante
    GROUP BY C.Id_competencia, C.Competencia;
END //
DELIMITER ;
-- promedio final del curso por estudiante
DELIMITER //
CREATE PROCEDURE promedio_final_estudiante(
    IN p_registro INT,
    IN p_estudiante INT
)
BEGIN
    SELECT 
        AVG(Nota) AS Promedio_final,
        clasificacion_literal(AVG(Nota)) AS Nota_literal
    FROM Notas_Registro
    WHERE Numero_de_registro = p_registro
      AND Codigo_estudiante = p_estudiante;
END //
DELIMITER ;
 

