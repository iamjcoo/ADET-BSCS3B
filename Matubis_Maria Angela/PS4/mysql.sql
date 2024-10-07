CREATE TABLE adet_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    middle_initial VARCHAR(10),
    last_name VARCHAR(255),
    address TEXT,
    email_address VARCHAR(255),
    contact_number VARCHAR(25),
    password VARCHAR(255)  -- Added password column
);