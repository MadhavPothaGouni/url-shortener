# CHANGES.md

1. **Initialized Flask App**  
   Set up the base Flask application with necessary configuration and routing structure for a modular URL shortener service.

2. **Added Health Check Endpoints**  
   Implemented two endpoints (`/` and `/api/health`) to verify that the service is running properly. These endpoints return simple JSON responses indicating system status.

3. **Implemented URL Shortening Endpoint**  
   Built a POST endpoint at `/api/shorten` that accepts a long URL, validates it, and generates a unique short code for redirection.

4. **Handled Invalid and Empty URL Input**  
   Added input validation to ensure the user submits a non-empty and correctly formatted URL. Returns a clear error message for invalid inputs.

5. **Generated Unique Short Codes**  
   Designed a function to generate random alphanumeric short codes and ensured uniqueness by checking against existing codes in memory.

6. **Mapped URLs In-Memory**  
   Used a Python dictionary to store the mapping between the short code and the original URL along with metadata like creation time and click count.

7. **Created Redirection Logic**  
   Set up a dynamic route `/s/<short_code>` that redirects the user to the original URL if the short code exists. If not, returns a 404 error.

8. **Tracked Click Count and Analytics**  
   Each time a short link is visited, the app increments a counter. An endpoint `/api/analytics/<short_code>` displays how many times the short link was accessed, when it was created, and what original URL it points to.

9. **Wrote 5 Core Functional Tests**  
   Developed and passed 5 `pytest` test cases to verify functionality including:  
   - URL shortening  
   - Redirection  
   - Error on invalid input  
   - Analytics reporting  
   - Handling of non-existent short codes

10. **Addressed Deprecation Warning**  
    Updated usage of `datetime.utcnow()` to a timezone-aware method using `datetime.now(timezone.utc)` to comply with modern Python standards and avoid future warnings.

