# Sample CRM

Desktop application build using Python, tkinter, and a SQL Server database. The basic functionality is to select a customer from a combobox and have their information loaded into the respective widgets. From there you can edit customers, contacts, and products.

![samplecrm](/images/samplecrm.png)

The application has 3 metadata csv files. These drive which widgets get added to the application, where they are placed, labels (if applicable), font, etc.

1. metadata.csv - main GUI
2. contact_metadata.csv - contact dialog when you double click on contact treeview row in contact tab.
2. product_metadata.csv - product dialog when you double click on product treeview row in contact tab.

## Installation

* Configure appsettings.json - Update connection_string
* Run createdatabase.sql
* Run insert_sampledata

## License
MIT