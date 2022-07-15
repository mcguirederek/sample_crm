"""
Author: Derek McGuire
Description:
Process CSV and dynaically create GUI using tkinter.
Widget objects are added to dictionary so they can be referenced later when inserting
or delting data.
"""
import logging
import tkinter as tk
from tkinter import ttk
import json
import pyodbc
import widget_builder


def config_parser(file_path,key):
    """Parses json config file returning value for given key."""
    try:
        with open(file_path,"r") as config_file:
            return_value = json.load(config_file)[key]
        return return_value
    except FileNotFoundError:
        APP_LOG.error("%s not found. Please check path and try again.",file_path)
    return None


def sql_executer(constring,sqlstmt,params=None):
    """
    Accepts connection string and SQL statement, and parameters to run.
    Logs errors to file
    """
    pyodbc.pooling = False
    dataset = []
    try:
        cnxn = pyodbc.connect(constring)
        cursor = cnxn.cursor()
        if params is None:
            cursor.execute(sqlstmt)
        else:
            cursor.execute(sqlstmt,params)
        if cursor.description is not None:
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = dict(zip(columns, row))
                dataset.append(result)
        cnxn.commit()
        cnxn.close()
    except pyodbc.Error as err:
        APP_LOG.error(err)
    return dataset


class Gui:
    """Graphical user interface to view customers, products, and contacts"""
    def __init__(self):
        self.widgets = {}
        self.contact_widgets = {}
        self.product_widgets = {}
        self.widget_lenths = {}
        self.frames = {}
        self.active_customers = []
        self.checkbutton_vars = {}
        self.main_gui = tk.Tk()
        self.main_gui.resizable(
            width=True,
            height=True
        )
        self.main_gui.title("Sample CRM")
        try:
            widget_builder.build_widgets(
                METADATA_FILE,
                self.frames,
                self.widgets,
                self.widget_lenths,
                self.main_gui
            )
        except FileNotFoundError:
            APP_LOG.error("%s not found. Please check path and try again.",METADATA_FILE)
        self.load_combobox_values(
            "customer_combobox",
            "EXEC GetAllActiveCustomers",
            "CompanyName",
            None,
        )
        self.widgets["customer_combobox"].bind(
            "<<ComboboxSelected>>",
            self.get_customer
        )

        self.change_widget_state(
            ("checkbox_frame","main_frame"),
            "disabled"
        )
        self.load_combobox_values(
            "state_combobox",
            "EXEC [GetStates]",
            "StateName",
            None
        )
        self.load_combobox_values(
            "pay_cycle_combobox",
            "GetBillingCycles",
            "CycleName",
            None
        )
        self.widgets["add_button"].config(command=self.add_customer)
        self.widgets["save_button"].config(command=self.save_customer,state="disabled")
        self.widgets["edit_button"].config(command=self.edit_customer,state="disabled")
        self.widgets["contact_tree"].bind("<Double-1>",self.edit_contact)
        self.widgets["product_tree"].bind("<Double-1>",self.edit_product)
        self.register_callback = self.main_gui.register(self.validate_entry)
        self.bind_validate_command(self.widgets)

    def __str__(self):
        return "This is a GUI class"


    def bind_validate_command(self,widget_dict):
        """Bind callback to entry widgets."""
        for widget in widget_dict.values():
            if isinstance(widget,tk.Entry):
                widget.config(
                    validate="key",
                    validatecommand=(self.register_callback, "%P")
                )


    def change_widget_state(self,frames,state):
        """Change state of all widgets in frame(s)"""
        for frame in frames:
            for child in self.frames[frame].children.values():
                child.config(state=state)
        self.widgets["customer_combobox"].config(state="normal")


    def delete_widget_values(self,frames,ignore_combobox=None):
        """Deletes values from all widgets in frame(s)"""
        for frame in frames:
            for child in self.frames[frame].children.values():
                if isinstance(child,ttk.Combobox) and ignore_combobox is False:
                    child.set("")
                if isinstance(child,ttk.Treeview):
                    child.delete(*child.get_children())
                #isinstance(child,tk.Entry) will return true for ttk.Combobox
                if isinstance(child,tk.Entry) and not isinstance(child,ttk.Combobox):
                    child.delete('0','end')
                if isinstance(child,tk.Text):
                    child.delete('1.0','end')
                if isinstance(child,tk.IntVar):
                    child.set(False)
        self.widgets["auto_pay_checkbutton_intvar"].set(False)


    def get_customer(self,event):
        """When a customer is selected from the combobox,
        load their data into corresponding fields"""
        self.change_widget_state(
            ("checkbox_frame","main_frame"),
            "normal"
        )
        self.delete_widget_values(
            ("checkbox_frame","main_frame","contact_frame","product_frame"),
            True
        )
        for customer in self.active_customers:
            if customer["CompanyName"] == self.widgets["customer_combobox"].get():
                customer_id = customer["CustomerID"]
        customer_data = sql_executer(
            CONNECTION_STRING,
            "EXEC GetCustomer ?",
            customer_id
        )
        customer_data = customer_data[0]
        self.widgets["customerno_entry"].insert("0",customer_data["CustomerID"])
        self.widgets["active_checkbutton_intvar"].set(int(customer_data["Active"]))
        self.widgets["auto_pay_checkbutton_intvar"].set(customer_data["AutoPay"])
        self.widgets["pay_cycle_combobox"].set(customer_data["PayCycle"])
        self.widgets["address1_entry"].insert("0",customer_data["Address1"])
        self.widgets["address2_entry"].insert("0",customer_data["Address2"])
        self.widgets["city_entry"].insert("0",customer_data["City"])
        self.widgets["state_combobox"].set(customer_data["StateName"])
        self.widgets["zip_entry"].insert("0",customer_data["PostalCode"])
        self.change_widget_state(("checkbox_frame","main_frame"),"disabled")
        contacts = sql_executer(
            CONNECTION_STRING,
            "EXEC GetAllCustomerContacts ?",
            customer_id
        )
        products = sql_executer(
            CONNECTION_STRING,
            "EXEC [GetCustomerProducts] ?",
            customer_id
        )
        self.load_tree_values("contact_tree",contacts)
        self.load_tree_values("product_tree",products)
        self.widgets["add_button"].config(state="normal")
        self.widgets["save_button"].config(state="disabled")
        self.widgets["edit_button"].config(state="normal")


    def load_tree_values(self,tree,source):
        """Accepts treeview name and path to CSV then inserts rows for customer"""
        for record in source:
            self.widgets[tree].insert(
                '',
                'end',
                values=list(record.values())
            )


    def load_combobox_values(self,combobox,sqlstmt,column,sql_params=None):
        """Load SQL dataset into specified combobox."""
        dataset = sql_executer(
            CONNECTION_STRING,
            sqlstmt,
            sql_params
        )
        dataset_list = []
        if len(dataset) > 0:
            for data in dataset:
                dataset_list.append(data[column])
        else:
            APP_LOG.info("Cannot populate combobox %s.",combobox)
        self.widgets[combobox].config(values=tuple(dataset_list))
        if combobox == "customer_combobox":
            self.active_customers = dataset


    def validate_entry(self,entry_input):
        """Validates entry input does not exceed database length"""
        return bool(len(entry_input) <= int(self.widget_lenths[self.main_gui.focus_get()]))


    def add_customer(self):
        """Clears widgets so new customer can be entered"""
        self.widgets["add_button"].config(state="disabled")
        self.widgets["save_button"].config(state="normal")
        self.widgets["edit_button"].config(state="disabled")
        self.change_widget_state(
            ("checkbox_frame","main_frame"),
            "normal"
        )
        self.delete_widget_values(
            ("checkbox_frame",
            "main_frame",
            "contact_frame",
            "product_frame"
            ),
            False
        )
        self.widgets["customerno_entry"].config(state="disabled")


    def save_customer(self):
        """Save customer record to database."""
        sql_params = []
        #Customer No will only be populated on existing customer so new customer won't have it.
        if (self.widgets["customerno_entry"].get() is not None
            and self.widgets["customerno_entry"].get() != ""
        ):
            sql = """EXEC UpdateCustomer  ?,?,?,?,?,?,?,?,?,?"""
            sql_params.append(self.widgets["customerno_entry"].get())

        else:
            sql = """EXEC InsertCustomer ?,?,?,?,?,?,?,?,?"""
        sql_params.append(self.widgets["customer_combobox"].get())
        sql_params.append(self.widgets["auto_pay_checkbutton_intvar"].get())
        sql_params.append(self.widgets["pay_cycle_combobox"].get())
        sql_params.append(self.widgets["address1_entry"].get())
        sql_params.append(self.widgets["address2_entry"].get())
        sql_params.append(self.widgets["city_entry"].get())
        sql_params.append(self.widgets["state_combobox"].get())
        sql_params.append(233)
        sql_params.append(self.widgets["zip_entry"].get())
        sql_executer(
            CONNECTION_STRING,
            sql,
            sql_params
        )
        self.change_widget_state(
            ("checkbox_frame","main_frame"),
            "disabled"
        )
        self.load_combobox_values(
            "customer_combobox",
            "EXEC GetAllActiveCustomers",
            "CompanyName",
            None,
        )
        self.widgets["add_button"].config(state="normal")
        self.widgets["save_button"].config(state="disabled")
        self.widgets["edit_button"].config(state="normal")
    def edit_customer(self):
        """Set widget states to normal to allow changes."""
        self.change_widget_state(
            ("checkbox_frame","main_frame"),
            "normal"
        )
        self.widgets["customerno_entry"].config(state="disabled")
        self.widgets["add_button"].config(state="normal")
        self.widgets["save_button"].config(state="normal")
        self.widgets["edit_button"].config(state="disabled")


    def edit_contact(self,event):
        """Loads contact treeview row into toplevel widget"""
        contact_frames = {}
        contact = self.widgets["contact_tree"].focus()
        temp = self.widgets["contact_tree"].item(contact,"values")
        true_false = lambda value: value == "True"
        contact_pop = tk.Toplevel(self.main_gui)
        contact_pop.title("Edit contact")
        contact_pop.resizable(
            height=True,
            width=True
        )
        contact_metadata = config_parser(CONFIG_FILE,"contact_metadata")
        try:
            widget_builder.build_widgets(
                contact_metadata,
                contact_frames,
                self.contact_widgets,
                self.widget_lenths,
                contact_pop
            )
        except FileNotFoundError:
            APP_LOG.error("%s not found. Please check path and try again.",contact_metadata)
        self.contact_widgets["contact_id_entry"].insert('0',temp[0])
        self.contact_widgets["contact_active_checkbox_intvar"].set(true_false(temp[1]))
        self.contact_widgets["contact_primary_checkbox_intvar"].set(true_false(temp[2]))
        self.contact_widgets["contact_title_entry"].insert('0',temp[3])
        self.contact_widgets["contact_firstname_entry"].insert('0',temp[4])
        self.contact_widgets["contact_lastname_entry"].insert('0',temp[5])
        self.contact_widgets["contact_email_entry"].insert('0',temp[6])
        self.contact_widgets["contact_phone_entry"].insert('0',temp[7])
        self.contact_widgets["contact_id_entry"].config(state="disabled")
        self.contact_widgets["contact_save_button"].config(command=self.save_contact)
        self.bind_validate_command(self.contact_widgets)

    def save_contact(self):
        """Save updated contact to database"""
        customer_id = self.widgets["customerno_entry"].get()
        sql_params = []
        sql_params.append(self.contact_widgets["contact_id_entry"].get())
        sql_params.append(self.contact_widgets["contact_active_checkbox_intvar"].get())
        sql_params.append(self.contact_widgets["contact_primary_checkbox_intvar"].get())
        sql_params.append(self.contact_widgets["contact_title_entry"].get())
        sql_params.append(self.contact_widgets["contact_firstname_entry"].get())
        sql_params.append(self.contact_widgets["contact_lastname_entry"].get())
        sql_params.append(self.contact_widgets["contact_email_entry"].get())
        sql_params.append(self.contact_widgets["contact_phone_entry"].get())
        sql_executer(
            CONNECTION_STRING,
            """EXEC UpdateContact ?,?,?,?,?,?,?,?""",
            sql_params
        )
        self.delete_widget_values(
            ["contact_frame"],
            True
        )
        contacts = sql_executer(
            CONNECTION_STRING,
            "EXEC GetAllCustomerContacts ?",
            customer_id
        )
        self.load_tree_values("contact_tree",contacts)


    def edit_product(self,event):
        """Loads product into new toplevel widget"""
        product_frames = {}
        product = self.widgets["product_tree"].focus()
        temp = self.widgets["product_tree"].item(product,"values")
        product_pop = tk.Toplevel(self.main_gui)
        product_pop.title("Edit Product")
        product_pop.resizable(
            height=True,
            width=True
        )
        product_metadata = config_parser(CONFIG_FILE,"product_metadata")
        try:
            widget_builder.build_widgets(
                product_metadata,
                product_frames,
                self.product_widgets,
                self.widget_lenths,
                product_pop
            )
        except FileNotFoundError:
            APP_LOG.error("%s not found. Please check path and try again.",product_metadata)
        self.product_widgets["productid_entry"].insert("0",temp[0])
        self.product_widgets["product_entry"].insert("0",temp[1])
        self.product_widgets["product_qty"].insert("0",temp[2])
        self.product_widgets["product_expiration"].insert("0",temp[3])
        self.product_widgets["product_sku"].insert("0",temp[4])
        self.product_widgets["productid_entry"].config(state="disabled")
        self.product_widgets["product_entry"].config(state="disabled")
        self.product_widgets["product_sku"].config(state="disabled")
        self.product_widgets["product_save_button"].config(command=self.save_product)
        self.bind_validate_command(self.product_widgets)

    def save_product(self):
        """Save updated customer product to database"""
        customer_id = self.widgets["customerno_entry"].get()
        sql_params = []
        sql_params.append(self.product_widgets["productid_entry"].get())
        sql_params.append(self.product_widgets["product_qty"].get())
        sql_params.append(self.product_widgets["product_expiration"].get())
        sql_executer(
            CONNECTION_STRING,
            """EXEC UpdateCustomerProduct ?,?,?""",
            sql_params
        )
        self.delete_widget_values(
            ["product_frame"],
            True
        )
        products = sql_executer(
            CONNECTION_STRING,
            """EXEC GetCustomerProducts ?""",
            customer_id
        )
        self.load_tree_values("product_tree",products)


CONFIG_FILE = "appsettings.json"
METADATA_FILE = config_parser(CONFIG_FILE,"metadata")
LOG_NAME = config_parser(CONFIG_FILE,"log_name")
CONNECTION_STRING = config_parser(CONFIG_FILE,"connection_string")

logging.basicConfig(
    filename=LOG_NAME,
    filemode="a",
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    level=logging.DEBUG
)
APP_LOG = logging.getLogger(LOG_NAME)

app = Gui()

if __name__ == "__main__":
    app.main_gui.mainloop()
