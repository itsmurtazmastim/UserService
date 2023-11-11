--SELECT 'CREATE DATABASE userservice'
--WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'userservice')\gexec;
--GRANT ALL PRIVILEGES ON DATABASE userservice TO postgres;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'userservice') THEN
    CREATE DATABASE userservice;
    GRANT ALL PRIVILEGES ON DATABASE userservice TO postgres;
  END IF;
END $$;
