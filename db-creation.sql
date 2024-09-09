CREATE TABLE 
    IF NOT EXISTS merged_data (
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    Quantity INT NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    DeliveryAddress VARCHAR(255) NOT NULL,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Size VARCHAR(255) NOT NULL,
    PRIMARY KEY (OrderID, ProductID)
);
