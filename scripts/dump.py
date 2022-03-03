import sys
import dump_tools

if __name__ == "__main__":

    version = sys.argv[-1]
    if "v" not in version:
        # If no version supplied, use default.
        version = "15.1v1"
    # Dump the modo version.
    dump_tools.dump(version)
