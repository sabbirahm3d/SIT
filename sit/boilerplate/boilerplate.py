#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implementation of the base class of BoilerPlate. This class generates the boilerplate code
required to build the black box interface in SST Interoperability Toolkit.

This class is purely virtual and therefore requires a child class to inherit and implement its
protected methods. The child class must implement the following protected methods:
- _get_driver_inputs()
- _get_driver_outputs()
- _get_driver_defs()

The following public methods are inherited by the child classes and are not to be overridden:
- set_ports(ports)
- generate_bbox()
- fixed_width_float_output(precision)
- disable_runtime_warnings(warnings)
"""

import math
import os

from .exceptions import *


class BoilerPlate(object):

    def __init__(self, ipc, module, lib, width_macros=None, module_dir="", lib_dir="", desc="",
                 driver_template_path="", component_template_path=""):
        """Constructor for the virtual base class BoilerPlate

        Initialize all member port variables and component variables. Only the following methods
        are public:
        `set_ports(ports)`
        `generate_bbox()`

        Parameters:
        -----------
        ipc : str (options: "sock", "zmq")
            method of IPC
        module : str
            SST element component and HDL module name
        lib : str
            SST element library name
        width_macros : dict(str:[str|int]) (default: dict(None:None))
            mapping of signal width macros to their integer values. An HDL module may declare
            constants or user-inputted variables in their implementation to determine signal widths.
            The module can only know the values of those macros by utilizing this parameter.
            Example:
            `width_macros = {
                "ADDRESS_WIDTH": 16,
                "DATA_WIDTH": 16,
            }`
        module_dir : str (default: "")
            directory of HDL module
        lib_dir : str (default: "")
            directory of SIT library
        desc : str (default: "")
            description of the SST model
        driver_template_path : str (default: "")
            path to the black box-driver boilerplate
        component_template_path : str (default: "")
            path to the black box-model boilerplate

        Raises:
        -------
        IPCException
            unsupported IPC is provided
        """
        if ipc in ("sock", "zmq"):
            self.ipc = ipc
        else:
            raise IPCException(f"{ipc} is not a supported IPC protocol")

        self.module = module
        self.lib = lib
        self.module_dir = module_dir
        self.lib_dir = lib_dir
        self.desc = desc
        self.precision = 0
        self.extra_libs = ""
        self.disable_warning = ""

        self.hdl_str = self.__class__.__name__.lower()
        self.template_path = os.path.join(os.path.dirname(__file__), "template", self.hdl_str)
        self.driver_template_path = driver_template_path if driver_template_path else os.path.join(
            self.template_path, "driver")
        self.component_template_path = component_template_path if component_template_path else os.path.join(
            self.template_path, "comp")

        self.width_macros = width_macros if width_macros else {}
        self.ports = {
            "clock": [],
            "input": [],
            "output": [],
            "inout": []
        }
        self.bbox_dir = "blackboxes"
        self.driver_path = self.comp_path = os.path.join(self.bbox_dir, self.module)

        self.driver_buf_size = 0
        self.comp_buf_size = 0
        if self.ipc == "sock":

            # component attributes
            self.sig_type = "SocketSignal"

        elif self.ipc == "zmq":

            # component attributes
            self.sig_type = "ZMQSignal"

        # shared attributes
        self.sender = self.receiver = "m_signal_io"

    @staticmethod
    def _sig_fmt(fmt, split_func, array, delim=";\n    "):
        """Format lists of signals based on fixed arguments

        Parameters:
        -----------
        fmt : str
            string format
        split_func : lambda or dict(str:str)
            map to split on the signals
        array : list(str)
            list of signals
        delim : str (default: ";n    ")
            delimiter

        Returns:
        --------
        str
            string formatted signals
        """
        return delim.join(fmt.format(**split_func(i)) for i in array)

    def _get_signal_width_from_macro(self, signal_type):
        """Get width of a signal type mapped in width_macros

        Parameters:
        -----------
        signal_type : str
            signal type of port

        Raises:
        -------
        SignalFormatException
            signal width macro not found

        Returns:
        --------
        value : str|int
            width of signal type
        """
        for macro, value in self.width_macros.items():
            if macro in signal_type:
                return value

        raise SignalFormatException(f"Invalid macro in signal: {signal_type}") from None

    def _get_all_ports(self):
        """Flatten all types of ports into a single array

        Returns:
        --------
        generator
            all ports in a single array
        """
        return (i for sig in self.ports.values() for i in sig)

    def set_ports(self, ports):
        """Assign ports to their corresponding member lists

        Parameters:
        -----------
        ports : tuple(tuple3(str))
            type-declared signals in the form (<PORT TYPE>, <PORT NAME>, <DATA TYPE>).
            The current types of signals supported are ("clock", "input", "output", "inout")

        Raises:
        -------
        SignalFormatException
            invalid signal format provided
        PortException
            invalid port type provided
        """
        # PORT =  PORT_DATA_TYPE, PORT_NAME, PORT_TYPE, PORT_LENGTH
        for port in ports:
            if len(port) not in (3, 4):
                raise SignalFormatException("Invalid signal format") from None
            try:
                self.ports[port[0]].append({
                    "name": port[1],
                    "type": port[2],
                    "len": int(port[-1]) if len(port) == 4 else self._parse_signal_type(port[2])
                })
            except KeyError:
                raise PortException(f"{port[0]} is an invalid port type") from None

    def __get_comp_defs(self):
        """Map definitions for the component format string

        Returns:
        --------
        dict(str:str)
            format mapping of template component string
        """
        self.comp_buf_size = sum(output_port["len"] for output_port in self.ports["output"])
        if self.precision and self.precision > self.comp_buf_size - 2:
            print(f"Component buffer size increased from {self.comp_buf_size} to ", end="")
            self.comp_buf_size += self.precision - 2
            print(f"{self.comp_buf_size} to include specified precision")

        return {
            "lib_dir": self.lib_dir,
            "module": self.module,
            "lib": self.lib,
            "desc": self.desc,
            "ports": self._sig_fmt(
                """{{ "{link}", "{desc}", {{ "sst.Interfaces.StringEvent" }}}}""",
                lambda x: {
                    "link": self.module + x[0],
                    "desc": self.module + x[-1]
                },
                (("_din", " data in"), ("_dout", " data out")),
                ",\n" + " " * 8
            ),
            "sig_type": self.sig_type,
            "buf_size": self.comp_buf_size,
            "sender": self.sender,
            "receiver": self.receiver,
        }

    def __generate_comp_str(self):
        """Generate the black box-model code based on methods used to format
        the template file

        Raises:
        -------
        TemplateFileNotFound
            boilerplate template file not found

        Returns:
        --------
        str
            boilerplate code representing the black box-model file
        """
        if os.path.isfile(self.component_template_path):
            with open(self.component_template_path) as template:
                return template.read().format(
                    **self.__get_comp_defs()
                )

        raise TemplateFileNotFound(
            f"Component boilerplate template file: {self.component_template_path} not found")

    def __generate_driver_str(self):
        """Generate the black box-driver code based on methods used to format
        the template file

        Raises:
        -------
        TemplateFileNotFound
            boilerplate template file not found

        Returns:
        --------
        str
            boilerplate code representing the black box-driver file
        """
        if os.path.isfile(self.driver_template_path):
            with open(self.driver_template_path) as template:
                return template.read().format(
                    inputs=self._get_driver_inputs(),
                    outputs=self._get_driver_outputs(),
                    **self._get_driver_defs()
                )

        raise TemplateFileNotFound(
            f"Driver boilerplate template file: {self.driver_template_path} not found")

    def generate_bbox(self):
        """Provide a high-level interface to the user to generate both the components of the
        black box and dump them to their corresponding files

        Raises:
        -------
        PortException
            no ports were provided
        """
        print("------------------------------------------------------------")
        if not len(self.ports):
            raise PortException(
                "No ports were set. Make sure to call set_ports() before generating files.")

        if not os.path.exists(self.bbox_dir):
            os.makedirs(self.bbox_dir)

        with open(self.driver_path, "w") as driver_file:
            driver_file.write(self.__generate_driver_str())

        with open(self.comp_path, "w") as comp_file:
            comp_file.write(self.__generate_comp_str())

        try:
            self._generate_extra_files()
        except AttributeError:
            pass

        print(f"Ports generated for: {self.module} ({self.hdl_str})")
        for port_type in self.ports:
            if self.ports[port_type]:
                print(f"Port type: {port_type}")
                for port in self.ports[port_type]:
                    print(f""" \"{port['name']}\" -> {{{
                        "data type" if self.hdl_str == "systemc" else "integer width"
                    }: {port['type']}, length: {port['len']}}}""")
        print(f"Driver buffer size: {self.driver_buf_size}")
        print(f"Component buffer size: {self.comp_buf_size}")
        print("------------------------------------------------------------")

    def fixed_width_float_output(self, precision):
        """Generate additional methods to handle ports with float signals

        Parameters:
        -----------
        precision : int
            level of precision for float signals

        Raises:
        -------
        APIException
            method not supported
        """
        self.precision = precision
        print("Adding fixed precision for float outputs")
        try:
            self._fixed_width_float_output()
        except AttributeError:
            raise APIException(f"fixed_width_float_output() not supported with {self.module}")

    def disable_runtime_warnings(self, warnings):
        """Generate additional methods to disable driver runtime warnings

        Parameters:
        -----------
        warnings : str|list(str)
            runtime warning or list of runtime warnings to ignore

        Raises:
        -------
        APIException
            method not supported
        """
        if not isinstance(warnings, list):
            warnings = [warnings]
        for warning in warnings:
            try:
                self._disable_runtime_warnings(warning)
            except AttributeError:
                raise APIException(f"disable_runtime_warnings() not supported with {self.module}")

    @staticmethod
    def _get_ints(signal):
        """Extract integers from signal string

        Parameters:
        -----------
        signal : str
            signal data type or integer width

        Returns:
        --------
        int
            string of integer found in signal string
        """
        return int("".join(s for s in signal if s.isdigit()))

    @staticmethod
    def _get_num_digits(signal):
        """Compute the minimum number of digits required to hold signal data type width by
        calculating: `floor(log(-1 + 2^x)/log(10)) + 1`

        Parameters:
        -----------
        signal : str
            signal data type width

        Returns:
        --------
        int
            number of digits for signal width
        """
        return math.floor(math.log(math.pow(2, signal) - 1) / math.log(10)) + 1
