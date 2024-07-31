# CTHUB

The Clean Transportation Data Hub provides an evidence base for the Clean Transportation Branch through data storage, analysis and visualization, that improves decision making to increase energy efficiency and de-carbonise the transportation system. It aims to be the most comprehensive, reliable and accessible data management system for clean transportation in the world.

# Docker Instructions

- Make sure Docker is installed and running
- In your terminal, go to your project folder and execute the following:
  - `docker-compose up`

## Useful Docker Commands

- To access postgres:

  - Go to your project folder in your terminal
  - Execute the following:
    - `docker-compose exec db psql -U postgres`
    - Some notes about the structure of the command
      - docker-compose exec - this is your standard command to execute something within the context of the docker-compose yml file
      - db - this is the service you want to execute your command in
      - psql -U postgres - execute psql with a the default user of postgres

- To access the backend: (to do migrations and other stuff with the backend)

  - Go to your project folder in your terminal
  - Execute the following:
    - `docker-compose exec api bash`
    - Here you can do your standard django stuff like:
      - `python manage.py makemigrations`
      - `python manage.py migrate`

- To access the frontend: (to install/update a package, etc)

  - Go to your project folder in your terminal
  - Execute the following:

    - `docker-compose exec web bash`
    - This is where you can make changes to your package.json
    - You can technically make changes to your packages without going into your container, but you'll need npm installed into your system

  - To run in testing mode
    if you don't have docker-compose-local-dev.yml locally, create a new file and
    add the contents from docker-compose plus a line for: - KEYCLOAK_TESTING=True
    in api environment

  to run using this docker file:
  docker-compose -f docker-compose-local-dev.yml up

  this ensures that the authentication skips the actual keycloak authentication
  and uses the user table to get permissions

# Rebasing Guide

- To rebase your branch onto the latest release branch:
- `git fetch upstream`
- `git checkout your_branch`
- `git rebase --onto A B`
- Where `upstream` is the remote containing the release branch, and `A` is the hash of the latest commit to the release branch, and `B` is the hash of the commit in `your_branch` such that every commit after `B` ought to be rebased onto the release branch.
- If you run into conflicts while rebasing, you can resolve them in your IDE, and `git add` the resolved changes before finishing the rebase (committing).
- The rebased commits will have different hashes than the old ones, so if you previously pushed `your_branch` to a remote you will have to `git push --force` in order not to end up with additional commits in your remote branch.
- On Github, you can modify the base branch of a PR if you're rebasing from a branch based on a previous release branch to the latest release branch.

# Metabase

- Locally, create a database to store metabase's internals, and use/modify `metabase.env`, django's `settings.DATABASES` and `settings.DATABASE_ROUTERS` to point to said database.
- You can create django data migrations to insert your custom queries into the metabase application database.
- To create a data migration within the metabase django app:
- `python manage.py makemigrations --empty metabase`
- Then, using `RunPython` and django's `QuerySet` API, you may read/insert/update/delete data from metabase's application database.
- For custom queries, the internal metabase table of interest would probably be `report_card` (the associated model is `ReportCard`).
- To make your `RunPython` "script" cleaner, consider putting the actual queries themselves in separate sql files and reading from those in `RunPython`
- To uncouple metabase from django, simply remove metabase from `settings.INSTALLED_APPS`.

# Updating packages

- From time to time, we may become aware of package updates (mainly the packages in package.json (frontend) and requirements.py (backend)).
- Tools like Dependabot (https://github.com/dependabot) may raise PRs that update these packages.
- If the package that can be updated is a npm package and is a transitive dependency (a dependency of an immediate dependency), we can implement the update using `overrides` (https://docs.npmjs.com/cli/v10/configuring-npm/package-json#overrides).
- When packages get updated, we'll have to confirm that things are still working; ideally, we would have test suites with good coverage that we can run. Otherwise, or in addition to that, some user testing may be needed.
- When an entire image is scanned by some tool, there may be deeper, OS level dependencies that show as being critically out of date/vulnerable; in cases like this, if an updated image is not yet available, there are usually `alpine` versions of images that simply don't include many of these dependencies; whether they will work for our purposes is another question.

# License

The code is a fork from Richard's personal project. Please do not clone, copy or replicate this project unless you're authorized to do so.

# List of Dev Work | What to do before bringing in a new ticket into a Sprint

This is a list that was created on 2023-02-01 with all Zelda Devs to provide alternative work instead of bringing in a new ticket.

\*_Team Rule_ Do not bring in ticket After Friday

1. Help another Dev - see if other Devs need help to finish their ticket

2. PR Reviews – linked to the task above

3. Writing additional tests – for both tront and back end

4. Take a look at Tech Debt tickets - If we bring in tickets let's bring in Tech Debt first

5. Learning time:

- Take the opportunity to familiarize yourself with business logic, tech (anything around work we do)

- New learning and applying it to our work

- Innovation work
