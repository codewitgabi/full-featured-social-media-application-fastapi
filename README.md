<div align="center">
    <h3>Full featured social media application -  FastAPI</h3>
</div>

A complex project that can leverage your existing backend skills while challenging you to learn and implement FastAPI concepts. Here’s a breakdown of the features to be implemented:

<br />

#### Database Design

This project models and schema strickly follows what is on the [database design file](https://dbdiagram.io/d/full-featured-social-media-app-66a43a2d8b4bb5230e7b6ae7)

<br />
<br />

#### Key Features

---

- **User Authentication**:

  - [x] User registration, login and logout
  - [x] Password hashing and JWT token-based authentication.
  - [ ] Role-based access control.

- **User profiles**:

  - [x] Create, update, and delete user profiles.
  - [x] Profile pictures and cover photos.
  - [x] Bio, contact information, and social links.

- **Posts and Feeds**:

  - [x] Create, edit, and delete posts (text, images, videos).
  - [ ] Like, comment, and share functionality.
  - [x] Real-time feed updates using WebSocket

- **Followers and Following**:

  - [x] Follow/unfollow users.
  - [x] Notifications for follows and follow-backs.
  - [x] Display follower and following lists.

- **Notifications**:

  - [ ] In-app notifications for likes, comments, shares, and follows.
  - [ ] Real-time notification updates using SSE.
  - [ ] Notification settings and preferences.

- **Messaging**:

  - [ ] Real-time private messaging between users.
  - [ ] Group chats and chat rooms.
  - [ ] File sharing within chats (images, documents, etc.).

- **Search and Discovery**:

  - [ ] Search users, posts, hashtags, and keywords.
  - [ ] Trending topics and suggested users to follow.
  - [ ] Tagging users in posts and comments.

- **Admin Panel**:

  - [ ] User management (view, ban, unban users).
  - [ ] Content moderation (flagged posts, reported users).
  - [ ] Analytics and dashboard for site activity.

<br />
<br />

#### Requirements

---

- **Documentation & Testing**:

  - Postman API documentation.
  - Comprehensive testing suite using pytest.

- **Database design**:

  - Use PostgreSQL database.
  - Design a robust schema to handle relationships and indexing.

- **Caching**:

  - Implement caching for frequently accessed data using Redis.
  - Use background tasks for cache invalidation.

- **Deployment**:

  - Use Docker for containerization.
  - Set up CI/CD pipelines for automated testing and deployment.
  - Deploy the application on a cloud provider (AWS, GCP, Azure) or any.

- **Security**:

  - Implement best security practices (CORS, CSRF protection, input validation).
  - Regular security audits and penetration testing.

- **Error handling**:

  - Endpoints should return the appropriate error responses and status codes
  - Errors should be properly handled to prevent server from crashing

<br />
<br />

#### Technologies to Learn and Use

---

- `FastAPI`: Main framework for building the application.
- `SQLAlchemy`: ORM for database interactions.
- `Alembic`: Database migrations.
- `Pydantic`: Data validation and settings management.
- `Docker`: Containerization.
- `Redis`: Caching and background task management.
- `Celery`: Background task queue.
- `WebSockets`: Real-time features (2-way).
- `SSE`: Real-time features (1-way).
- `pytest`: Testing.

<br />
<br />

#### Achievement

---

This project will challenge you to integrate various advanced features and best practices, providing a comprehensive learning experience in building complex backend systems with FastAPI.

<br />
<br />

#### Starting the project

---

Follow the steps below to get the project up and running

```shell
cd fastapi-social-media-api/
copy .env.sample .env
```

At this point, you should update the values in the created .env file. Now, let's setup our environment

```shell
pip -m venv venv # create virtual environment
pip install -r requirements.txt # install dependencies
```

Everything should run successfully. Next is to setup our database.

```shell
# create postgresql database
CREATE DATABASE fastapi-social-media-api;

# let's make migrations to our database
alembic upgrade head
```

We are now set up. Now, let's start our project server

```shell
python3 main.py
```

<br />
<br />

#### Testing

---

To run your tests using `pytest`, follow the steps below

```shell
pytest --disable-warnings -vv -s api/v1/tests
```
