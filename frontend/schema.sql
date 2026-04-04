CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password TEXT,
    balance FLOAT
);

CREATE TABLE portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stock_symbol VARCHAR(10),
    quantity INT,
    avg_price FLOAT,
    UNIQUE(user_id, stock_symbol)
);