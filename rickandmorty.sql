CREATE TABLE locations(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(100),
    dimension VARCHAR(150)
);

CREATE TABLE characters(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    status VARCHAR(100),
    species VARCHAR(100),
    gender VARCHAR(100),
    origin VARCHAR(150),
    location INT,
    image VARCHAR(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE episodes(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    episode VARCHAR(100),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);