# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Here you install the packages necessary for psycopg2 compilation if needed
RUN apt-get update && apt-get install -y \
	libpq-dev \
	gcc \
	libffi-dev \
	zlib1g-dev \
	curl \
	build-essential \
	libjpeg-dev \
	pkg-config \
	libssl-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install Rust compiler for cryptography package
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the init script and project files
COPY init-static.sh /app/
COPY . /app/

# Execute the init script
RUN chmod +x /app/init-static.sh && /app/init-static.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "farmeris.wsgi:application", "--bind", "0.0.0.0:8000"]
