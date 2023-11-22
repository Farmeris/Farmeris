# Farmeris

This repository contains the backend code necessary to run the platform for managing web site logic and operations for our Appalachia project.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed the latest version of Docker and Docker Compose.
- You have a basic understanding of Docker containerization and Docker Compose.

## Installation & Setup

To set up the Farmeris platform, follow these steps:

### Docker Environment

1. Clone the repository to your local machine:

```
git clone git@gitlab.com:farmeris/farmeris.git
```

2. Navigate to the cloned directory:

```
cd farmeris
```

3. To build and run the Docker containers in the background using the `Makefile`, execute:

```
make farmeris_full
```

This command builds the Docker image and runs the containers as specified in your `docker-compose.prod.yml` file.

### Local Development Without Docker

If you wish to run the project without Docker:

1. Create a virtual environment in the project directory:

```
python -m venv myvenv
```

2. Activate the virtual environment:

- On Windows:
  ```
  venv\Scripts\activate
  ```

- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Run the Django development server:

```
python manage.py runserver
```

The Django application will start on the default port `8000`.

## Usage

After setting up the project with Docker, you can manage the Docker containers using Docker Compose commands. Here are some common commands you might find useful:

- To start the services:

```
docker-compose -f docker-compose.prod.yml up
```

- To rebuild the services:

```
docker-compose -f docker-compose.prod.yml up --build
```

- To stop the services:

```
docker-compose -f docker-compose.prod.yml down
```

For more detailed information on Docker Compose commands, refer to the [Docker Compose documentation](https://docs.docker.com/compose/).

## Contributing to Farmeris

To contribute to Farmeris, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <my_branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin farmeris/<my_branch_name>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contact

If you have any questions or would like to contact the maintainers, please email us at farmeris-sk@proton.me.

## License

This project uses the following license: 
