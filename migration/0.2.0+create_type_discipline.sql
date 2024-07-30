DO $$
BEGIN
IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'discipline') THEN
    CREATE TYPE discipline AS ENUM ('men''s_singles', 'women''s_singles', 'pair_skating', 'ice_dance');
END IF;
END 
$$;