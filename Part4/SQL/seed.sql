-- Insert an initial user (admin)
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    is_active,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',  -- Unique user ID (UUID)
    'Admin',                                  -- First name
    'HBnB',                                   -- Last name
    'admin@hbnb.io',                          -- Email address
    '$2b$12$MI0/rfWswl7cNCR8NP7gaOIEYmGeIdaX4GvoVExhU2xlH8mQW.8Qq',  -- Password hash (bcrypt)
    TRUE,                                     -- Admin flag (TRUE = Admin)
    TRUE,                                     -- Active status (TRUE = Active)
    CURRENT_TIMESTAMP,                        -- Created at (current timestamp)
    CURRENT_TIMESTAMP                         -- Updated at (current timestamp)
);

-- Create initial amenities
INSERT INTO amenities (
    id,
    name,
    description,
    created_at,
    updated_at
) VALUES
    ('550e8400-e29b-41d4-a716-446655440000',  -- Unique amenity ID (UUID)
     'WiFi',                                  -- Amenity name
     'High-speed wireless internet',          -- Description
     CURRENT_TIMESTAMP,                       -- Created at (current timestamp)
     CURRENT_TIMESTAMP                        -- Updated at (current timestamp)
    ),
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8',  -- Unique amenity ID (UUID)
     'Swimming Pool',                         -- Amenity name
     'Outdoor swimming pool',                 -- Description
     CURRENT_TIMESTAMP,                       -- Created at (current timestamp)
     CURRENT_TIMESTAMP                        -- Updated at (current timestamp)
    ),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c9',  -- Unique amenity ID (UUID)
     'Air Conditioning',                      -- Amenity name
     'Climate control system',                -- Description
     CURRENT_TIMESTAMP,                       -- Created at (current timestamp)
     CURRENT_TIMESTAMP                        -- Updated at (current timestamp)
    );
