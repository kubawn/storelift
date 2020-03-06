# start mysql docker container
docker pull mysql
docker network create mynet
docker run --name store_db -e MYSQL_ROOT_PASSWORD=storelift -p 3306:3306 -d mysql:5.7
# build & start flask app container
docker build -t store_api .
docker run --name store_api -d -p 5000:5000 store_api:latest
# wait for mysql container to get up properly
sleep 20
# setup schema of mysql db
docker network connect mynet store_db
docker network connect mynet store_api
python setup_db.py
# start cli
docker ps
cd src
python cli.py
docker stop store_db
docker stop store_api
docker rm store_db
docker rm store_api
docker network rm mynet