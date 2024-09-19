CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) NOT NULL,
    CHECK (role IN ('IT', 'Manager','Data Science', 'Data Analyst')),
    userlevel VARCHAR(50) NOT NULL,
    CHECK (userlevel IN ('admin', 'user'))
);

INSERT INTO users (username, password, phone, role, userlevel)
VALUES
    ('admin1', 'password123', '123-456-7890', 'IT', 'admin'),
    ('user1', 'password456', '234-567-8901', 'Data Science', 'user'),
    ('admin2', 'password789', '345-678-9012', 'Data Analyst', 'admin'),
    ('user2', 'password012', '456-789-0123', 'Manager', 'user'),
    ('admin3', 'password345', '567-890-1234', 'IT', 'admin');

