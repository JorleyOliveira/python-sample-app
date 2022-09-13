## Python Sample App

## Install python 3.9 on UBUNTU

```
sudo apt update -y &&
sudo apt install -y software-properties-common &&
sudo add-apt-repository -y ppa:deadsnakes/ppa &&
sudo apt install -y python3.9 &&
python3.9 --version &&
sudo apt install -y python3.9-distutils &&
sudo apt-get -f install
```

## Setting up the VirtualEnv and install dependencies

```
pipenv shell --python=/usr/bin/python3.9
pipenv install

```

## Run the Application

```
python main.py

```

## Execute tests with pytest 

```
pytest tests/

```


## Test the application using swagger
```
http://localhost:9000/docs

```

## Check especification of application
```
http://localhost:9000/redoc

```