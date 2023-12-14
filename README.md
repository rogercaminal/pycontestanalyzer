<!-- <img src="docs/images/ALMO_overlord.png"
  height="200"
  style="display:block;margin-left:auto;margin-right:auto;"
/> -->

# pycontestanalyzer

Quick analysis of hamradio contests


## Requirements

The requirements to run the code on this repository are the following:

- [GNU Make](https://www.gnu.org/software/make/) to run the project's recipes and
  commands.
- [Docker](https://www.docker.com/) to build/pull the project's image.
- (Recommended) [Pyenv](https://github.com/pyenv/pyenv) and
  [Pyenv Virtualenv](https://github.com/pyenv/pyenv-virtualenv) to handle Python
  versions and provide a virtual environment for the project
  (`pyenv virtualenv 3.10.8 env-pycontestanalyzer && pyenv shell env-pycontestanalyzer`)

## Development setup

In order to set up the repository for development, one can use the following Makefile
recipe:

```shell
make local-setup
```

On a first run, this will create an `.env` file, based on [.env.example](.env.example)
containing environment variables we can use in our IDE/editor or when running the code
locally; install the necessary project dependencies as well as development dependencies
(formatting, linting, testing); and install the pre-commit hooks (formatting and
linting) to standarise code before commiting it to the repository.

Alternatively, one can set up the project locally directly creating a new virtual
environment by running the recipe:

```shell
make local-setup-with-venv
```

This rule will create it for you in the current directory and all you'll have to do is
to activate it.

To load the environment variables from the `.env` file, you can

```python
from dotenv import load_dotenv
load_dotenv()
```

### Code style

In order to maintain a cohesive code style throughout the application, which encourages
clean code practices, the repository includes a set of pre-commit hooks and format/lint
make commands to check and fix styling options. Just run:

```shell
pre-commit run --all
make format
make lint
```

### PyContestAnalyzer package documentation

To find more detail documentation on the PyContestAnalyzer package, you can take a look at the
[source code](pycontestanalyzer/) or check the [docs](docs/README.md).

## Usage

One can run the code in an interactive containerised shell, by running:

```shell
make run-sh
```

This will open an interactive shell where we can run the application. You can see the
differnet command arguments and options by running:

```shell
python pycontestanalyzer --help
```

Alternatively, you can directly install the dependencies and run the commands locally,
with:

```shell
make install
python pycontestanalyzer --help
```

## Repository commands

Use the recipe `make help` to list the available commands with their description.

## Contributing

When contributing to the repository, it is encouraged to follow a set of guidelines.

### Branches, commits and pull requests

In first place, when creating a new branch consider using the following branch name
structure:

```text
{branch_type}/{short_descriptive_name}
```

Where `branch_type` can be one of:

- Features, new functionality or additive content -> `feature`.
- Fixes or corrections to the code or logic -> `fix`.
- Hotfixes or corrections directly over the main branch -> `hotfix`.
- Refactor for reorganization or improvements on existing code -> `refactor`.
- Releases of a group of changes from development to main branch -> `release`.

On the other hand, when creating and pushing commits to ones branch, consider using
the [conventional commits convention](https://www.conventionalcommits.org/en/v1.0.0/).
Body and footer for the commit are usually not needed, except when squashing commits
when the body should contain the commit messages of the squashed commits for
convenience.

The moment you are finished with the changes in your branch, consider creating a Pull
Request so that it can be reviewed. Consider following the PR template for the body and
using the following naming structure for ones PR's title:

```text
[ticket_reference] {Short Descriptive title}
```

Once approved, the recommended way to merge the changes to the development branch is via
the `Squash & merge` option, keeping in the squashed commit title's the PR title with
the ticket reference.

### Releases

Releases are scheduled manually when the changes to the development branch are stable,
tested and validated by the team.

The release process is performed using Git Flow release strategy. One can perform it by
using the git-flow command line utility
[here](https://danielkummer.github.io/git-flow-cheatsheet/#setup) or through the
equivalent regular git commands
[here](https://gist.github.com/JamesMGreene/cdd0ac49f90c987e45ac).
