# storelift

1. Clone this repo
2. Create an empty conda env
3. Run 'conda env update' in the repo root.
4. Make sure ports 5000 and 3306 are not occupied in docker (also network name 'mynet')
5. Run 'docker pull mysql:5.7'
6. Run 'sh setup.sh'. It:
 - Starts a mysql container.
 - Builds flask app image.
 - Starts flask app container
 - Waits for db to be up and ready (20 sec)
 - Runs db setup script
 - Starts the cli app

7. CLI app sends HTTP requests to flask app (you can navigate to 'localhost:5000' to see it). Flask app then updates the state of the db according to the circumstances.

8. After closing the CLI, the script stops containers, deletes network etc.

PS. Tested on Mac. If you encounter any difficulties, please just run every command in 'setup.sh' by hand.

Example sequence:

create 1 1000
item 1 100
item 2 5.5
enter 1
take 1 1
take 1 1
take 1 2
exit 1
state
quit
