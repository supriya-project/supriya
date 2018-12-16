import os
import pathlib
import subprocess
import tempfile

import uqbar.io

from supriya.system.SupriyaObject import SupriyaObject


class SuperColliderSynthDef(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = "SynthDef Internals"

    __slots__ = ("_body", "_name", "_rates")

    ### INITIALIZER ###

    def __init__(self, name, body, rates=None):
        self._name = name
        self._body = body
        self._rates = rates

    ### PRIVATE METHODS ###

    def _build_sc_input(self, directory_path):
        input_ = []
        input_.append("(")
        input_.append("a = SynthDef(")
        input_.append("    \\{}, {{".format(self.name))
        for line in self.body.splitlines():
            input_.append("    " + line)
        if self.rates:
            input_.append("}}, {});".format(list(self.rates)))
        else:
            input_.append("});")
        input_.append('"Defined SynthDef".postln;')
        input_.append('a.writeDefFile("{}");'.format(directory_path))
        input_.append('"Wrote SynthDef".postln;')
        input_.append("0.exit;")
        input_.append(")")
        input_ = "\n".join(input_)
        return input_

    ### PUBLIC METHODS ###

    def compile(self):
        sclang_candidates = uqbar.io.find_executable("sclang")
        if not sclang_candidates:
            raise RuntimeError("Cannot find sclang")
        sclang_path = sclang_candidates[0]
        prefix = None
        if os.environ.get("CI") == "true":
            prefix = str(pathlib.Path.home()) + os.path.sep
        with tempfile.TemporaryDirectory(prefix=prefix) as directory:
            directory_path = pathlib.Path(directory)
            sc_input = self._build_sc_input(directory_path)
            print(sc_input)
            sc_file_name = "{}.sc".format(self.name)
            sc_file_path = directory_path / sc_file_name
            synthdef_file_name = "{}.scsyndef".format(self.name)
            synthdef_file_path = directory_path / synthdef_file_name
            with sc_file_path.open("w") as file_pointer:
                file_pointer.write(sc_input)
            command = " ".join([str(sclang_path), "-D", str(sc_file_path)])
            subprocess.run(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            with synthdef_file_path.open("rb") as file_pointer:
                result = file_pointer.read()
        return bytes(result)

    ### PUBLIC PROPERTIES ###

    @property
    def body(self):
        return self._body

    @property
    def rates(self):
        return self._rates

    @property
    def name(self):
        return self._name
