# Lunch Voting Service

This is an internal service for a company that helps employees decide where to go for lunch. The service allows restaurants to upload their daily menus, employees can vote for their favorite menu, and the system tracks which menu is the most popular for the day.

## Technologies Used

- **Django**: The backend is built with Django.
- **Django REST Framework (DRF)**: For building the REST API.
- **PostgreSQL**: Used as the database to store all the data.
- **Docker**: The project is containerized using Docker.
- **JWT**: Used for authentication.
- **PyTest**: Used for testing the application.

## Features

1. **Restaurant Management**:
   - Administrators can create restaurants.
   - Administrators can upload menus for restaurants on a daily basis.

2. **Voting System**:
   - Employees can vote for a restaurant's menu, but only once per day.
   - The system ensures that each user can only vote for one menu per day.

3. **Endpoints**:
   - `GET /menu/current/`: Returns the menus for the current day.
   - `GET /menu/winner/`: Returns the menu that received the most votes for the current day.

4. **Authentication**:
   - Users authenticate via JWT tokens.
   - There is support for both updated and older versions of the mobile app (based on the build version sent in the headers).

5. **Admin Features**:
   - Only administrators can create restaurants and upload menus.

## Getting Started with Docker

To set up the project locally using Docker, follow these steps:

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A `.env` file containing environment variables (see `.env.example` for an example).

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/lunch-voting-service.git
   cd lunch-voting-service
   ```
   
2. Create a .env file

3. Build and start the services:

   ```bash
   docker-compose up --build
   ```
   
4. Migrate the database:

   ```bash
   docker-compose exec lunchipy sh
   python manage.py migrate
   ```
   
5. Running Tests:

   ```bash
   docker-compose exec lunchipy sh test
   ```
