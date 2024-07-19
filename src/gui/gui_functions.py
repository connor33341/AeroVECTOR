# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:21:38 2021

@author: Guido di Pasquo
"""


import copy
import tkinter as tk
from tkinter import ttk
import numpy as np
from src.gui import gui_setup
from src.aerodynamics import rocket_functions
from src import warnings_and_cautions

DEG2RAD = np.pi / 180
RAD2DEG = 1 / DEG2RAD


"""
Functions necessary to make the GUI.

    Functions:
        move_tk_object -- Move a tk object.

    Classes:
        ActiveFileLabel -- Active file label on the bottom left.
        Tab -- Basic tab.
        TabWithCanvas -- Tab with a canvas.
"""


# Order in the savefile:
# Checkboxes
# combobox
# entry


def move_tk_object(obj, r=0, c=0, columnspan=1):
    """
    Move a tk object to the selected position.

    Parameters
    ----------
    obj : tk object
        Object to move.
    r : int, optional
        move to row r. The default is 0.
    c : int, optional
        move to column c. The default is 0.
    columnspan : int, optional
        columnspan of the object. The default is 1.

    Returns
    -------
    None.
    """
    obj.grid(row=r, column=c, columnspan=columnspan)


def points_2_param_fins(s):
    p_string = [0]*4
    s_float = []
    for element in s:
        a = element.split(",")
        s_float.append([float(a[0]), float(a[1])])
    pos_root = s_float[0][0]
    pos_tip = s_float[1][0] - s_float[0][0]
    c_root = s_float[3][0] - s_float[0][0]
    c_tip = s_float[2][0] - s_float[1][0]
    wingspan = s_float[1][1] - s_float[0][1]
    p_string[0] = str(pos_root) + ", " + str(c_root)
    p_string[1] = str(pos_tip) + ", " + str(c_tip)
    p_string[2] = str(wingspan)
    p_string[3] = "0.003"
    return p_string


class ActiveFileLabel:
    """
    Creates a label with the active file name.

    Methods
    -------
        create_label -- Creates the label.
        update -- Updates the label.

    """

    def __init__(self):
        self.r = 0
        self.c = 0

    def create_label(self, root):
        """
        Create the label in the canvas root, in the row = r and column = c.

        Parameters
        ----------
        root : tk canvas
            canvas where to create a label.
        r : int
            row (position).
        c : int
            column (position).

        Returns
        -------
        None.
        """
        self.canvas = root
        self.text = tk.StringVar()
        self.active_file_label = tk.Label(self.canvas, textvariable=self.text)
        self.active_file_label.grid(columnspan=2)
        self.active_file_label.place(x=10, y=535)

    def update(self, active_file):
        """
        Update the label with the new file name.

        Parameters
        ----------
        active_file : string
            File name.

        Returns
        -------
        None.
        """
        self.text.set("Active File is " + active_file)
        self.active_file_label.place(x=3, y=540)


class Tab:
    """
    Basic tab template with checkboxes, combobox and entries.

    Methods
    -------
        create_tab -- Creates the tab in the notebook.
        create_checkboxes -- Creates them in the tab.
        activate_all -- Activates everything in the tab.
        deactivate_all -- Deactivates everything in the tab.
        change_state -- Activates/Deactivates everything in the tab.
        create_combobox -- Creates comboboxes.
        create_entry -- Creates entries.
        populate -- fills the tab with the data.
        depopulate -- Deletes the data from the tab.
        get_configuration -- Returns the data in the tab (strings).
        get_configuration_destringed -- Returns the data in the tab.
        configure -- Sets the minimum size of the grid.
        create_active_file_label -- Creates the label.

    Class Methods:
        update_active_file_label -- Updates all labels.

    """

    objs = []

    def __init__(self, names_checkbox=None, names_combobox=None, names_entry=None):
        # List with tabs to update the active file label
        Tab.objs.append(self)
        if names_checkbox is not None:
            self.names_checkbox = names_checkbox
        else:
            self.names_checkbox = []
        self.checkbox_status = []
        self.checkbox = []
        if names_combobox is not None:
            self.names_combobox = names_combobox
        else:
            self.names_combobox = []
        self.combobox_options = []
        self.combobox = []
        self.combobox_label = []
        if names_entry is not None:
            self.names_entry = names_entry
        else:
            self.names_entry = []
        self.entry = []
        self.entry_label = []
        self.active_file_label = ActiveFileLabel()
        self.i = 0

    def create_tab(self, nb, name):
        """
        Create the new tab in the notebook nb and call it name.

        Parameters
        ----------
        nb : ttk notebook
            main notebook.
        name : string
            name of the tab.

        Returns
        -------
        None.
        """
        self.tab = tk.Frame(nb, width=500, height=500, padx=10, pady=10)
        # Adds it to the notebook
        nb.add(self.tab, text=name)

    def create_checkboxes(self, names_checkbox, r, c, s="W", disables_all=False):
        """
        Create the checkboxes starting at the row = r, column = c,
        using the list names_checkboxes to determine their order and names

        Parameters
        ----------
        names_checkbox : list of strings
            labels for the checkboxes.
        r : int
            starting row of the list of checkboxes.
        c : int
            starting column of the list of checkboxes.
        s : tk position ("S", "W", etc), optional
            where the labels are aligned. The default is "W".
        disables_all : bool, optional
            The first item will enable or disable the tab. Default is False.

        Returns
        -------
        None.
        """
        self.names_checkbox = copy.deepcopy(names_checkbox)
        # Creates list with the status of the checkboxes
        self.checkbox_status = ["False"] * len(self.names_checkbox)
        self.checkbox = [0]*len(self.names_checkbox)
        for i in range(len(self.names_checkbox)):
            # If the first checkbox disables the tab:
            if i == 0:
                if disables_all is True:
                    self.checkbox_status[i] = tk.StringVar()
                    self.checkbox[i] = tk.Checkbutton(self.tab,
                                                      text=self.names_checkbox[i],
                                                      variable=self.checkbox_status[i],
                                                      onvalue="True", offvalue="False",
                                                      command=self.change_state)
                    self.checkbox[i].deselect()
                    self.checkbox[i].grid(row=r+i, column=c, sticky=s)
                else:
                    self.checkbox_status[i] = tk.StringVar()
                    self.checkbox[i] = tk.Checkbutton(self.tab,
                                                      text=self.names_checkbox[i],
                                                      variable=self.checkbox_status[i],
                                                      onvalue="True", offvalue="False")
                    self.checkbox[i].deselect()
                    self.checkbox[i].grid(row=r+i, column=c, sticky=s)
                continue
            self.checkbox_status[i] = tk.StringVar()
            self.checkbox[i] = tk.Checkbutton(self.tab,
                                              text=self.names_checkbox[i],
                                              variable=self.checkbox_status[i],
                                              onvalue="True", offvalue="False")
            self.checkbox[i].deselect()
            self.checkbox[i].grid(row=r+i, column=c, sticky=s)

    def activate_all(self):
        """
        Activates all widgets in the tab.

        Returns
        -------
        None.
        """
        for i in range(len(self.checkbox)-1):
            self.checkbox[i+1].config(state="normal")
        for i in range(len(self.names_combobox)):
            self.combobox[i].config(state="normal")
        for i in range(len(self.entry)):
            self.entry[i].config(state="normal")

    def deactivate_all(self):
        """
        Deactivates all widgets in the tab.

        Returns
        -------
        None.
        """
        for i in range(len(self.checkbox)-1):
            self.checkbox[i+1].config(state="disable")
        for i in range(len(self.names_combobox)):
            self.combobox[i].config(state="disable")
        for i in range(len(self.entry)):
            self.entry[i].config(state="disable")

    def change_state(self):
        """
        If the tab widgets are enable, it disables them, and vise versa.

        Returns
        -------
        None.
        """
        # If the first checkbox disables all
        if self.checkbox_status[0].get() == "True":
            self.activate_all()
        else:
            self.deactivate_all()

    def create_combobox(self, options, names_combobox, r, c, s="E", w=20):
        """
        Create the comboboxes starting at the row = r, column = c,
        using the list names_combobox to determine their order and names
        and the nested list options as options of each combobox.

        Parameters
        ----------
        options : nested list of strings
            options of each combobox.
        names_combobox : list of strings
            label of each combobox.
        r : int
            starting row of the list of checkboxes.
        c : int
            starting column of the list of checkboxes.
        s : tk position ("S", "W", etc), optional
            where the labels are aligned. The default is "E".

        Returns
        -------
        None.
        """
        self.names_combobox = copy.deepcopy(names_combobox)
        self.combobox_options = copy.deepcopy(options)
        self.combobox = [0]*len(self.names_combobox)
        self.combobox_label = [0]*len(self.names_combobox)
        for i in range(len(self.names_combobox)):
            self.combobox[i] = ttk.Combobox(self.tab, width=w, state="readonly")
            self.combobox[i].grid(row=r+i, column=c+1, sticky=s)
            self.combobox[i]["values"] = options[i]
            self.combobox_label[i] = tk.Label(self.tab, text=self.names_combobox[i])
            self.combobox_label[i].grid(row=r+i, column=c, sticky=s)
            self.combobox[i].set(self.combobox_options[i][0])

    def create_entry(self, names_entry, r, c, s="E", w=20):
        """
        Create the entries starting at the row = r, column = c,
        using the list names_entry to determine their order and names

        Parameters
        ----------
        names_entry : list of strings
            labels for the entries.
        r : int
            starting row of the list of entries.
        c : int
            starting column of the list of entries.
        s : tk position ("S", "W", etc), optional
            where the labels are aligned. The default is "E".
        w : int, optional
            width of the entry. The default is 20.

        Returns
        -------
        None.
        """
        self.names_entry = copy.deepcopy(names_entry)
        self.entry = [0]*len(self.names_entry)
        self.entry_label = [0]*len(self.names_entry)
        for i in range(len(self.entry)):
            self.entry_label[i] = tk.Label(self.tab, text=self.names_entry[i])
            self.entry_label[i].grid(row=r+i, column=c, sticky="E")
            self.entry[i] = tk.Entry(self.tab, width=w)
            self.entry[i].grid(row=r+i, column=c+1, sticky=s)

    def populate(self, l0):
        """
        Populate the tab with the information in l0 (checkboxes status,
        combobox selected option, entries, in that order).

        Parameters
        ----------
        l0 : list of strings
            information of all the tab's widgets.

        Returns
        -------
        None.
        """
        # Fills the widgets with the data of the save file
        data = copy.deepcopy(l0)
        # Can't write to a disable widget
        self.activate_all()
        # Checkbox, combobox, entry
        n_check = len(self.checkbox)
        n_comb = len(self.names_combobox)
        n_ent = len(self.entry)
        for i in range(n_check):
            if data[i] == "True":
                self.checkbox[i].select()
            elif data[i] == "False":
                self.checkbox[i].deselect()
        for i in range(n_comb):
            self.combobox[i].set(data[i+n_check])
        for i in range(n_ent):
            self.entry[i].insert(0, data[i+n_check+n_comb])

    def depopulate(self):
        """
        Clear all the widgets.

        Returns
        -------
        None.
        """
        self.activate_all()
        for i in range(len(self.checkbox)):
            self.checkbox[i].deselect()
        for i in range(len(self.names_combobox)):
            self.combobox[i].set(self.combobox_options[i][0])
        for i in range(len(self.entry)):
            self.entry[i].delete(0, 150)

    def get_configuration(self):
        """
        Get the status and information of all the tab's widgets.

        Returns
        -------
        list of strings
            information in the tab.
        """
        # Creates list with the data from the widgets
        # Order is checkbox, combobox, entry
        d = []
        for i in range(len(self.checkbox)):
            d.append(self.checkbox_status[i].get())
        for i in range(len(self.combobox)):
            d.append(self.combobox[i].get())
        for i in range(len(self.entry)):
            d.append(self.entry[i].get())
        return copy.deepcopy(d)

    def _destring_data(self, data):
        """
        Transform a list of strings into variables.

        Parameters
        ----------
        data : list of strings
            Data to convert.

        Returns
        -------
        list of variables
            Destringed data.
        """

        def is_number(s):
            """Return True is string is a number."""
            try:
                float(s)
                return True
            except ValueError:
                return False

        def string_or_bool(s):
            """Return True if string == True."""
            if s == "True":
                return True
            if s == "False":
                return False
            return s

        def is_baudrate(f):
            """If f > 9000 almost certainly it's a baudrate."""
            return bool(f > 9000)
        for i, elem in enumerate(data):
            if is_number(data[i]):
                data[i] = float(data[i])
                if is_baudrate(data[i]):
                    data[i] = int(data[i])
            else:
                data[i] = string_or_bool(data[i])
        return data

    def get_configuration_destringed(self):
        """
        Get the status and information of all the tab's widgets (in variable
        format).

        Returns
        -------
        list of variables
            information in the tab.
        """
        data = self.get_configuration()
        data = self._destring_data(data)
        return copy.deepcopy(data)

    def configure(self, n=10):
        """
        Configure the tab with a minimum row and columns size of n.

        Parameters
        ----------
        n : int, optional
            Minimum size of the row/column. The default is 10.

        Returns
        -------
        None.
        """
        # creates the empty rows and columns
        # so as to have empty space between widgets
        col_count, row_count = self.tab.grid_size()
        for col in range(col_count):
            self.tab.grid_columnconfigure(col, minsize=n)
        for row in range(row_count):
            self.tab.grid_rowconfigure(row, minsize=n)

    def create_active_file_label(self):
        """
        Create a label with the active file name in the position row = r and
        column = c.

        Parameters
        ----------
        r : int
            position (row).
        c : int
            position (column).

        Returns
        -------
        None.
        """
        self.active_file_label.create_label(self.tab)

    @classmethod
    def update_active_file_label(cls, name):
        """
        Update the text in the active file label to match the new active file.

        Parameters
        ----------
        cls : Tab
            Tab.
        name : string
            Active file name.

        Returns
        -------
        None.
        """
        for obj in cls.objs:
            obj.active_file_label.update(name)


class TabWithCanvas(Tab):
    """
    For tabs with canvases.

    Methods
    -------
        set_points -- Sets the rocket component points.
        add_point -- Adds a point to the rocket component.
        delete_point -- Delets a point of the rocket components.
        get_points -- Returns the points of a rocket component (string).
        get_points_float -- Returns the points of a rocket component.
        create_canvas -- Creates the canvas.
        draw_rocket -- Draws the rocket.
        populate -- Fills the tab.
        get_configuration -- Returns the rocket's configuration in the tab (string).
        get_configuration_destringed -- Returns the rocket's configuration in the tab.
        populate -- fills the tab with the data.
        depopulate -- Deletes the data from the tab.
        change_state_fins -- Activate/deactivate fins.
    """

    def __init__(self):
        super().__init__()
        self.canvas_height = 0
        self.canvas_width = 0
        r"""
        points[0] -> rocket, points[1] -> fin
        Rocket points go from the tip down to the tail.
        Fin[n][x position (longitudinal), z position (span)]
         [0]|\
            | \[1]
            | |
         [3]|_|[2]
        """
        self.points = [["0,0", "0,0"],
                       ["0.001,0.001",
                        "0.001,0.001",
                        "0.001,0.001",
                        "0.001,0.001"],
                       ["0.001,0.001",
                        "0.001,0.001",
                        "0.001,0.001",
                        "0.001,0.001"]]
        self.param_fin = [["0, 0", "0, 0", "0", "0"],
                          ["0, 0", "0, 0", "0", "0"]]
        self.rocket = rocket_functions.Rocket()
        self.active_point = 0
        self.active_point_fins = 0
        self.flag_hollow_body = False
        self.aoa = 0.00000001
        self.aoa_ctrl_fin = 0
        self.tvc_angle = 0
        self.current_motor = ""
        self.velocity = 1
        self.rocket_length = 0
        self.max_fin_len = 0
        self.max_length = 0
        self.scale_y = 1
        self.centering = 0
        self.choose_cg = 2
        self.flight_time = 0.01
        self.prev_total_errors = 0
        self.point_diameter = 6

    def _sort(self, l):
        """
        Sort the data l.

        Parameters
        ----------
        l : list of strings or floats.
            data to sort.

        Returns
        -------
        list of floats.
            data sorted.
        """
        def _l2j_is_greater_than(l2, j):
            if float(l2[j].split(",")[0]) > float(l2[j+1].split(",")[0]):
                return True
            return False
        l2 = copy.deepcopy(l)
        for _ in range(len(l2)):
            for j in range(len(l2)-1):
                if _l2j_is_greater_than(l2, j):
                    b = l2[j]
                    l2[j] = l2[j+1]
                    l2[j+1] = b
        return copy.deepcopy(l2)

    def set_points(self, n, l):
        """
        Recieve a list and sets the points of the rocket body to it.

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin.
        l : list of strings
            points.

        Returns
        -------
        None.
        """
        self.points[n] = copy.deepcopy(l)

    def add_point(self, n, s):
        """
        Add the point "s" to the rocket part "n".

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin.
        s : string
            format: "x,z".

        Returns
        -------
        None.
        """
        self.points[n].append(s)
        self.points[n] = self._sort(self.points[n])
        if n == 0:
            # If it is from the body it goes to the combobox
            self.combobox[n]["values"] = self.points[n]
            self.combobox[n].set(s)
        else:
            for i in range(len(self.entry)):
                # else you delete the entries and populates them
                # with the points, it is not used
                self.entry[i].delete(0, 150)
                self.entry[i].insert(0, s)

    def delete_point(self, n, s):
        """
        Delete the point "s" form the rocket part "n".

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin.
        s : string
            format: "x,z".

        Returns
        -------
        None.
        """
        for i in range(len(self.points[n])):
            if n == 0:
                if self.points[n][i] == s:
                    del self.points[n][i]
                    self.combobox[n]["values"] = self.points[n]
                    self.combobox[n].set(self.points[n][i-1])
                    break

    def get_points(self, n):
        """
        Get the points of the rocket part "n" as strings.

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin..

        Returns
        -------
        Nested list of strings.
            points of the part "n".
        """
        return copy.deepcopy(self.points[n])

    def get_points_float(self, n):
        """
        Get the points of the rocket part "n" as floats.

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin.

        Returns
        -------
        Nested list of floats.
            points of the part "n".
        """
        l = copy.deepcopy(self.points[n])
        l2 = []
        for element in l:
            a = element.split(",")
            l2.append([float(a[0]), float(a[1])])
        return copy.deepcopy(l2)

    def get_param_fin(self, n):
        """
        Get the points of the rocket part "n" as strings.

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin..

        Returns
        -------
        Nested list of strings.
            points of the part "n".
        """
        return copy.deepcopy(self.param_fin[n])

    def get_param_fin_float(self, n):
        """
        Get the points of the rocket part "n" as floats.

        Parameters
        ----------
        n : int
            n = 0 = body, 1 = stabilization fin, 2 = control fin.

        Returns
        -------
        Nested list of floats.
            points of the part "n".
        """
        l = copy.deepcopy(self.param_fin[n])
        l2 = []
        zero = 0.0000000001
        for i in range(2):
            a = l[i].split(",")
            l2.append([float(a[0]) + zero, float(a[1]) + zero])
        for i in range(2):
            a = l[i+2]
            l2.append(float(a) + zero)
        return copy.deepcopy(l2)

    def create_canvas(self, canvas_width, canvas_height):
        """
        Create a canvas of determined width and height

        Parameters
        ----------
        canvas_width : int
            Canvas width.
        canvas_height : int
            Canvas height.

        Returns
        -------
        None.
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = (tk.Canvas(self.tab, width=self.canvas_width,
                                 heigh=self.canvas_height, bg="white"))
        self.canvas.grid(row=0, column=0, rowspan=20)
        self._create_labels()

    def _create_labels(self):
        self.n_force_label = tk.Label(self.tab, text="")
        self.n_force_label.grid(row=14, column=3)
        self.f_point_label = tk.Label(self.tab, text="")
        self.f_point_label.grid(row=15, column=3)
        self.moment_label = tk.Label(self.tab, text="")
        self.moment_label.grid(row=16, column=3)
        self.thrust_label = tk.Label(self.tab, text="")
        self.thrust_label.grid(row=17, column=3)
        self.warn_and_cau_label = tk.Label(self.tab, text="")
        self.warn_and_cau_label.place(x=3, y=520)
        self.stalled_stabilization_fins_label = tk.Label(self.tab, text="")
        self.stalled_stabilization_fins_label.place(x=3, y=430)
        self.stalled_control_fins_label = tk.Label(self.tab, text="")
        self.stalled_control_fins_label.place(x=3, y=410)

    def draw_rocket(self):
        """
        Draws the rocket using the set points.

        Returns
        -------
        None.
        """
        """
        x in the canvas is y/z in the rocket
        y in the canvas is x in the rocket
        """
        self._update_scale_limits()
        self.update_full_rocket()
        self.canvas.delete("all")
        l2 = self.get_points_float(0)
        self.rocket_length = l2[-1][0]
        self._calculate_bounding_box()
        if self.rocket_length != 0:
            canvas_h_to_w_ratio = self.canvas_height / self.canvas_width
            length_relative = self.max_length
            width_relative = self.max_width * canvas_h_to_w_ratio * 2.1
            if width_relative < length_relative:
                self.scale_y = self.canvas_height / self.max_length * 0.93
            else:
                self.scale_y = self.canvas_width / self.max_width / 2.1
        else:
            self.scale_y = 1
        # Centers the rocket in the horizontal
        self.centering = (self.canvas_height-self.max_length*self.scale_y) / 2
        self._re_draw_rocket(l2)
        if self.checkbox_status[1].get() == "True":
            self.points[1] = self.param_2_points_fins(self.param_fin[0])
            fin_stab_points = self.get_points_float(1)
            attached = self.checkbox_status[2].get()
            separate = "False"
            self._draw_fins(fin_stab_points, "black", attached, separate)
            if self.checkbox_status[3].get() == "True":
                self.points[2] = self.param_2_points_fins(self.param_fin[1])
                fin_control_points = self.get_points_float(2)
                attached = self.checkbox_status[4].get()
                separate = "True"
                self._draw_fins(fin_control_points, "red", attached, separate)

    def _calculate_bounding_box(self):
        fin_stab_points = self.get_points_float(1)
        fin_control_points = self.get_points_float(2)
        max_fin_stab_length = self._calculate_max_length_fins(fin_stab_points)
        max_fin_stab_width = fin_stab_points[1][1]
        max_fin_control_length = self._calculate_max_length_fins(fin_control_points)
        max_fin_control_width = fin_control_points[1][1]
        if max_fin_stab_length > max_fin_control_length:
            self.max_fin_len = max_fin_stab_length
        else:
            self.max_fin_len = max_fin_control_length
        if max_fin_stab_width > max_fin_control_width:
            self.max_fin_width = fin_stab_points[1][1]
        else:
            self.max_fin_width = fin_control_points[1][1]
        if self.max_fin_width > self.rocket.max_diam:
            self.max_width = self.max_fin_width
        else:
            self.max_width = self.rocket.max_diam
        if self.checkbox_status[1].get() == "True":
            if self.rocket_length > self.max_fin_len:
                self.max_length = self.rocket_length
            else:
                self.max_length = self.max_fin_len
        else:
            self.max_length = self.rocket_length

    def _calculate_max_length_fins(self, s):
        current_max = 0
        for i in range(4):
            if s[i][0] > current_max:
                current_max = s[i][0]
        return current_max

    def _re_draw_rocket(self, l2):
        # x in the canvas is y/z in the rocket
        # y in the canvas is x in the rocket
        for i in range(len(l2)-1):
            # checkbox_status[0] is the Ogive
            if i == 0 and self.checkbox_status[0].get() == "True":
                radius_nc = l2[1][1] / 2
                len_nc = l2[1][0]
                rho_radius = (radius_nc**2 + len_nc**2) / (2*radius_nc)
                x_ogive_1 = 0
                # y = np.sqrt(rho_radius**2 - (len_nc-x_ogive_1)**2)+radius_nc-rho_radius
                # Draws an ogive with 20 points
                resolution = 20
                for j in range(resolution):
                    x_ogive_2 = x_ogive_1 + len_nc/resolution
                    y_ogive_1 = (np.sqrt(rho_radius**2 - (len_nc-x_ogive_1)**2)
                                 + radius_nc - rho_radius)
                    y_ogive_2 = (np.sqrt(rho_radius**2 - (len_nc-x_ogive_2)**2)
                                 + radius_nc - rho_radius)
                    x1 = (y_ogive_1*self.scale_y + self.canvas_width / 2)
                    y1 = x_ogive_1*self.scale_y + self.centering
                    x2 = (y_ogive_2*self.scale_y + self.canvas_width / 2)
                    y2 = x_ogive_2*self.scale_y + self.centering
                    x1_mirror = (-y_ogive_1*self.scale_y + self.canvas_width / 2)
                    x2_mirror = (-y_ogive_2*self.scale_y + self.canvas_width / 2)
                    self.canvas.create_line(x1, y1, x2, y2)
                    self.canvas.create_line(x1_mirror, y1, x2_mirror, y2)
                    x_ogive_1 += len_nc/resolution
                    if j == 0:
                        self.rocket_origin_canvas = y1
                self.canvas.create_line(x2_mirror, y2, x2, y2)
            else:
                # Conic nosecone / rest of the body
                x1 = (l2[i][1]*self.scale_y + self.canvas_width) / 2
                y1 = l2[i][0]*self.scale_y + self.centering
                x2 = (l2[i+1][1]*self.scale_y + self.canvas_width) / 2
                y2 = l2[i+1][0]*self.scale_y + self.centering
                x1_mirror = (-l2[i][1]*self.scale_y + self.canvas_width) / 2
                x2_mirror = (-l2[i+1][1]*self.scale_y + self.canvas_width) / 2
                self.canvas.create_line(x1, y1, x2, y2)
                self.canvas.create_line(x1_mirror, y1, x2_mirror, y2)
                self.canvas.create_line(x2_mirror, y2, x2, y2)
                if i == 0:
                    self.rocket_origin_canvas = y1
        self._create_point_cp()
        self._create_point_xcg()
        self._update_labels()

    def _draw_points(self):
        #self._create_point_xcg()
        self.canvas.delete(self.xcg_point_canvas, self.cp_point_canvas)
        self._update_scale_limits()
        self._create_point_cp()
        self._create_point_xcg()
        self._update_labels()

    def _create_point_cp(self):
        # Creates a point where the CP is located
        # the slider can move it by modifying the aoa
        f = self.point_diameter / 2
        v = self.transform_AoA_2_v(self.aoa) * self.velocity
        cn, cm, ca, cp_point = self.rocket.calculate_aero_coef(v_loc_tot=v,
                                                               actuator_angle=self.aoa_ctrl_fin)
        self.normal_force, self.force_app_point = self._calculate_total_cn_cp(cn, cp_point)
        self._set_f_app_point_color(self.normal_force)
        self.cp_point_canvas = self.canvas.create_oval(self.canvas_width/2-f,
                                                       (self.force_app_point*self.scale_y
                                                        - f
                                                        + self.rocket_origin_canvas),
                                                       self.canvas_width/2 + f,
                                                       (self.force_app_point*self.scale_y
                                                        + f
                                                        + self.rocket_origin_canvas),
                                                       fill=self.f_app_colour,
                                                       outline=self.f_app_colour)

    def transform_AoA_2_v(self, aoa):
        if aoa <= -np.pi/2:
            v = [-1, -np.tan(aoa)]/np.sqrt(1+np.tan(aoa)**2)
        elif aoa <= 0:
            v = [1, np.tan(aoa)]/np.sqrt(1+np.tan(aoa)**2)
        elif aoa <= np.pi/2:
            v = [1, np.tan(aoa)]/np.sqrt(1+np.tan(aoa)**2)
        else:
            v = [-1, -np.tan(aoa)]/np.sqrt(1+np.tan(aoa)**2)
        return v

    def _update_scale_limits(self):
        mass_parameters = [0]*6
        for i in range(6):
            mass_parameters[i] = float(gui_setup.param_file_tab.entry[i].get())
        # self.rocket.update_rocket(self.get_configuration_destringed(), mass_parameters)
        self.rocket.update_mass_parameters(mass_parameters)
        data = gui_setup.param_file_tab.get_configuration_destringed()
        max_actuator_angle = data[9]
        servo_def = data[8]
        reduction = data[10]
        if reduction != 0:
            resolution = servo_def/reduction
        else:
            resolution = 1
        if max_actuator_angle == "":
            max_actuator_angle = 10
        self.scale_act_angle.config(from_=-max_actuator_angle,
                                    to=max_actuator_angle,
                                    resolution=resolution)
        self.scale_time.config(to=self.rocket.t_burnout)

    def update_full_rocket(self):
        mass_parameters = [0]*6
        for i in range(6):
            mass_parameters[i] = float(gui_setup.param_file_tab.entry[i].get())
        self.rocket.update_rocket(self.get_configuration_destringed(), mass_parameters)

    def _calculate_total_cn_cp(self, cn, cp_point):
        q = 0.5 * 1.225 * self.velocity**2
        aero_force = q * self.rocket.area_ref * cn
        thrust = self._get_motor_thrust()
        xt = float(gui_setup.param_file_tab.entry[6].get())
        normal_force = thrust*np.sin(self.tvc_angle) + aero_force
        force_app_point = ((aero_force*cp_point + thrust*np.sin(self.tvc_angle) * xt)
                           / normal_force)
        return normal_force, force_app_point

    def _get_motor_thrust(self):
        if self.current_motor != gui_setup.param_file_tab.combobox[0].get():
            gui_setup.savefile.read_motor_data(gui_setup.param_file_tab.combobox[0].get())
            self.rocket.set_motor(gui_setup.savefile.get_motor_data())
            self.current_motor = gui_setup.param_file_tab.combobox[0].get()
            self.thrust = self.rocket.get_thrust(self.flight_time, 0)
        else:
            self.thrust = self.rocket.get_thrust(self.flight_time, 0)
        return self.thrust

    def _set_f_app_point_color(self, cn):
        if cn <= 0:
            self.f_app_colour = "red"
        else:
            self.f_app_colour = "green"

    def _create_point_xcg(self):
        f = self.point_diameter / 2
        self.xcg_point = self.rocket.get_xcg(self.flight_time, 0)
        self.xcg_point_canvas = self.canvas.create_oval(self.canvas_width/2 - f,
                                                        (self.xcg_point*self.scale_y
                                                         - f
                                                         + self.rocket_origin_canvas),
                                                        self.canvas_width/2 + f,
                                                        (self.xcg_point*self.scale_y
                                                         + f + self.rocket_origin_canvas),
                                                        fill="blue", outline="blue")

    def _update_labels(self):
        n_force = "N Force = " + str(round(self.normal_force, 3)) + " N"
        f_point = "Force App point = " + str(round(self.force_app_point, 4)) + " m"
        moment = self.normal_force * (self.force_app_point-self.xcg_point)
        moment_text = "Moment = " + str(round(moment, 3)) + " N.m"
        thrust_text = "T = " + str(round(self.rocket.get_thrust(self.flight_time, 0), 3)) + " N"
        self.n_force_label.config(text=n_force)
        self.f_point_label.config(text=f_point)
        self.moment_label.config(text=moment_text)
        self.thrust_label.config(text=thrust_text)
        warn, cau, new_event = warnings_and_cautions.w_and_c.check_warnings_and_cautions()
        if warn == 0 and cau == 0:
            c_and_w_text = ""
            color = self.tab.cget("background")
            color2 = self.tab.cget("background")
        else:
            c_and_w_text = str(warn) + " WARNINGS and " + str(cau) + " CAUTIONS active in the console."
            if warn > 0:
                color = "red"
                color2 = "white"
            elif cau > 0:
                color = "yellow"
                color2 = "black"
        self.warn_and_cau_label.config(text=c_and_w_text, bg=color, fg=color2)
        total_errors = warn + cau
        if total_errors != self.prev_total_errors and total_errors == 0:
            print("\nAll warnings or cautions have been corrected, good work :). \n")
        self.prev_total_errors = total_errors

        stalled_fins = warnings_and_cautions.w_and_c.check_stalled_fins()
        stalled_stab_fin_text, stalled_control_fins_text = "", ""
        if stalled_fins[0] is True:
            stalled_stab_fin_text = "Stabilization fin stalled!"
        if stalled_fins[1] is True:
            stalled_control_fins_text = "Control fin stalled!"
        self.stalled_stabilization_fins_label.config(text=stalled_stab_fin_text, bg="white")
        self.stalled_control_fins_label.config(text=stalled_control_fins_text, bg="white")

    def _draw_fins(self, l2, s, attached, separate):
        """
        Stabilization fins are attached to a hollow
        body, therefore they lose a lot of lift but
        aren't physically separated from the body.
        Control fins are attached  to a servo and they
        are a distance apart from the body (or not,
        it depends on the rocket)
        """
        if separate == "True" and attached == "False":
            sep = l2[0][1] / 3
        else:
            sep = 0
        # Draws the fin
        for i in range(len(l2)-1):
            x1 = (l2[i][1]+sep) * self.scale_y + self.canvas_width/2
            y1 = l2[i][0]*self.scale_y + self.centering
            x2 = (l2[i+1][1]+sep) * self.scale_y + self.canvas_width/2
            y2 = l2[i+1][0]*self.scale_y + self.centering
            x1_mirror = -(l2[i][1]+sep) * self.scale_y + self.canvas_width/2
            x2_mirror = -(l2[i+1][1]+sep) * self.scale_y + self.canvas_width/2
            self.canvas.create_line(x1, y1, x2, y2, fill=s)
            self.canvas.create_line(x1_mirror, y1, x2_mirror, y2, fill=s)
            if i == 0:
                x0, y0, x0_mirror = x1, y1, x1_mirror
        self.canvas.create_line(x0, y0, x2, y2, fill=s)  # Root Chord
        self.canvas.create_line(x0_mirror, y0, x2_mirror, y2, fill=s)  # Root Chord
        # Draws an horizontal line to "simulate" the cut body
        if attached == "False" and separate == "False":
            x1 = l2[0][1]*self.scale_y + self.canvas_width/2
            y1 = l2[0][0]*self.scale_y + self.centering
            x2 = -l2[0][1]*self.scale_y + self.canvas_width/2
            y2 = l2[0][0]*self.scale_y + self.centering
            self.canvas.create_line(x1, y1, x2, y2)
        # Draws the vertical line that connects the root chord of
        # the fin, (usually the body takes care of it, but in
        # this case, the fin is separated)
        if separate == "True":
            x1 = (l2[0][1]+sep) * self.scale_y + self.canvas_width/2
            y1 = l2[0][0]*self.scale_y + self.centering
            x2 = (l2[3][1]+sep) * self.scale_y + self.canvas_width/2
            y2 = l2[3][0]*self.scale_y + self.centering
            x1_m = -(l2[0][1]+sep) * self.scale_y + self.canvas_width/2
            y1_m = l2[0][0]*self.scale_y + self.centering
            x2_m = -(l2[0][1]+sep) * self.scale_y + self.canvas_width/2
            y2_m = l2[3][0]*self.scale_y + self.centering
            self.canvas.create_line(x1, y1, x2, y2, fill=s)
            self.canvas.create_line(x1_m, y1_m, x2_m, y2_m, fill=s)

    def populate(self, l0):
        # Populates the entries and more importantly, the points[i]
        # the savefile separates the body from the sabilization fins
        # with "Fins_s", and these from the control ones with "Fins_c"
        l = copy.deepcopy(l0)[:(len(self.checkbox) + len(self.combobox))]
        l1 = copy.deepcopy(l0)[(len(self.checkbox)):]
        l2 = []
        l3 = []
        l4 = []
        flag = "Body"
        for i, element in enumerate(l1):
            if element == "Fins_s" and i > 0:
                flag = "Fins_s"
                continue
            if element == "Fins_c":
                flag = "Fins_c"
                continue
            if flag == "Body":
                l2.append(element)
                continue
            if flag == "Fins_s":
                l3.append(element)
            if flag == "Fins_c":
                l4.append(element)
        # Populates the widgets, not the variables
        super().populate((l+l3))
        # Updates the points of the components
        self.combobox[0]["values"] = l2
        self.param_fin[0] = copy.deepcopy(l3)
        self.param_fin[1] = copy.deepcopy(l4)
        self.points[0] = copy.deepcopy(l2)
        self.rocket._update_rocket_dim(self.get_points_float(0))
        self.points[1] = copy.deepcopy(self.param_2_points_fins(l3))
        self.points[2] = copy.deepcopy(self.param_2_points_fins(l4))
        self.prev_total_errors = 0  # prevents showing the "all errors corrected" when opening a file without errors after opening one that had
        self.draw_rocket()
        self.change_state_fins()

    def get_configuration(self):
        # Takes the whole configurations and dumps it
        # into a list, must include the separators
        # between fins
        d = []
        d0 = self.get_points(0)
        d1 = self.get_param_fin(0)
        d2 = self.get_param_fin(1)
        for i in range(len(self.checkbox)):
            d.append(self.checkbox_status[i].get())
        d += d0
        d.append("Fins_s")
        d += d1
        d.append("Fins_c")
        d += d2
        return copy.deepcopy(d)

    def get_configuration_destringed(self):
        # Format [che,ck,box, [body], [fin_s], [fin_c]]
        d = []
        d0 = self.get_points_float(0)
        d1 = self.get_param_fin_float(0)
        d2 = self.get_param_fin_float(1)
        for i in range(len(self.checkbox)):
            if self.checkbox_status[i].get() == "True":
                d.append(True)
            else:
                d.append(False)
        d.append(d0)
        d.append(d1)
        d.append(d2)
        return copy.deepcopy(d)

    def activate_all(self):
        for i in range(len(self.checkbox)-1):
            self.checkbox[i+1].config(state="normal")
        for i in range(len(self.names_combobox)):
            self.combobox[i].config(state="normal")
        for i in range(len(self.entry)):
            self.entry[i].config(state="normal")

    def deactivate_all(self):
        for i in range(len(self.checkbox)-2):
            self.checkbox[i+1+1].config(state="disable")
        for i in range(len(self.entry)):
            self.entry[i].config(state="disable")

    def change_state_fins(self):
        """
        Activate the fins if they were deactivated and vise versa.

        Returns
        -------
        None.
        """
        if self.checkbox_status[1].get() == "True":
            self.activate_all()
        else:
            self.deactivate_all()
        self.draw_rocket()

    def change_state_control_fins(self):
        a = self.scale_act_angle.get()
        if self.checkbox_status[3].get() == "True":
            self.aoa_ctrl_fin = float(a)/57.295
            self.tvc_angle = 0
        else:
            self.tvc_angle = float(a)/57.295
            self.aoa_ctrl_fin = 0
        self.scale_act_angle.set(float(a))
        self.draw_rocket()

    def create_sliders(self):
        def slider_aoa(a):
            # Changes the aoa and re draws the CP
            if float(a) < 1:
                self.aoa = float(a)*DEG2RAD + 0.000001
            else:
                self.aoa = float(a)*DEG2RAD - 0.0000001
            self._draw_points()

        self.aoa_scale = tk.Scale(self.tab, from_=0, to=90,
                                  orient=tk.HORIZONTAL,
                                  command=slider_aoa,
                                  length=220,
                                  resolution=0.5)
        self.aoa_scale.grid(row=20, column=0)
        tk.Label(self.tab, text="Angle of Attack" + u' [\xb0]'
                 ).grid(row=21, column=0)

        def slider_actuator_angle(a):
            if self.checkbox_status[3].get() == "True":
                self.aoa_ctrl_fin = float(a)/57.295
                self.tvc_angle = 0
            else:
                self.tvc_angle = float(a)/57.295
                self.aoa_ctrl_fin = 0
            if float(gui_setup.param_file_tab.entry[8].get()) == 0:
                self.tvc_angle = 0
                self.aoa_ctrl_fin = 0
            self._draw_points()

        self.scale_act_angle = tk.Scale(self.tab, from_=-45, to=45,
                                        orient=tk.HORIZONTAL,
                                        command=slider_actuator_angle,
                                        length=150)
        self.scale_act_angle.grid(row=20, column=1)
        tk.Label(self.tab, text="Actuator Deflection" + u' [\xb0]'
                 ).grid(row=21, column=1)

        def slider_velocity(a):
            self.velocity = float(a)
            self._draw_points()

        self.scale_velocity = tk.Scale(self.tab, from_=1, to=100,
                                       orient=tk.HORIZONTAL,
                                       command=slider_velocity,
                                       length=150)
        self.scale_velocity.set(10)
        self.scale_velocity.grid(row=20, column=3)
        tk.Label(self.tab, text="Speed [m/s]").grid(row=21, column=3)

        def slider_time(a):
            self.flight_time = float(a)
            self._update_scale_limits()
            self._draw_points()

        self.scale_time = tk.Scale(self.tab, from_=0.01, to=15,
                                   orient=tk.HORIZONTAL,
                                   command=slider_time,
                                   length=150,
                                   resolution=0.01)
        self.scale_time.set(0.01)
        self.scale_time.grid(row=18, column=3)
        tk.Label(self.tab, text="Time [s]").grid(row=19, column=3)

    def param_2_points_fins(self, s):
        p = [[0, 0]]*4
        p_string = [[0, 0]]*4
        wingspan = float(s[2])
        position = float(s[0].split(",")[0])
        chord = float(s[0].split(",")[1])
        radius = self.rocket.diam_interp(position) / 2
        p[0] = [position, radius]
        p[3] = [position+chord, radius]
        position = float(s[1].split(",")[0])
        chord = float(s[1].split(",")[1])
        pos_root = p[0][0]
        position += pos_root
        radius += wingspan
        p[1] = [position, radius]
        p[2] = [position+chord, radius]
        for i in range(4):
            p_string[i] = str(p[i][0]) + "," + str(p[i][1])
        return p_string
