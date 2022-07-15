USE [master]
CREATE DATABASE [SampleCRM2]
GO
USE [SampleCRM2]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[BillingCycles](
	[BillingCycleID] [int] IDENTITY(1,1) NOT NULL,
	[CycleName] [varchar](25) NULL,
	[CycleValue] [int] NULL,
	[Active] [bit] NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Contacts](
	[ContactID] [int] IDENTITY(1,1) NOT NULL,
	[CustomerID] [int] NULL,
	[Active] [bit] NULL,
	[PrimaryContact] [bit] NULL,
	[Title] [varchar](50) NULL,
	[FirstName] [varchar](50) NULL,
	[LastName] [varchar](50) NULL,
	[EmailAddress] [varchar](100) NULL,
	[PhoneNumber] [varchar](50) NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Countries](
	[CountryID] [int] IDENTITY(1,1) NOT NULL,
	[CountryName] [varchar](50) NULL,
	[Abbrev] [varchar](3) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CustomerAddress](
	[AddressID] [int] IDENTITY(1,1) NOT NULL,
	[CustomerID] [int] NULL,
	[Address1] [varchar](150) NULL,
	[Address2] [varchar](150) NULL,
	[City] [varchar](100) NULL,
	[StateID] [int] NULL,
	[CountryID] [int] NULL,
	[PostalCode] [varchar](16) NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CustomerProducts](
	[CustomerProductsID] [int] IDENTITY(1,1) NOT NULL,
	[CustomerID] [int] NULL,
	[ProductID] [int] NULL,
	[Quantity] [int] NULL,
	[Expiration] [datetime] NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Customers](
	[CustomerID] [int] IDENTITY(1,1) NOT NULL,
	[CompanyName] [varchar](200) NULL,
	[Active] [bit] NULL,
	[AutoPay] [bit] NULL,
	[PayCycle] [varchar](20) NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Products](
	[ProductID] [int] IDENTITY(1,1) NOT NULL,
	[ProductName] [varchar](100) NULL,
	[Active] [bit] NULL,
	[SKU] [varchar](50) NULL,
	[LastModified] [datetime] NULL,
	[LastModifiedBy] [varchar](50) NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[States](
	[StateID] [int] IDENTITY(1,1) NOT NULL,
	[StateName] [varchar](20) NULL,
	[Abbrev] [varchar](3) NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Contacts] ADD  DEFAULT ((1)) FOR [Active]
GO
ALTER TABLE [dbo].[Contacts] ADD  DEFAULT ((0)) FOR [PrimaryContact]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT ((1)) FOR [Active]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT ((0)) FOR [AutoPay]
GO
ALTER TABLE [dbo].[Products] ADD  DEFAULT ((1)) FOR [Active]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[DeleteContact]
  @ContactID INT
AS
BEGIN
  DELETE FROM Contacts WHERE ContactID = @ContactID
END
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[DeleteCustomerProduct]
  @CustomerProductsID INT
AS
BEGIN
  DELETE FROM CustomerProducts WHERE CustomerProductsID = @CustomerProductsID
END
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[DeleteCutomer]
  @CustomerID INT
AS
BEGIN
  DELETE FROM CustomerAddress WHERE CustomerID = @CustomerID
END
BEGIN
  DELETE FROM Contacts WHERE CustomerID = @CustomerID
END
BEGIN
  DELETE FROM Customers WHERE CustomerID = @CustomerID
END
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[DeleteProduct]
  @ProductID INT
AS
BEGIN
  DELETE FROM Products WHERE ProductID = @ProductID
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetAllActiveCustomers]
AS
  SELECT
	Customers.CustomerID,
	Customers.CompanyName
  FROM Customers
  WHERE
	Customers.Active = 1
  ORDER BY
    Customers.CompanyName
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetAllCustomerContacts]
  @CustomerID INT
AS
SELECT
  ContactID,
  Active,
  PrimaryContact,
  Title,
  FirstName,
  LastName,
  EmailAddress,
  PhoneNumber
FROM Contacts
WHERE
	CustomerID = @CustomerID
ORDER BY
  Contacts.PrimaryContact, Contacts.LastName, Contacts.FirstName
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetAllProducts]
AS
BEGIN
  SELECT
  *
  FROM Products
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetBillingCycles]
AS
SELECT
	BillingCycleID,
	CycleName
FROM BillingCycles
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetCustomer]
  @CustomerID INT
AS
SELECT
  Customers.CustomerID,
  Customers.CompanyName,
  Customers.Active,
  Customers.AutoPay,
  Customers.PayCycle,
  CustomerAddress.AddressID,
  CustomerAddress.Address1,
  CustomerAddress.Address2,
  CustomerAddress.City,
  States.StateName,
  Countries.CountryName,
  CustomerAddress.PostalCode
FROM Customers
  JOIN CustomerAddress ON CustomerAddress.CustomerID = Customers.CustomerID
  JOIN States ON States.StateID = CustomerAddress.StateID
  JOIN Countries ON Countries.CountryID = CustomerAddress.CountryID
WHERE 
  Customers.CustomerID = @CustomerID
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetCustomerProducts]
  @CustomerID INT
AS
  SELECT
  CP.CustomerProductsID,
  P.ProductName,
  CP.Quantity,
  CONVERT(VARCHAR,CP.Expiration,20) AS Expiration,
  P.SKU
  FROM CustomerProducts CP
  JOIN Products P ON P.ProductID = CP.ProductID
  WHERE
    CustomerID = @CustomerID
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetStates]
AS
SELECT
*
FROM States
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[InsertContact]
  @CustomerID INT,
  @Active BIT,
  @PrimaryContact BIT,
  @Title VARCHAR(50),
  @FirstName VARCHAR(50),
  @LastName VARCHAR(50),
  @EmailAddress VARCHAR(100),
  @PhoneNumber VARCHAR(50)
AS
BEGIN
  INSERT INTO Contacts (CustomerID,Active,PrimaryContact,Title,FirstName,LastName,EmailAddress,PhoneNumber,LastModified,LastModifiedBy)
  VALUES(@CustomerID,@Active,@PrimaryContact,@Title,@FirstName,@LastName,@EmailAddress,@PhoneNumber,GETUTCDATE(),SYSTEM_USER)
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[InsertCustomer]
  @CompanyName VARCHAR(200),
  @AutoPay BIT,
  @PayCycle VARCHAR(20),
  @Address1 VARCHAR(150),
  @Address2 VARCHAR(150),
  @City VARCHAR(100),
  @StateName VARCHAR(20),
  @CountryName VARCHAR(50),
  @PostalCode VARCHAR(16)
AS
DECLARE @NewCustomer TABLE (CustomerID INT)
DECLARE @CustomerID INT, @StateID INT, @CountryID INT
SET @StateID = (SELECT StateID FROM States WHERE StateName = @StateName)
SET @CountryID = ISNULL((SELECT CountryID FROM Countries WHERE CountryName = @CountryName),233)
BEGIN
  INSERT INTO Customers(CompanyName,AutoPay,PayCycle,LastModified,LastModifiedBy)
  OUTPUT inserted.CustomerID INTO @NewCustomer
  VALUES(@CompanyName,@AutoPay,@PayCycle,GETUTCDATE(),SYSTEM_USER)
      
  SET @CustomerID = (SELECT CustomerID FROM @NewCustomer)
END
BEGIN
  INSERT INTO CustomerAddress (CustomerID,Address1,Address2,City,StateID,CountryID,PostalCode,LastModified,LastModifiedBy)
  VALUES(@CustomerID,@Address1,@Address2,@City,@StateID,@CountryID,@PostalCode,GETUTCDATE(),SYSTEM_USER)
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[InsertCustomerProduct]
  @CustomerID INT,
  @ProductID INT,
  @Quantity INT,
  @Expiration DATETIME
AS
BEGIN
  INSERT INTO CustomerProducts (CustomerID,ProductID,Quantity,Expiration,LastModified,LastModifiedBy)
  VALUES (@CustomerID,@ProductID,@Quantity,@Expiration,GETUTCDATE(),SYSTEM_USER)
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[InsertProduct]
  @ProductName VARCHAR(100),
  @Active BIT,
  @SKU VARCHAR(50)
AS
BEGIN
  INSERT INTO Products (ProductName,Active,SKU,LastModified,LastModifiedBy)
  VALUES(@ProductName,@Active,@SKU,GETUTCDATE(),SYSTEM_USER)
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateContact]
  @ContactID INT,
  @Active BIT,
  @PrimaryContact BIT,
  @Title VARCHAR(50),
  @FirstName VARCHAR(50),
  @LastName VARCHAR(50),
  @EmailAddress VARCHAR(100),
  @PhoneNumber VARCHAR(50)
AS
BEGIN
  UPDATE Contacts SET
    Active = @Active,
	PrimaryContact = @PrimaryContact,
	Title = @Title,
	FirstName = @FirstName,
	LastName = @LastName,
	EmailAddress = @EmailAddress,
	PhoneNumber = @PhoneNumber,
	LastModified = GETUTCDATE(),
	LastModifiedBy = SYSTEM_USER
  WHERE
    ContactID = @ContactID
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateCustomer]
  @CustomerID INT,
  @CompanyName VARCHAR(200),
  @AutoPay BIT,
  @PayCycle VARCHAR(20),
  @Address1 VARCHAR(150),
  @Address2 VARCHAR(150),
  @City VARCHAR(100),
  @StateName VARCHAR(20),
  @CountryName VARCHAR(50),
  @PostalCode VARCHAR(16)
AS
DECLARE @StateID INT, @CountryID INT
SET @StateID = (SELECT StateID FROM States WHERE StateName = @StateName)
SET @CountryID = ISNULL((SELECT CountryID FROM Countries WHERE CountryName = @CountryName),233)

BEGIN
  UPDATE Customers SET 
    CompanyName = @CompanyName,
	AutoPay = @AutoPay,
	PayCycle = @PayCycle,
	LastModified = GETUTCDATE(),
	LastModifiedBy = SYSTEM_USER
  WHERE 
	CustomerID = @CustomerID
END
BEGIN
  UPDATE CustomerAddress SET
    Address1 = @Address1,
	Address2 = @Address2,
	City = @City,
	StateID = @StateID,
	CountryID = @CountryID,
	PostalCode = @PostalCode,
	LastModified = GETUTCDATE(),
	LastModifiedBy = SYSTEM_USER
  WHERE 
    CustomerID = @CustomerID
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateCustomerProduct]
  @CustomerProductsID INT,
  @Quantity INT,
  @Expiration VARCHAR(50)
AS
BEGIN
  UPDATE CustomerProducts SET
    Quantity = @Quantity,
	Expiration = CAST(@Expiration AS DATETIME),
	LastModified = GETUTCDATE(),
	LastModifiedBy = SYSTEM_USER
  WHERE
	CustomerProductsID = @CustomerProductsID
END
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateProduct]
  @ProductID INT,
  @ProductName VARCHAR(100),
  @Active BIT,
  @SKU VARCHAR(50)
AS
BEGIN
  UPDATE Products SET
    ProductName = @ProductName,
	Active = @Active,
	SKU = @SKU,
	LastModified = GETUTCDATE(),
	LastModifiedBy = SYSTEM_USER
  WHERE
    ProductID = @ProductID
END
GO
