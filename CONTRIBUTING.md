# Contributing to Langflow

Hello there! We appreciate your interest in contributing to Langflow.
As an open-source project in a rapidly developing field, we are extremely open
to contributions, whether it be in the form of a new feature, improved infra, or better documentation.

To contribute to this project, please follow a ["fork and pull request"](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow.
Please do not try to push directly to this repo unless you are a maintainer.

The branch structure is as follows:

- `main`: The stable version of Langflow
- `dev`: The development version of Langflow. This branch is used to test new features before they are merged into `main` and, as such, may be unstable.

## 🗺️Contributing Guidelines

## 🚩GitHub Issues

Our [issues](https://github.com/logspace-ai/langflow/issues) page is kept up to date
with bugs, improvements, and feature requests. There is a taxonomy of labels to help
with sorting and discovery of issues of interest.

If you're looking for help with your code, consider posting a question on the
[GitHub Discussions board](https://github.com/logspace-ai/langflow/discussions). Please
understand that we won't be able to provide individual support via email. We
also believe that help is much more valuable if it's **shared publicly**,
so that more people can benefit from it.

- **Describing your issue:** Try to provide as many details as possible. What
  exactly goes wrong? _How_ is it failing? Is there an error?
  "XY doesn't work" usually isn't that helpful for tracking down problems. Always
  remember to include the code you ran and if possible, extract only the relevant
  parts and don't just dump your entire script. This will make it easier for us to
  reproduce the error.

- **Sharing long blocks of code or logs:** If you need to include long code,
  logs or tracebacks, you can wrap them in `<details>` and `</details>`. This
  [collapses the content](https://developer.mozilla.org/en/docs/Web/HTML/Element/details)
  so it only becomes visible on click, making the issue easier to read and follow.

## Issue labels

[See this page](https://github.com/logspace-ai/langflow/labels) for an overview of
the system we use to tag our issues and pull requests.

## Local development

You can develop Langflow using docker compose, or locally.

We provide a .vscode/launch.json file for debugging the backend in VSCode, which is a lot faster than using docker compose.

Setting up hooks:

```bash
make init
```

This will install the pre-commit hooks, which will run `make format` on every commit.

It is advised to run `make lint` before pushing to the repository.

## Run locally

Langflow can run locally by cloning the repository and installing the dependencies. We recommend using a virtual environment to isolate the dependencies from your system.

Before you start, make sure you have the following installed:

- Poetry (>=1.4)
- Node.js

Then, in the root folder, install the dependencies and start the development server for the backend:

```bash
make backend
```

And the frontend:

```bash
make frontend
```

## Docker compose

The following snippet will run the backend and frontend in separate containers. The frontend will be available at `localhost:3000` and the backend at `localhost:7860`.

```bash
docker compose up --build
# or
make dev build=1
```

## Documentation

The documentation is built using [Docusaurus](https://docusaurus.io/). To run the documentation locally, run the following commands:

```bash
cd docs
npm install
npm run start
```

The documentation will be available at `localhost:3000` and all the files are located in the `docs/docs` folder.
Once you are done with your changes, you can create a Pull Request to the `main` branch.
