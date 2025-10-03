import os
import runpy


def main() -> None:
    project_root = os.path.dirname(__file__)
    target = os.path.join(project_root, "Jarvis", "jarvis.py")
    if not os.path.isfile(target):
        raise FileNotFoundError(f"Cannot find target script at: {target}")
    runpy.run_path(target, run_name="__main__")


if __name__ == "__main__":
    main()


