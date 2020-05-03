--Написати PL/SQL код, що заносить тестові дані в одну з таблиць, 
--що були спроектовані у Лабораторній роботі №2, використавши LOOP. 
--Таблиця повинна містити мінімум два атрибути.

--
--Had to make insert into 3 tables becouse I have no table with 2 or mor
--columns without FK
--

SET SERVEROUTPUT ON

DECLARE 
    v_museum_state museum_location.m_state%type;
    v_museum_city museum_location.city%type;


BEGIN
    FOR i IN 1..15 LOOP
        INSERT INTO museum_state (m_state)
        VALUES (i || '_state');
        
        INSERT INTO museum_city (city)
        VALUES (i || '_city');
        
        INSERT INTO museum_location (m_state, city)
        VALUES (i || '_state', i || '_city');
    END LOOP;
END;