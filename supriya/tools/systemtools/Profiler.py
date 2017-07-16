import cProfile
import io
import pstats
import subprocess


class Profiler:

    def __enter__(self):
        self._profiler = cProfile.Profile()
        self._profiler.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self._profiler.disable()
        stream = io.StringIO()
        profiler_stats = pstats.Stats(self._profiler, stream=stream)
        profiler_stats = profiler_stats.sort_stats('cumulative')
        profiler_stats.print_stats()
        print(stream.getvalue())
        profiler_stats.dump_stats('stats.profile')
        gprof2dot_command = 'gprof2dot -f pstats -o stats.dot stats.profile'
        exit_code = subprocess.call(gprof2dot_command)
        if exit_code:
            return
        dot_command = 'dot -Tpdf -ostats.pdf'
        exit_code = subprocess.call(dot_command)
        if exit_code:
            return
        subprocess.call('open stats.pdf')
