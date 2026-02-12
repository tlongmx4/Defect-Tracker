DROP TABLE IF EXISTS defects;

CREATE TABLE defects (
    id UUID PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reported_by TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    absn TEXT NOT NULL CHECK (absn ~ '^[0-9]{4}$'),
    assigned_to TEXT,
    status TEXT NOT NULL CHECK (status IN ('open', 'repaired'))
);