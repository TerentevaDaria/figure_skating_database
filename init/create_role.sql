DO 
$do$ 
BEGIN 
IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE  rolname = 'creator') 
THEN 
CREATE USER creator WITH PASSWORD 'creator' CREATEDB;
END IF; 
END $do$;