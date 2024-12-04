# Character Sheet Web App

This web application allows users to create and manage character sheets for any RPG.

## Features

- Create new characters with default attributes and skills.
- Edit character details, attributes, skills, talents, armor, weapons, spells, and trappings.
- View character sheets in a structured format.

## Serving The Application Locally

**Windows**:

First install the project with the following command:

```{code}
uv add path/to/clone/character-creator
```

or

```{code}
pip install path/to/clone/character-creator
```

Then serve the app with waitress which should be installed with the project

```{code}
waitress-serve --host 127.0.0.1 src:app
```
