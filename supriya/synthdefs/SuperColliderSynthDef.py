import os
import shutil
import subprocess
import tempfile
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SuperColliderSynthDef(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_body',
        '_name',
        '_rates',
        )

    ### INITIALIZER ###

    def __init__(self, name, body, rates=None):
        self._name = name
        self._body = body
        self._rates = rates

    ### PUBLIC METHODS ###

    def compile(self):
        directory_path = tempfile.mkdtemp()
        input_ = []
        input_.append('(')
        input_.append('a = SynthDef(')
        input_.append(r'    \{}, {{'.format(self.name))
        for line in self.body.splitlines():
            input_.append('    ' + line)
        if self.rates:
            input_.append('}}, {});'.format(list(self.rates)))
        else:
            input_.append('});')
        input_.append('a.writeDefFile("{}");'.format(directory_path))
        input_.append('0.exit;')
        input_.append(')')
        input_ = '\n'.join(input_)
        sc_file_name = '{}.sc'.format(self.name)
        sc_file_path = os.path.join(directory_path, sc_file_name)
        synthdef_file_name = '{}.scsyndef'.format(self.name)
        synthdef_file_path = os.path.join(directory_path, synthdef_file_name)
        with open(sc_file_path, 'w') as f:
            f.write(input_)
        command = ['sclang', sc_file_path]
        subprocess.call(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        with open(synthdef_file_path, 'rb') as f:
            result = f.read()
        shutil.rmtree(directory_path)
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
