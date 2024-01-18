# Theatre API
The Theatre API is a service for theatre management, developed using Django Rest Framework (DRF).

## Technologies Used
- JWT Auth: Implementation of JSON Web Tokens for secure authentication.
- PostgreSQL: An advanced open-source relational database.
- Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- Django Rest Framework (DRF): A powerful and flexible toolkit for building Web APIs in the Django framework.
- Docker: is a platform for developing, shipping, and running applications in containers. 
- Docker Compose: is a tool for defining and running multi-container Docker applications. 
- Django Debug Toolbar (DjDT): A set of panels displaying various debug information about the current request/response.
- SWAGGER UI: A popular tool for API documentation that allows visualization and interaction with API resources without direct access to the source code.
## Installing
### Run
```
git clone https://github.com/laskarj/theatre-api.git
cd theatre-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
docker-compose build
docker-compose up
```

### Getting access
- /api/user/register/ for register new user.
- /api/user/token get access token 

### Features
- JWT authenticated;
- Admin panel /admin/;
- Documentation is located at api/doc/swagger/;
- Managing reservation and ticket;
- Creating plays with artists and genres;
- Creating theatre halls;
- Adding performances;
- Filtering plays, performances, artists and reservation. 
