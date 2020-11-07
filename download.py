from pathlib import Path
import sys
import subprocess
import converter.util as util
script = util.PROJECT / "p5e-data-conversion" / "main.py"
output = util.CACHE

if __name__ == '__main__':
    if len(sys.argv) == 2:
        token = sys.argv[1]
        subprocess.run(["python", str(script), token, "--output", str(output), "--keep-dice", "--no-variants"])
    else:
        print("Please supply spread token")
