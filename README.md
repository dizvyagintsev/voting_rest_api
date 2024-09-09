# Voting REST API for Choosing Where to Go to Lunch

[![Swagger UI](https://img.shields.io/badge/Swagger-API_Documentation-brightgreen)](https://voting-rest-api-57093fdeadee.herokuapp.com/api/schema/swagger-ui/#/)
![GitHub Actions Status](https://github.com/dizvyagintsev/voting_rest_api/actions/workflows/ci.yml/badge.svg)


## How to Use the API

1. **Register a user** using the `/api/v1/register` endpoint:
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/register/" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data-raw "{
      \"username\": \"username\",
      \"password\": \"password\",
      \"email\": \"user@example.com\"
    }"
    ```
   The response will return an access token, which is required for voting.

2. **Create a restaurant** using the `/api/v1/restaurants/` endpoint:
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/restaurants/" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data-raw "{
      \"name\": \"string\",
      \"description\": \"string\"
    }"
    ```

3. **Vote for a restaurant** using the `/api/v1/votes/` endpoint. Replace `<auth_token>` with the token received in step 1, and `<restaurant_id>` with the ID of the restaurant created in step 2:
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/votes/" \
    --header "accept: application/json" \
    --header "Authorization: Bearer <auth_token>" \
    --header "Content-Type: application/json" \
    --data-raw "{
      \"restaurant\": <restaurant_id>
    }"
    ```
   **Voting Restrictions**: Users can vote only a limited number of times within a set period, depending on the system rules. If the voting limit is exceeded, a 403 error may be returned.

4. **Get voting results** using the `/api/v1/votes-history/` endpoint:
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/votes-history/?start_date=2024-09-01&end_date=2024-09-30" \
    --header "accept: application/json"
    ```
   
   You can also explore and interact with the API through the Swagger UI, which is available [here](https://voting-rest-api-57093fdeadee.herokuapp.com/api/schema/swagger-ui/#/), without needing to manually execute these commands.

## How to Run Locally

### Prerequisites

- Python 3.12
- Docker
- Poetry

1. Rename `.env.example` to `.env` and configure the secret key and database credentials.

2. Start the web server and PostgreSQL database in Docker containers:
   ```bash
   make up
   ```
   You can interact with the API using Swagger UI at [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/).

3. To stop the containers, run:
   ```bash
   make down
   ```

### Running Tests

Run tests with the following command:
```bash
make test
```

### Technologies Used

1. **Django** – While I usually prefer FastAPI for REST APIs, Django was specified in the assignment, so I chose it for this project. I opted not to use async views because Django's ORM doesn't fully support async operations yet.
2. **PostgreSQL** – I picked PostgreSQL because it handles relationships well and works great with a fixed schema.
3. **GitHub Actions** – I used GitHub Actions for running tests and deploying to Heroku.

### Possible Improvements

While the current implementation meets the requirements of this test assignment , there are several areas where further enhancements could be made to improve the codebase. These enhancements have not been implemented due to time constraints but could be considered for future development:

1. **Additional Tests**: Add tests for services and repositories, not just API tests.
3. **Rate Limiting**: Add throttling to user registration and token acquisition to prevent brute force attacks.
5. **Vote Calculation Service**: If the application experiences high load and performance degradation, a dedicated service for vote result calculations could be introduced. This service would process votes asynchronously, possibly using event streaming (e.g., Redis Streams or Kafka) to handle large-scale data more efficiently. For smaller-scale tasks, the current approach of handling vote calculations in Python with simple database aggregations should be sufficient.
