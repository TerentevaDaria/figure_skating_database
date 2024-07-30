DO $$
BEGIN
IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'result_type') THEN
    CREATE TYPE result_type AS ENUM ('short_program', 'free_skate', 'total');
END IF;
END
$$;