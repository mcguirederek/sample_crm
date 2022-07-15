"""
Accepts "metadata" CSV and itterates through rows to construct tkinter widgets.
Widgets are added to dicts so they can easily be referenced later for configuration.
"""
import tkinter as tk
from tkinter import ttk
import csv
#create widgets
def build_widgets(csv_file,frame_dict,widget_dict,length_dict,master):
    """Accepts CSV and proccesses it to create tkinter widgets.
    Adds frames and widgets to resepctive dicts for reference later.
    """
    with open(csv_file,newline='') as metadata:
        reader= csv.reader(metadata, delimiter=',')
        next(reader,None) #skip first row of headers
        for md_row in reader:
            if md_row[2].lower() == "frame":
                frame = tk.Frame(
                    master,bd=2,
                    relief="groove"
                )
                frame.grid(
                    column=md_row[6],
                    row=md_row[7]
                )
                frame_dict[md_row[5]] = frame
            if md_row[2].lower() == "button":
                button = tk.Button(
                    frame_dict[md_row[3]],
                    text=md_row[0]
                )
                button.grid(
                    column=md_row[6],
                    row=md_row[7],
                    columnspan=md_row[9],
                    sticky=md_row[8],
                    padx=(3,3),
                    pady=(3,3)
                )
                widget_dict[md_row[5]] = button
            if md_row[2].lower() == "checkbutton":
                checkbutton_intvar = tk.IntVar()
                checkbutton = tk.Checkbutton(
                    frame_dict[md_row[3]],
                    text=md_row[0],
                    font=md_row[13],
                    variable=checkbutton_intvar
                )
                checkbutton.grid(
                    column=md_row[6],
                    row=md_row[7],
                    columnspan=md_row[9],
                    sticky=md_row[8],
                    padx=(2,2),
                    pady=(2,2)
                )
                widget_dict[md_row[5]] = checkbutton
                widget_dict[md_row[5]+"_intvar"] = checkbutton_intvar
            if md_row[2].lower() == "label":
                label = ttk.Label(
                    frame_dict[md_row[3]],
                    text=md_row[0],
                    font=md_row[13]
                )
                label.grid(
                    column=md_row[6],
                    row=md_row[7]
                )
            if md_row[2].lower() == "entry":
                entry = tk.Entry(frame_dict[md_row[3]])
                entry.grid(
                    column=md_row[6],
                    row=md_row[7],
                    columnspan=md_row[9],
                    sticky=md_row[8],
                    padx=(2,2),
                    pady=(2,2)
                )
                entry.config(width=md_row[10])
                widget_dict[md_row[5]] = entry
                length_dict[entry] = md_row[16]
                label = ttk.Label(
                    frame_dict[md_row[3]],
                    text=md_row[0],
                    font=md_row[13]
                )
                label.grid(
                    column=int(md_row[6])-1,
                    row=md_row[7],
                    columnspan=1,
                    sticky="e"
                )
            if md_row[2].lower() == "combobox":
                combobox = ttk.Combobox(frame_dict[md_row[3]])
                combobox.grid(
                    column=md_row[6],
                    row=md_row[7],
                    columnspan=md_row[9],
                    sticky=md_row[8],
                    padx=(2,2),
                    pady=(2,2)
                )
                combobox.config(width=md_row[10])
                widget_dict[md_row[5]] = combobox
                length_dict[combobox] = md_row[16]
                label = ttk.Label(
                    frame_dict[md_row[3]],
                    text=md_row[0],
                    font=md_row[13]
                )
                label.grid(
                    column=int(md_row[6])-1,
                    row=md_row[7],sticky="e"
                )
            if md_row[2].lower() == "notebook":
                notebook = ttk.Notebook(frame_dict[md_row[3]])
                notebook.grid(
                    column=md_row[6],
                    row=md_row[7],
                    columnspan=md_row[9],
                    sticky=md_row[8],
                    padx=(2,2),
                    pady=(2,2)
                )
                widget_dict[md_row[5]] = notebook
            if md_row[2].lower() == "notebook_tab":
                widget_dict[md_row[4]].add(
                    frame_dict[md_row[3]],
                    text=md_row[0]
                )
            if md_row[2].lower() == "treeview":
                header = md_row[14].split(',')
                columns = md_row[15].split(',')
                tree = ttk.Treeview(
                    frame_dict[md_row[3]],
                    columns=header,
                    show="headings",
                    height=md_row[11]
                )
                tree.pack(
                    side="left",
                    expand=True,
                    fill="both"
                )
                tree.grid_columnconfigure(0, weight=1)
                tree.grid_rowconfigure(0, weight=1)
                for width,column in enumerate(header):
                    tree.heading(
                        column,
                        text=column,
                        anchor="w"
                    )
                    tree.column(
                        column,
                        width=columns[width]
                    )
                widget_dict[md_row[5]] = tree
                style = ttk.Style()
                style.configure(
                    "Treeview.Heading",
                    font=md_row[13]
                )
                vertical_scrollbar = ttk.Scrollbar(
                    frame_dict[md_row[3]],
                    orient="vertical",
                    command=tree.yview
                )
                vertical_scrollbar.pack(side="right",fill="y")
                tree.configure(yscrollcommand=vertical_scrollbar.set)
