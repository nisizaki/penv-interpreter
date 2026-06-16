# Programmable Environment Calculus Interpreter

This repository contains a small Python interpreter for the programmable environment calculus `lambda_penv`.

The implementation is based mainly on the semantics in Section 2 of `docs/paper.md`. The main purpose of this repository is to make it easy to try the interpreter through the Jupyter Notebook:

```text
examples/demo01_commented.ipynb
```

## Directory structure

```text
penv-interpreter/
  docs/
    paper.md
  examples/
    demo.py
    demo01_commented.ipynb
  src/
    penv/
      __init__.py
      ast.py
      evaluator.py
      parser.py
      runtime.py
  tests/
    test_evaluator.py
    test_parser.py
  pyproject.toml
  README.md
```

## Requirements

The following environment is assumed.

```text
Python 3.10 or later
pip
Jupyter Notebook or JupyterLab
pytest
```

On Ubuntu or WSL2 Ubuntu, check Python and pip by running:

```bash
python3 --version
python3 -m pip --version
```

## Getting the files

If you use Git, clone this repository as follows.

```bash
git clone https://github.com/YOUR-GITHUB-USER/penv-interpreter.git
cd penv-interpreter
```

Replace `YOUR-GITHUB-USER` with the actual GitHub user name.

If you do not use Git, open the GitHub page in a browser and download the repository from:

```text
Code -> Download ZIP
```

Then unzip the file and move into the extracted directory.

## Setup

From the top directory of this repository, run:

```bash
python3 -m pip install -e .
```

This installs the local package in editable mode, so that Python can import the `penv` package from `src/penv`.

If Jupyter Notebook is not installed, install it by:

```bash
python3 -m pip install notebook
```

Alternatively, if you use JupyterLab, install it by:

```bash
python3 -m pip install jupyterlab
```

For running tests, install pytest if necessary:

```bash
python3 -m pip install pytest
```

## Check that the interpreter works

Run the test suite first.

```bash
python3 -m pytest -v
```

If the tests pass, run the simple demo script.

```bash
python3 examples/demo.py
```

## Running `demo01_commented.ipynb`

The main notebook is:

```text
examples/demo01_commented.ipynb
```

To open it with Jupyter Notebook, run:

```bash
jupyter notebook examples/demo01_commented.ipynb
```

To open it with JupyterLab, run:

```bash
jupyter lab
```

Then open the following file from the file browser:

```text
examples/demo01_commented.ipynb
```

## What the notebook does

The notebook demonstrates how to use the interpreter from Python.

It imports the AST definitions, evaluator, runtime values, and parser from the `penv` package.

Typical imports are:

```python
from penv.ast import *
import penv.evaluator as ev
import penv.parser as parser
```

The empty environment is created by:

```python
rho = ev.empty_env()
```

A basic example is:

```python
term = Comp(
    Var("x"),
    Ext(NameConst("M"), "x", Id())
)

ev.eval(term, rho)
```

This corresponds to the expression:

```text
x circ (("M" / x) . id)
```

The expected result is:

```text
NameValue(name='M')
```

The notebook also demonstrates the idea that an environment can be used as a function on names. For example:

```python
term = App(
    Ext(NameConst("value-of-x"), "x", Id()),
    NameConst("x")
)

ev.eval(term, rho)
```

This corresponds to:

```text
(("value-of-x" / x) . id) "x"
```

The expected result is:

```text
NameValue(name='value-of-x')
```

## Using the parser

The parser can be used through `parser.parse`.

For example:

```python
term = parser.parse('x circ (("M" / x) . id)')
ev.eval(term, rho)
```

This should return:

```text
NameValue(name='M')
```

Depending on the current parser implementation, some more complex expressions involving `if`, `then`, `else`, and equality may require parser fixes. The notebook includes examples and comments explaining the intended semantics.

## Mathematical background

The interpreter follows the Section 2 semantics of the programmable environment calculus.

The intended correspondence is:

```text
eval(Var(x), rho)       = lookup(rho, x)
eval(Lam(x, M), rho)    = closure capturing rho
eval(App(M, N), rho)    = apply(eval(M, rho), eval(N, rho))
eval(Id(), rho)         = rho
eval(Ext(M, x, N), rho) = update(eval(N, rho), x, eval(M, rho))
eval(Comp(M, N), rho)   = eval(M, eval(N, rho))
eval(NameConst(x), rho) = NameValue(x)
```

In mathematical notation, the important cases are:

```math
\llbracket x \rrbracket \rho = \mathrm{Lookup}\ \rho\ \llbracket x \rrbracket
```

```math
\llbracket (M/x).N \rrbracket \rho
=
\mathrm{Update}\ (\llbracket N \rrbracket \rho)\ \llbracket x \rrbracket\ (\llbracket M \rrbracket \rho)
```

```math
\llbracket M \circ N \rrbracket \rho
=
\llbracket M \rrbracket(\llbracket N \rrbracket \rho)
```

Thus, `id` represents the current environment, `(M/x).N` extends an environment, and `M circ N` evaluates `M` under the environment produced by `N`.

## Notes for WSL users

If you are using WSL2 Ubuntu and Jupyter prints a URL such as:

```text
http://localhost:8888/tree?token=...
```

open that URL in a Windows browser.

If import errors occur, run the following command again from the repository top directory:

```bash
python3 -m pip install -e .
```

You can also check whether the package is importable by:

```bash
python3 -c "import penv; print(penv)"
```

## How to add this README to GitHub

Place this file at the top of the project directory:

```bash
cd ~/prog/penv-interpreter
cp /path/to/README.md README.md
```

If the file was downloaded to Windows `Downloads`, the command may be:

```bash
cd ~/prog/penv-interpreter
cp /mnt/c/Users/nisiz/Downloads/README.md README.md
```

Check the file:

```bash
sed -n '1,240p' README.md
```

Add and commit it:

```bash
git status
git add README.md
git commit -m "Add README with notebook instructions"
```

Push it to GitHub:

```bash
git push
```

If the repository has not yet been created on GitHub, create a public repository and push it by:

```bash
gh repo create penv-interpreter --public --source=. --remote=origin --push
```

After pushing, open the GitHub page:

```bash
gh repo view --web
```

The README should be displayed on the top page of the repository.
