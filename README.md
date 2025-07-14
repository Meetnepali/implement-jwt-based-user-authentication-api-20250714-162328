# User Management API Assessment

## Task Overview
You are provided with a partially implemented FastAPI user management API. Your task is to complete the implementation of JWT authentication, registration, role-based admin endpoints, custom error handling, async ORM integration, dependency injection, and enhanced OpenAPI documentation. All endpoints should be organized via routers, operate asynchronously, and use SQLAlchemy's async features.

### Requirements
- Users can register and log in to obtain a JWT.
- Users can update their own profiles.
- Only admins can list all users or delete any user.
- Passwords must be securely hashed.
- Use dependency injection for database/session and authentication.
- Organize code with FastAPI routers.
- Implement custom error handlers that return consistent JSON error models.
- Enhance OpenAPI docs with endpoint grouping via tags and example responses.
- All data access must be async (use async session/queries).
- All features must be tested (see provided test suite).

## Setup Instructions

1. **Build and start the environment:**
   ```sh
   ./run.sh
   ```
   This will build the Docker image and run the app on [http://localhost:8000](http://localhost:8000)

2. **API Documentation:**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the OpenAPI documentation.

3. **Testing:**
   To run the tests, open a shell in the running container:
   ```sh
   docker-compose exec app bash
   pytest
   ```

## Completing the Assessment
- Ensure all endpoints are implemented and operate asynchronously.
- Complete any missing authentication, role checks, and error models.
- Confirm that all endpoints behave as described and tests pass for both admin and regular users.
- Ensure OpenAPI docs are well-organized with tags and example responses.

## Notes
- Do not remove or modify provided tests except as needed for compatibility.
- Focus on clear, production-like FastAPI implementation.
