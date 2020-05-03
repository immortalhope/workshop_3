--
--After a little research I've defined 
--tables that are used in each SQL-request.
--They are museum and museum_type.
--So here is created the view called type_museum.
--

CREATE OR REPLACE VIEW type_myseum AS
SELECT 
museum.museum_id
,museum.museum_name
,museum.m_state
,museum.city
,museum_type.museum_type 
FROM museum
INNER JOIN museum_type ON museum.museum_type = museum_type.museum_type;
