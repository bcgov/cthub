# CTHUB
The Clean Transportation Data Hub provides an evidence base for the Clean Transportation Branch through data storage, analysis and visualization, that improves decision making to increase energy efficiency and de-carbonise the transportation system. It aims to be the most comprehensive, reliable and accessible data management system for clean transportation in the world.

# Docker Instructions
- Make sure Docker is installed and running
- In your terminal, go to your project folder and execute the following: 
  - ```docker-compose up```
- You'll have to make an edit to your host file
  - Mac Users
    - Edit ```/private/etc/hosts```
    - Add this line:
      - ```127.0.0.1 keycloak```
  - Windows Users
    - Edit ```c:\windows\system32\drivers\etc\hosts```
    - Add this line:
      - ```127.0.0.1 keycloak```
- Navigate to ```http://localhost:3000/```
- Login with:
  - username: ```user```
  - password: ```1234```

## Useful Docker Commands
- To access keycloak:
  - Navigate to ```http://localhost:8080/```
    - username: ```admin```
    - password: ```admin```

- To access postgres:
  - Go to your project folder in your terminal
  - Execute the following:
    - ```docker-compose exec db psql -U postgres```
    - Some notes about the structure of the command
      - docker-compose exec - this is your standard command to execute something within the context of the docker-compose yml file
      - db - this is the service you want to execute your command in
      - psql -U postgres - execute psql with a the default user of postgres

- To access the backend: (to do migrations and other stuff with the backend)
  - Go to your project folder in your terminal
  - Execute the following:
    - ```docker-compose exec api bash```
    - Here you can do your standard django stuff like:
      - ```python manage.py makemigrations```
      - ```python manage.py migrate```

- To access the frontend: (to install/update a package, etc)
  - Go to your project folder in your terminal
  - Execute the following:
    - ```docker-compose exec web bash```
    - This is where you can make changes to your package.json
    - You can technically make changes to your packages without going into your container, but you'll need npm installed into your system

# License
The code is a fork from Richard's personal project. Please do not clone, copy or replicate this project unless you're authorized to do so.


# List of Dev Work | What to do before bringing in a new ticket into a Sprint

This is a list that was created on 2023-02-01 with all Zelda Devs to provide alternative work instead of bringing in a new ticket.  

**Team Rule* Do not bring in ticket After Friday 

1. Help another Dev - see if other Devs need help to finish their ticket 

2. PR Reviews – linked to the task above 

3. Writing additional tests – for both tront and back end 

4. Take a look at Tech Debt tickets - If we bring in tickets let's bring in Tech Debt first 

5. Learning time: 

- Take the opportunity to familiarize yourself with business logic, tech (anything around work we do) 

- New learning and applying it to our work 

- Innovation work 
