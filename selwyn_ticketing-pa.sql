-- Create the Customers Table
CREATE TABLE customers (
    customer_id INT,
    first_name VARCHAR(50),
    family_name VARCHAR(50),
    date_of_birth DATE,
    email VARCHAR(100),
    PRIMARY KEY (customer_id)
);

-- Create the Events Table
CREATE TABLE events (
    event_id INT,
    event_name VARCHAR(100),
    age_restriction INT,
    capacity INT,
    event_date DATE,
    PRIMARY KEY (event_id)
);

-- Create the Event-Customer Relationship Table (for ticket sales)
CREATE TABLE ticket_sales (
    ticket_sales_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT,
    event_id INT,
    tickets_purchased INT,
    PRIMARY KEY (ticket_sales_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Insert Data into Customers Table
INSERT INTO customers (customer_id, first_name, family_name, date_of_birth, email)
VALUES
(1, 'Simon', 'Charles', '1952-07-15', 'simon@charles.nz'),
(2, 'Jane', 'Doe', '1992-06-21', 'jane@doe.nz'),
(3, 'John', 'Smith', '1985-01-10', 'john.smith@nzmail.com'),
(4, 'Emily', 'Johnson', '1990-03-18', 'emily.johnson@nzmail.com'),
(5, 'Michael', 'Williams', '1980-11-12', 'michael.williams@nzmail.com'),
(6, 'Sarah', 'Brown', '1993-05-22', 'sarah.brown@nzmail.com'),
(7, 'James', 'Davis', '1975-09-29', 'james.davis@nzmail.com'),
(8, 'Linda', 'Martinez', '1982-02-07', 'linda.martinez@nzmail.com'),
(9, 'David', 'Garcia', '2000-04-04', 'david.garcia@nzmail.com'),
(10, 'Robert', 'Johnson', '1995-07-25', 'robert.johnson@nzmail.com'),
(11, 'Jessica', 'Wilson', '1998-12-19', 'jessica.wilson@nzmail.com'),
(12, 'Daniel', 'Moore', '1991-08-31', 'daniel.moore@nzmail.com'),
(13, 'Thomas', 'Taylor', '1988-10-15', 'thomas.taylor@nzmail.com'),
(14, 'Karen', 'Anderson', '1994-01-06', 'karen.anderson@nzmail.com'),
(15, 'Paul', 'Thomas', '1997-11-02', 'paul.thomas@nzmail.com'),
(16, 'Nancy', 'Johnson', '1987-09-09', 'nancy.johnson@nzmail.com'),
(17, 'Laura', 'White', '1984-06-25', 'laura.white@nzmail.com'),
(18, 'Kevin', 'Moore', '1992-07-14', 'kevin.moore@nzmail.com'),
(19, 'Debbie', 'Martin', '1999-12-30', 'debbie.martin@nzmail.com'),
(20, 'Steven', 'Lee', '1986-03-02', 'steven.lee@nzmail.com');

-- Insert Data into Events Table
INSERT INTO events (event_id, event_name, age_restriction, capacity, event_date)
VALUES
(1, 'Selwyn Sounds 2025', 18, 50, '2025-03-01'),
(2, 'Winter Markets 2025', 16, 150, '2025-07-20'),
(3, 'Music Mania 2025', 21, 50, '2025-06-10'),
(4, 'Selwyn Christmas Parade 2025', 18, 60, '2025-12-25'),
(5, 'Tech Expo 2025', 12, 60, '2025-05-15');

-- Insert Data into Ticket-Sales Table
INSERT INTO ticket_sales (customer_id, event_id, tickets_purchased)
VALUES
(1, 1, 5),   
(2, 1, 8),   
(3, 1, 7),   
(4, 1, 4),   
(5, 1, 6),   
(6, 2, 5),   
(7, 2, 6),   
(8, 2, 7),   
(9, 2, 10),  
(10, 2, 8),  
(11, 2, 9),  
(12, 2, 5),  
(13, 2, 10), 
(14, 2, 4),  
(15, 2, 6),
(16, 3, 8),  
(17, 3, 6),
(18, 3, 8),
(19, 4, 10),  
(20, 4, 6),  
(1, 4, 8),  
(2, 4, 7),    
(3, 4, 6),    
(4, 5, 7),  
(5, 5, 9),   
(6, 5, 8),   
(7, 5, 5),   
(8, 5, 6);