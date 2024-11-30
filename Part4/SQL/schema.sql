-- Create 'users' table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,                      -- Unique identifier for each user (UUID)
    first_name VARCHAR(255) NOT NULL,              -- First name of the user
    last_name VARCHAR(255) NOT NULL,               -- Last name of the user
    email VARCHAR(255) UNIQUE NOT NULL,            -- Email, must be unique for each user
    password VARCHAR(255) NOT NULL,                -- Hashed password for the user
    is_admin BOOLEAN DEFAULT FALSE                -- Boolean indicating if the user is an admin (default is false)
);

-- Create 'places' table if it doesn't exist
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,                      -- Unique identifier for each place (UUID)
    title VARCHAR(255) NOT NULL,                   -- Title or name of the place
    description TEXT,                              -- Description of the place
    price DECIMAL(10, 2) NOT NULL,                 -- Price per night (up to 10 digits, 2 decimal places)
    latitude FLOAT NOT NULL,                       -- Latitude for the geographical location
    longitude FLOAT NOT NULL,                      -- Longitude for the geographical location
    owner_id CHAR(36),                             -- Foreign key linking to the owner (user) of the place
    FOREIGN KEY (owner_id) REFERENCES users(id)   -- Ensure that each place is owned by a valid user
);

-- Create 'reviews' table if it doesn't exist
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,                      -- Unique identifier for each review (UUID)
    text TEXT NOT NULL,                            -- Review text written by the user
    rating INT CHECK(rating BETWEEN 1 AND 5) NOT NULL,  -- Rating between 1 and 5, ensuring valid rating
    user_id CHAR(36),                              -- Foreign key linking to the user who wrote the review
    place_id CHAR(36),                             -- Foreign key linking to the place being reviewed
    FOREIGN KEY (user_id) REFERENCES users(id),   -- Ensure that the review is written by a valid user
    FOREIGN KEY (place_id) REFERENCES places(id), -- Ensure that the review is for a valid place
    CONSTRAINT unique_review UNIQUE (user_id, place_id)  -- Ensures each user can only leave one review per place
);

-- Create 'amenities' table if it doesn't exist
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,                      -- Unique identifier for each amenity (UUID)
    name VARCHAR(255) UNIQUE NOT NULL              -- Name of the amenity, must be unique (e.g., pool, Wi-Fi)
);

-- Create 'place_amenities' table to map places to amenities if it doesn't exist
CREATE TABLE IF NOT EXISTS place_amenities (
    place_id CHAR(36),                             -- Foreign key linking to the place
    amenity_id CHAR(36),                           -- Foreign key linking to the amenity
    PRIMARY KEY (place_id, amenity_id),            -- Composite primary key ensuring unique pairs of place and amenity
    FOREIGN KEY (place_id) REFERENCES places(id),  -- Ensure that each place exists
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) -- Ensure that each amenity exists
);
