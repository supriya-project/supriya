import os
import shutil
import subprocess
import tempfile


class SCSynthDef(object):

    ### INITIALIZER ###

    def __init__(self, name, code):
        self._name = name
        self._code = code

    ### PUBLIC METHODS ###

    def compile(self):
        directory_path = tempfile.mkdtemp()
        input_ = []
        input_.append('(')
        input_.append('a = SynthDef(')
        input_.append(r'    \{}, {{'.format(self.name))
        for line in self.code.splitlines():
            input_.append('    ' + line)
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
        command = 'sclang {}'.format(sc_file_path)
        subprocess.call(command, shell=True)
        with open(synthdef_file_path, 'r') as f:
            result = f.read()
        shutil.rmtree(directory_path)
        return bytearray(result)

    ### PUBLIC PROPERTIES ###

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name
