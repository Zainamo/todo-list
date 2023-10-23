# todo-list
A TODO app for tracking tasks

To start, ensure your docker engine is running. Then run the following commands in order:

    docker-compose up -d --build  
    docker-compose exec backend flask --app src/app db upgrade
    docker-compose up

You will then be able to access the server at http://localhost:5000/
