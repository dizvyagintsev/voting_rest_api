# Voting REST API for choosing where to go to lunch

---

[![Swagger UI](https://img.shields.io/badge/Swagger-API_Documentation-brightgreen)](https://voting-rest-api-57093fdeadee.herokuapp.com/api/schema/swagger-ui/#/)


## How to use API

1. Register user using `/api/v1/register` endpoint
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
    Access token will be returned in response body, it is required for voting.

2. Create a restaurant using `/api/v1/restaurants/` endpoint
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/restaurants/" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data "{
      \"name\": \"string\",
      \"description\": \"string\"
    }"
    ```

3. Vote for a restaurant using `/api/v1/votes/` endpoint. Replace `<auth_token>` with the token received in step 1 and 
`<restaurant_id>` with the id of the restaurant created in step 2.
    ```bash
    curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/votes/" \
    --header "accept: application/json" \
    --header "Authorization: Bearer <auth_token>" \
    --header "Content-Type: application/json" \
    --data "{
      \"restaurant\": <restaurant_id>
    }"
    ```
   
4. Get results of voting using `/api/v1/votes-history/` endpoint
   ```bash
   curl --location "https://voting-rest-api-57093fdeadee.herokuapp.com/api/v1/votes-history/?start_date=2024-09-01&end_date=2024-09-30" \
   --header "accept: application/json"
   ```
   
## How to run locally

Prerequisites:
- Python 3.12
- Docker
- Poetry

1. Rename `.env.example` file to `.env` and set secret key and database credentials.

2. Run the following command to start web server and PostgreSQL database in Docker containers:
   ```bash
   make up
   ```
   
   Interact with the API using Swagger UI at http://localhost:8000/api/schema/swagger-ui/

3. To stop the containers run:
   ```bash
   make down
   ```
   
### Tests

Run tests with the following command:
```bash
make test
```

### Used technologies
1. Django – I usually prefer FastAPI for REST APIs, but in assignment was mentioned Django, so I decided to use it.
I didn't use async views because Django ORM doesn't fully support async yet.
2. PostgreSQL – I used PostgreSQL because entities have relations and their schema is fixed.
3. GitHub Actions – I used GitHub Actions for running tests and deploying to Heroku.

### Improvements
While the current implementation meets the requirements of this test assignment , there are several areas where further
enhancements could be made to improve the codebase. These enhancements have not been implemented due to time constraints 
but could be considered for future development:

1. Add more tests. Now only API tests are implemented, and it would be good to add tests for services and repositories.
2. Add more validation for input data. For example, check if the restaurant with the same name already exists. 
3. Add throttling on user registration and token acquisition to prevent brute force attacks.
4. Introduce a separate service for vote result calculation: Currently, new votes are stored without any real-time 
aggregation or modification, allowing for flexible result calculation at a later time. Simple aggregations are handled 
by the database, while more complex calculations (e.g., vote weights) are done in Python. If daily vote volume grows 
significantly, Python memory could become a bottleneck. A dedicated service that processes new votes streamingly would 
handle result calculation independently and scale as needed.




