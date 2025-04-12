#!/bin/sh

cd ./src

mkdir $1

cd $1

touch schemas.py models.py services.py routes.py

echo "# your Pydantic schemas here" > schemas.py
echo "# your sqlalchemy models here" > models.py
echo "# your business logic here" > services.py
echo "# your api routers here" > routes.py

