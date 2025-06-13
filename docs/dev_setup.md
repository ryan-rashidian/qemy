# Development Setup

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Optional - Setup Launch Script

- Recommended for convenience.

Step 1 - Set path to your venv in the bash script

In the scripts directory, find the qemy-dev bash script and open with a text editor:

```bash
#!/bin/bash

orig_dir=$(pwd)
source ~/path/to/qemyenv/bin/activate # make sure this matches your venv activate path
# Conda users: change above line to "conda activate qemyenv"
cd ~/path/to/projectroot/qemy # match with your project root directory
python -m qemy.cli_main
deactivate 
# Conda users: change above line to "conda deactivate"
cd "$orig_dir"
```

Step 2 - Turn qemy script into an executable

Also from scripts directory:

```bash
chmod +x qemy
```

Step 3 - Create Path in .bashrc

```bash
nano ~/.bashrc
```

Add the following to the bottom of your .bashrc. Replace "path/to/qemy/scripts" with your own: 

```bash
# PATH for Qemy
export PATH="$HOME/path/to/qemy/scripts:$PATH"

