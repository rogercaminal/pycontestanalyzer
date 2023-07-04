# PyContestAnalyzer Settings

This page explains PyContestAnalyzer settings management strategy.

General and environment specific settings for the application are stored inside the
[settings](../../settings/) directory, in YAML files for the different settings of the
app. These are loaded into the application using the
[Dynaconf](https://www.dynaconf.com/) Python package, which allows for layered
environment, formatting and dynamic variables, among other goodies. In order to have
statically typed settings, the Dynaconf settings object is used to initialize a
[Pydantic](https://docs.pydantic.dev/) model.

These settings can be easily loaded into the code through the configuration module:

```python
from pycontestanalyzer.config import get_settings
# ... inside the application code
settings = get_settings()
```

## Settings files

This section defines a regular setting file.
For further reference, see
[Dynaconf's documentation](https://www.dynaconf.com/settings_files/).

```yaml
# Default environment key is used as base for all environments
default:
    # The top-level key after the environment key must coincide with the AlmoSettings
    # class field, with the appriate AlmoBaseSettings subclass
    setting_name:
        a_sting: foo
        a_number: 1.0
        a_bool: true
        a_list:
            - One
            - Two
        a_dict:
            key: value
        format_env: "@jinja One can use {{env['ENVIRONMENT_VARIABLE']}}"
        format_this: "@jinja Or other settings -> {{this.setting_name.a_number}}"
        expressions: "@jinja Or expressions {{env['ENVIRONMENT_VARIABLE'] or 0}}"

# By specifying other environment keys, we can merge/override settings
# More details on merging in https://www.dynaconf.com/merging/
testing:
    settings:
        # We can merge keys on top-level settings
        new_setting: 1
        dynaconf_merge: true
    # We can use dunder merging to target deep nested environments overrides
    settings_name__a_dict__key: new_value
```

## Credentials and secrets

Settings which contain credentials or secrets are passed by using environment variables,
such as the following:

```yaml
default:
  redshift:
    connection:
      database: "@jinja {{env['POSTGRES_DB_NAME']}}"
      host: "@jinja {{env['POSTGRES_HOST']}}"
      password: "@jinja {{env['POSTGRES_PASSWORD']}}"
      port: "@jinja {{env['POSTGRES_PORT']}}"
      username: "@jinja {{env['POSTGRES_USER']}}"
```

The values of these variables will be loaded from the [.env](../../.env) file locally,
and injected into the Docker image on beta/prod execution.

> Note the environment variable's values **MUST NOT** be enclosed in either single or
> double quotes, neither they should contain escaped characters (e.g. newline `\n`).

## Adding new settings

When adding a new setting to a part of the ALMO package, there can be to scenarios:

1. The setting is included in one of the existing setting files in
    [settings](../../settings/) directory.
2. A new setting file needs to be created and setup.

In the first case, one only has to add the setting to the appropriate YAML file and
update the appropiate settings model in [almo.config](../../almo/config).

In the second case, after creating the new YAML file one has to create a new setting
Pydantic model, in a new file in `almo.config`. Next, one needs to add the settings to
the general `AlmoSettings` model in
[almo.config.settings](../../almo/config/settings.py), by creating a new field with the
type corresponding to the previously created model.

## Setting documentation

Specific per-settings file documentation can be found in the following files:

- [Download settings](./download.md)
