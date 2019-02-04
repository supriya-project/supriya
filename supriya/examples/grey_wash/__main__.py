from supriya import play
from . import composite, project_settings

if __name__ == "__main__":
    play(
        composite.session,
        memory_size=project_settings["server_options"]["memory_size"],
        print_transcript=True,
    )
