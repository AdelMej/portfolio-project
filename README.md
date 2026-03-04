```
_____ _______ _    _         _         _______     ____  _
_ 
     /\   / ____|__   __| |  | |  /\   | |       / ____\ \   / /  \/  |
    /  \ | |       | |  | |  | | /  \  | |      | |  __ \ \_/ /| \  / |
   / /\ \| |       | |  | |  | |/ /\ \ | |      | | |_| \   / | |\/| |
  / ____ \ |____   | |  | |__| / ____ \| |____  | |__| |  | |  | |  | |
 /_/    \_\_____|  |_|   \____/_/    \_\______|  \_____|  |_|  |_|  |_|
```

## 📌 Project Overview

This portfolio project is a web-based gym management system developed for Actual Digital.

The company operates a small gym within one of its buildings. The gym is managed directly by the building manager, who is responsible for handling member registrations, payments, and general administrative tasks.
The purpose of this platform is to reduce the manager’s administrative workload by providing a centralized web application to manage:

- Member registration and profiles
- Payment recording and tracking
- Membership management
- Basic administrative operations
By digitizing these processes, the system simplifies daily management tasks, improves data organization, and minimizes manual record-keeping.

## 🔖 Table of Contents

<details>
 <summary>
  Click to enlarge
 </summary>

- 🔨 [Tech stack](#-tech-stack)
- 🎬 [Demo](#-demo)
- 🌐 [Api](#-api)
- 🏗️ [Structure](#%EF%B8%8Fstructure)
- 🔧 [What's next?](#-whats-next)
- 👷 [Authors](#-authors)

</details>

## 🔨 Tech stack

### Database

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

### Backend

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

### Frontend

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![Svelte](https://img.shields.io/badge/sveltekit-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)

### DevOps

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## 🎬 Demo

Work in progress

## 🌐 Api

### Authentication and authorization

## Route: <`POST`> <`/auth/login`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /auth/login          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Request body               |  email, password           |
| Success response           |  200           |
| Error responses            |  422, 401           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| email | Emailstr | yes | the user email |
| password | string | yes | the user password |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  access_token     |   string    |  the jwt access token           |
| token_type | string | the token type |

---

## Route: <`POST`> <`/auth/refresh`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /auth/refresh          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Request body               |  None           |
| Success response           |  204           |
| Error responses            |  422, 400, 404, 401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  access_token     |   string    |  the jwt access token           |
| token_type | string | the token type |

---

## Route: <`POST`> <`/auth/register`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /auth/register          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Request body               |  email, password, first_name, last_name           |
| Success response           |  201           |
| Error responses            |  422, 400           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| email | Emailstr | yes | the user email |
| password | string | yes | the user password |
| first_name | string | yes | the user first name |
| last_name | string | yes | the user last name |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  message     |   string    |  success message           |

---

## Route: <`POST`> <`/auth/logout`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /auth/logout          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Request body               |  email, password, first_name, last_name           |
| Success response           |  204           |
| Error responses            |  204           |

### me

## Route: <`GET`> <`/me/`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /me/          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_SELF         |
| Success response           |  200           |
| Error responses            |  401, 403            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  email     |   Emailstr    |  the user email           |
| roles | string[] | the user roles |

---

## Route: <`DELETE`> <`/me/`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   DELETE      |
| Endpoint                   |   /me/          |
| Auth required              |   yes          |
| Required permission / role |    user, DELETE_SELF         |
| Success response           |  204           |
| Error responses            |  401, 403, 409            |

---

## Route: <`PATCH`> <`/me/email-change`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PATCH      |
| Endpoint                   |   /me/email-change          |
| Auth required              |   yes          |
| Required permission / role |    USER         |
| Request body               |  email           |
| Success response           |  204           |
| Error responses            |  422, 400, 401, 403, 409           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| email | Emailstr | yes | the user email |

---

## Route: <`PATCH`> <`/me/password-change`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PATCH      |
| Endpoint                   |   /me/password-change          |
| Auth required              |   yes          |
| Required permission / role |    USER         |
| Request body               |  email           |
| Success response           |  204           |
| Error responses            |  422, 400, 401, 403, 409           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| old_password | string | yes | the user current password |
| new_password | string | yes | the user new passowrd |

---

## Route: <`GET`> <`/me/profile`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /me/profile          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_SELF         |
| Success response           |  200           |
| Error responses            |  401, 403            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  first_name     |   string    |  the user first name           |
|last_name | string | the user last name |

---

## Route: <`PUT`> <`/me/profile`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /me/profile          |
| Auth required              |   yes          |
| Required permission / role |    USER, UPDATE_SELF         |
| Request body               |  first_name, last_name           |
| Success response           |  204           |
| Error responses            |  422, 401, 403, 400           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| first_name | string | yes | the user first name |
| last_name | string | yes | the user last name |

---

## Route: <`GET`> <`/me/sessions`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /me/sessions          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   sessions[]    |  the user sessions           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

---

## Route: <`GET`> <`/me/sessions/{session_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /me/sessions/{session_id}          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403, 404            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  session     |   session    |  the user session asked for          |

---

### sessions

## Route: <`GET`> <`/sessions`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /sessions          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Success response           |  200           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   sessions[]    |  the available sessions           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

---

## Route: <`PUT`> <`/sessions/{session_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /sessions/{session_id}          |
| Auth required              |   yes          |
| Required permission / role |    COACH, ADMIN, UPDATE_SESSION         |
| Request body               |  title, starts_at, ends_at           |
| Success response           |  204           |
| Error responses            |  422, 401, 403, 400, 404, 409           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| title | string | yes | the new title |
| starts_at | datetime | yes | the new session starting time |
| ends_at | datetime | yes | the new session ending time |

---

## Route: <`POST`> <`/sessions`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /sessions          |
| Auth required              |   yes          |
| Required permission / role |    COACH CREATE_SESSION         |
| Request body               |  title, starts_at, ends_at, price_cents, currency            |
| Success response           |  201           |
| Error responses            |  422, 401, 403, 400, 404, 409           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| title | string | yes | the new title |
| starts_at | datetime | yes | the new session starting time |
| ends_at | datetime | yes | the new session ending time |
| price_cents | int | yes | the session price in cents|
| currency | str | yes | the session currency |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
| message | string | session creation successful |

--

## Route: <`GET`> <`/sessions/{session_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /sessions/{session_id}          |
| Auth required              |   no          |
| Required permission / role |    None         |
| Success response           |  200           |
| Error responses            |  404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  session     |   sessions   |  the sessions with session_id          |

---

## Route: <`PUT`> <`/sessions/cancel`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /sessions/cancel          |
| Auth required              |   yes          |
| Required permission / role |    COACH, CANCEL_SESSION         |
| Request body               |  None           |
| Success response           |  204           |
| Error responses            |  401, 403, 400, 404, 409           |

---

## Route: <`GET`> <`/sessions/{session_id}/attendance`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /sessions/{session_id}/attendance          |
| Auth required              |   yes          |
| Required permission / role |    coach, READ_ATTENDANCE         |
| Success response           |  200           |
| Error responses            |  422, 401, 403, 404            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  attedance list     |  userprofile[]   |  the user attendance list for the session |

---

## Route: <`PUT`> <`/sessions/{session_id}/attendance`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /sessions/{session_id}/attendance          |
| Auth required              |   yes          |
| Required permission / role |    coach, CREATE_ATTENDANCE         |
| Success response           |  204           |
| Error responses            |  422, 401, 403, 404            |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| attendance list | attendance[] | yes | the list of attendee |

---

## Route: <`POST`> <`/sessions/{session_id}/cancel-registration`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /sessions/{session_id}/cancel-registration          |
| Auth required              |   yes          |
| Required permission / role |    user, CANCEL_REGISTRATION         |
| Success response           |  204           |
| Error responses            |  401, 403, 404, 409            |

---

## Route: <`POST`> <`/sessions/{session_id}/register`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /sessions/{session_id}/register          |
| Auth required              |   yes          |
| Required permission / role |    user, CREATE_REGISTRATION         |
| Success response           |  204           |
| Error responses            |  401, 403, 404, 409            |

### credits

## Route: <`GET`> <`/credit`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /credit          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_CREDIT         |
| Success response           |  200           |
| Error responses            |  401, 403            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   credit[]    |  the available credits           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

### payments

## Route: <`GET`> <`/payment`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /payment          |
| Auth required              |   yes          |
| Required permission / role |    user, READ_PAYMENT         |
| Success response           |  200           |
| Error responses            |  401, 403            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   payment[]    |  the available payments           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

### stripe

## Route: <`POST`> <`/stripe/event`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /stripe/event          |
| Auth required              |   yes          |
| Required permission / role |    stripe-signature         |
| Success response           |  200           |
| Error responses            |  401, 403, 503            |

### coach

## Route: <`POST`> <`/coach/stripe/account`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /coach/stripe/account          |
| Auth required              |   yes          |
| Required permission / role |    coach, CREATE_STRIPE_ACCOUNT         |
| Success response           |  200           |
| Error responses            |  401, 403, 503            |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
| onboarding_link | str | stripe connect onboarding link |

---

## Route: <`POST`> <`/coach/{session_id}/payout`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /coach/{session_id}/payout          |
| Auth required              |   yes          |
| Required permission / role |    None         |
| Success response           |  204           |
| Error responses            |  400, 403, 404, 503            |

---

## Route: <`GET`> <`/coach/sessions/{session_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /coach/sessions/{session_id}          |
| Auth required              |   yes          |
| Required permission / role |    coach, COACH_READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  session     |   sessions   |  the sessions owned by coach with session_id          |

---

## Route: <`GET`> <`/coach/sessions`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /coach/sessions          |
| Auth required              |   yes          |
| Required permission / role |    coach, COACH_READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   sessions[]    |  the coach owned sessions           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

### admin-user

## Route: <`GET`> <`/admin/users/`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/users/          |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, ADMIN_READ_USERS         |
| Success response           |  200           |
| Error responses            |  401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   userprofile[]    |  all user profiles           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

---

## Route: <`GET`> <`/admin/users/{user_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/users/{user_id}         |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, ADMIN_READ_USERS        |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  userprofile     |   userprofile    |  the user  profile by user_id           |

---

## Route: <`POST`> <`/admin/users/{user_id}/grant-role`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /admin/users/{user_id}/grant-role         |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, GRANT_ROLE        |
| Success response           |  204           |
| Error responses            |  401, 403, 404           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| role | userRole | yes | an enumeration of possible roles to grant |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  userprofile     |   userprofile    |  the user  profile by user_id           |

---

## Route: <`POST`> <`/admin/users/{user_id}/revoke-role`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /admin/users/{user_id}/revoke-role         |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, GRANT_ROLE        |
| Success response           |  204           |
| Error responses            |  401, 403, 404           |

## Request body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| role | userRole | yes | an enumeration of possible roles to revoke |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  userprofile     |   userprofile    |  the user  profile by user_id           |

---

## Route: <`POST`> <`/admin/users/{user_id}/disable`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /admin/users/{user_id}/grant-role         |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, DISABLE_USER        |
| Success response           |  204           |
| Error responses            |  401, 403, 404           |

---

## Route: <`POST`> <`/admin/users/{user_id}/reenable`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   POST      |
| Endpoint                   |   /admin/users/{user_id}/grant-role         |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, REEENABLE_USER        |
| Success response           |  204           |
| Error responses            |  401, 403, 404, 409  |

### admin-session

## Route: <`GET`> <`/admin/sessions/{session_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/sessions/{session_id}          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN,  ADMIN_READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  session     |   sessions   |  the sessions by session_id          |

---

## Route: <`GET`> <`/admin/sessions`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/sessions          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN, ADMIN_READ_SESSION         |
| Success response           |  200           |
| Error responses            |  401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   sessions[]    |  all the sessions           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

---

## Route: <`PUT`> <`/admin/sessions/cancel`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   PUT      |
| Endpoint                   |   /admin/sessions/cancel          |
| Auth required              |   yes          |
| Required permission / role |    ADMIN, ADMIN_CANCEL_SESSION         |
| Request body               |  None           |
| Success response           |  204           |
| Error responses            |  401, 403, 400, 404, 409           |

---

## Route: <`GET`> <`/admin/sessions/{session_id}/attendance`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/sessions/{session_id}/attendance          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN,  ADMIN_READ_ATTENDANCE         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  user profile     |   userprofile[]   |  the profile of the attendee          |

### admin-payment

## Route: <`GET`> <`/admin/payment/users/{user_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/payment/users/{user_id}          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN,  ADMIN_READ_PAYMENT         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  payment     |   payment   |  the payment by user_id          |

---

## Route: <`GET`> <`/admin/payment/coach/{coach_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/payment/coach/{coach_id}          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN,  ADMIN_READ_PAYMENT         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  payment     |   payment   |  the payment by coach_id          |

---

## Route: <`GET`> <`/admin/payment`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/sessions          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN, ADMIN_READ_PAYMENT         |
| Success response           |  200           |
| Error responses            |  401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   payment[]    |  all the payments           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

### admin-credit

## Route: <`GET`> <`/admin/credit/{user_id}`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/credit/{credit_id}          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN,  ADMIN_READ_CREDIT         |
| Success response           |  200           |
| Error responses            |  401, 403, 404           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  credit     |   credits   |  the credit by user_id          |

---

## Route: <`GET`> <`/admin/credit`>

| Field                      | Description |
| -------------------------- | ----------- |
| Method                     |   GET      |
| Endpoint                   |   /admin/credit          |
| Auth required              |   yes          |
| Required permission / role |   ADMIN, ADMIN_READ_CREDIT         |
| Success response           |  200           |
| Error responses            |  401, 403           |

## Response body

| Field | Type | Description |
| ----- | ---- | ----------- |
|  items     |   credits[]    |  all the credits           |
| limit | int | limit for the number of pages |
| offset | int | where the page starts |
| has_more | boolean | are more pages available |

### References

[Backend](./backend/)

## 🏗️ Structure

| directory | description |
| -------------- | --------------- |
| [db](./db/) | directory containing sql scripts for db definition |
| [backend](./backend/)| directory containing the backend code in fastapi |
| [Frontend](./frontend/)| directory containing the frontend code in svelte |

### architecture

- Feature first
  - Domain Driven
  - Unit of Work
  - Repository
  - Dependency injection
  - Hexagonal with Ports and Adapters

<details>
 <summary>
  Click to enlarge
 </summary>

```bash
.
├── backend
│   ├── app
│   │   ├── domain
│   │   │   ├── auth
│   │   │   │   ├── actor_entity.py
│   │   │   │   ├── auth_email_rules.py
│   │   │   │   ├── auth_exceptions.py
│   │   │   │   ├── auth_password_rules.py
│   │   │   │   ├── permission.py
│   │   │   │   ├── permission_rules.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── actor_entity.cpython-314.pyc
│   │   │   │   │   ├── auth_exceptions.cpython-314.pyc
│   │   │   │   │   ├── refresh_token_entity.cpython-314.pyc
│   │   │   │   │   └── role.cpython-314.pyc
│   │   │   │   ├── refresh_token_entity.py
│   │   │   │   ├── refresh_tokens_rules.py
│   │   │   │   └── role.py
│   │   │   ├── coach_stripe_acount
│   │   │   ├── credit
│   │   │   │   ├── credit_cause.py
│   │   │   │   ├── credit_entity.py
│   │   │   │   └── credit_exception.py
│   │   │   ├── currency
│   │   │   │   ├── currency_exception.py
│   │   │   │   └── currency_rules.py
│   │   │   ├── __init__.py
│   │   │   ├── payment
│   │   │   │   ├── payment_entity.py
│   │   │   │   └── payment_exception.py
│   │   │   ├── payment_intent
│   │   │   │   ├── payment_intent_entity.py
│   │   │   │   ├── payment_intent_exceptions.py
│   │   │   │   └── payment_intent_providers.py
│   │   │   ├── __pycache__
│   │   │   │   └── __init__.cpython-314.pyc
│   │   │   ├── session
│   │   │   │   ├── session_creation_rules.py
│   │   │   │   ├── session_entity.py
│   │   │   │   ├── session_exception.py
│   │   │   │   └── session_status.py
│   │   │   ├── session_participation
│   │   │   │   └── session_participation_entity.py
│   │   │   ├── stripe
│   │   │   │   └── stripe_exception.py
│   │   │   └── user
│   │   │       ├── __pycache__
│   │   │       │   └── user_entity.cpython-314.pyc
│   │   │       ├── user_entity.py
│   │   │       ├── user_exceptions.py
│   │   │       ├── user_profile_entity.py
│   │   │       └── user_profile_rules.py
│   │   ├── feature
│   │   │   ├── admin
│   │   │   │   ├── credit
│   │   │   │   │   ├── admin_credit_dependencies.py
│   │   │   │   │   ├── admin_credit_dto.py
│   │   │   │   │   ├── admin_credit_exception.py
│   │   │   │   │   ├── admin_credit_router.py
│   │   │   │   │   ├── admin_credit_service.py
│   │   │   │   │   ├── repositories
│   │   │   │   │   │   ├── admin_credit_read_repository_port.py
│   │   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   └── uow
│   │   │   │   │       └── admin_credit_uow_port.py
│   │   │   │   ├── payment
│   │   │   │   │   ├── admin_payment_dependencies.py
│   │   │   │   │   ├── admin_payment_dto.py
│   │   │   │   │   ├── admin_payment_exception.py
│   │   │   │   │   ├── admin_payment_router.py
│   │   │   │   │   ├── admin_payment_service.py
│   │   │   │   │   ├── repositories
│   │   │   │   │   │   ├── admin_payment_read_repository_port.py
│   │   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   └── uow
│   │   │   │   │       └── admin_payment_uow_port.py
│   │   │   │   ├── session
│   │   │   │   │   ├── admin_session_dependencies.py
│   │   │   │   │   ├── admin_session_dto.py
│   │   │   │   │   ├── admin_session_exception.py
│   │   │   │   │   ├── admin_session_router.py
│   │   │   │   │   ├── admin_session_service.py
│   │   │   │   │   ├── repositories
│   │   │   │   │   │   ├── admin_session_attendance_read_repo.py
│   │   │   │   │   │   ├── admin_session_read_repository_port.py
│   │   │   │   │   │   ├── admin_session_update_repository_port.py
│   │   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   └── uow
│   │   │   │   │       ├── admin_session_system_uow_port.py
│   │   │   │   │       └── admin_session_uow_port.py
│   │   │   │   └── users
│   │   │   │       ├── admin_user_dependencies.py
│   │   │   │       ├── admin_user_exception.py
│   │   │   │       ├── admin_users_dto.py
│   │   │   │       ├── admin_users_router.py
│   │   │   │       ├── admin_users_service.py
│   │   │   │       ├── repositories
│   │   │   │       │   ├── admin_user_creation_repository_port.py
│   │   │   │       │   ├── admin_user_deletion_repository_port.py
│   │   │   │       │   ├── admin_user_read_repository_port.py
│   │   │   │       │   ├── admin_user_update_repository.py
│   │   │   │       │   ├── auth_read_repository_port.py
│   │   │   │       │   └── __init__.py
│   │   │   │       └── uow
│   │   │   │           ├── admin_user_system_uow_port.py
│   │   │   │           └── admin_user_uow_port.py
│   │   │   ├── auth
│   │   │   │   ├── auth_dependencies.py
│   │   │   │   ├── auth_dto.py
│   │   │   │   ├── auth_exception.py
│   │   │   │   ├── auth_router.py
│   │   │   │   ├── auth_service.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── auth_dto.cpython-314.pyc
│   │   │   │   │   ├── auth_service.cpython-314.pyc
│   │   │   │   │   └── auth_UoW_port.cpython-314.pyc
│   │   │   │   ├── repositories
│   │   │   │   │   ├── auth_creation_respository_port.py
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── auth_update_repository_port.py
│   │   │   │   │   ├── me_delete_repository_port.py
│   │   │   │   │   └── __pycache__
│   │   │   │   │       ├── auth_creation_respository.cpython-314.pyc
│   │   │   │   │       ├── auth_read_repository.cpython-314.pyc
│   │   │   │   │       └── auth_update_repository.cpython-314.pyc
│   │   │   │   └── uow
│   │   │   │       ├── auth_uow_port.py
│   │   │   │       ├── __pycache__
│   │   │   │       │   └── login_uow.cpython-314.pyc
│   │   │   │       └── registration_uow_port.py
│   │   │   ├── coach
│   │   │   │   ├── coach_dependencies.py
│   │   │   │   ├── coach_dto.py
│   │   │   │   ├── coach_exception.py
│   │   │   │   ├── coach_router.py
│   │   │   │   ├── coach_service.py
│   │   │   │   ├── repositories
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── coach_stripe_account_creation_repository_port.py
│   │   │   │   │   ├── coach_stripe_account_read_repository_port.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── payment_creation_repository_port.py
│   │   │   │   │   ├── payment_read_repository_port.py
│   │   │   │   │   └── session_read_repository_port.py
│   │   │   │   └── uow
│   │   │   │       └── coach_uow_port.py
│   │   │   ├── credit
│   │   │   │   ├── credit_dependencies.py
│   │   │   │   ├── credit_dto.py
│   │   │   │   ├── credit_exception.py
│   │   │   │   ├── credit_router.py
│   │   │   │   ├── credit_service.py
│   │   │   │   ├── respositories
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── credit_ledger_read_repository_port.py
│   │   │   │   │   └── __init__.py
│   │   │   │   └── uow
│   │   │   │       └── credit_uow_port.py
│   │   │   ├── __init__.py
│   │   │   ├── me
│   │   │   │   ├── me_dependencies.py
│   │   │   │   ├── me_dto.py
│   │   │   │   ├── me_exception.py
│   │   │   │   ├── me_router.py
│   │   │   │   ├── me_service.py
│   │   │   │   ├── repositories
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── auth_update_repo_port.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── me_delete_repository_port.py
│   │   │   │   │   ├── me_read_repository_port.py
│   │   │   │   │   ├── me_update_repository_port.py
│   │   │   │   │   ├── session_participation_read_repository_port.py
│   │   │   │   │   └── session_read_repository_port.py
│   │   │   │   └── uow
│   │   │   │       ├── me_system_uow_port.py
│   │   │   │       └── me_uow_port.py
│   │   │   ├── payment
│   │   │   │   ├── payment_dependencies.py
│   │   │   │   ├── payment_dto.py
│   │   │   │   ├── payment_exception.py
│   │   │   │   ├── payment_router.py
│   │   │   │   ├── payment_service.py
│   │   │   │   ├── repostories
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── payment_read_repository.py
│   │   │   │   └── uow
│   │   │   │       └── payment_uow_port.py
│   │   │   ├── __pycache__
│   │   │   │   └── __init__.cpython-314.pyc
│   │   │   ├── session
│   │   │   │   ├── repositories
│   │   │   │   │   ├── auth_read_repository_port.py
│   │   │   │   │   ├── coach_stripe_account_read_repository_port.py
│   │   │   │   │   ├── credit_ledger_creation_repository_port.py
│   │   │   │   │   ├── credit_ledger_read_repository_port.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── payment_intent_creation_repository_port.py
│   │   │   │   │   ├── session_attendance_creation_repository.py
│   │   │   │   │   ├── session_attendance_read_repository.py
│   │   │   │   │   ├── session_creation_repository_port.py
│   │   │   │   │   ├── session_participation_creation_repository.py
│   │   │   │   │   ├── session_participation_read_repository.py
│   │   │   │   │   ├── session_participation_update_repository_port.py
│   │   │   │   │   ├── session_read_repository_port.py
│   │   │   │   │   └── session_update_repository_port.py
│   │   │   │   ├── session_dependencies.py
│   │   │   │   ├── session_dto.py
│   │   │   │   ├── session_exception.py
│   │   │   │   ├── session_router.py
│   │   │   │   ├── session_service.py
│   │   │   │   └── uow
│   │   │   │       ├── session_public_uow_port.py
│   │   │   │       └── session_uow_port.py
│   │   │   └── stripe
│   │   │       ├── repositories
│   │   │       │   ├── coach_stripe_account_update_repository_port.py
│   │   │       │   ├── credit_ledger_cretion_repository_port.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── payment_creation_repo_port.py
│   │   │       │   ├── payment_intent_read_repository.py
│   │   │       │   ├── payment_intent_update_repository_port.py
│   │   │       │   └── session_participation_update_repository_port.py
│   │   │       ├── stripe_dependencies.py
│   │   │       ├── stripe_dto.py
│   │   │       ├── stripe_exception.py
│   │   │       ├── stripe_router.py
│   │   │       ├── stripe_service.py
│   │   │       └── uow
│   │   │           └── stripe_uow_port.py
│   │   ├── infrastructure
│   │   │   ├── __init__.py
│   │   │   ├── persistence
│   │   │   │   ├── __init__.py
│   │   │   │   ├── in_memory
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── provider.py
│   │   │   │   │   ├── __pycache__
│   │   │   │   │   │   ├── __init__.cpython-314.pyc
│   │   │   │   │   │   └── storage.cpython-314.pyc
│   │   │   │   │   ├── repositories
│   │   │   │   │   │   └── auth
│   │   │   │   │   │       ├── auth_creation_repository.py
│   │   │   │   │   │       ├── auth_read_repository.py
│   │   │   │   │   │       ├── auth_update_repository.py
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── __pycache__
│   │   │   │   │   │           ├── auth_creation_repository.cpython-314.pyc
│   │   │   │   │   │           ├── auth_read_repository.cpython-314.pyc
│   │   │   │   │   │           ├── auth_update_repository.cpython-314.pyc
│   │   │   │   │   │           └── __init__.cpython-314.pyc
│   │   │   │   │   ├── storage.py
│   │   │   │   │   └── uow
│   │   │   │   │       └── auth
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           ├── login_uow.py
│   │   │   │   │           └── __pycache__
│   │   │   │   │               ├── __init__.cpython-314.pyc
│   │   │   │   │               └── login_uow.cpython-314.pyc
│   │   │   │   ├── __pycache__
│   │   │   │   │   └── __init__.cpython-314.pyc
│   │   │   │   └── sqlalchemy
│   │   │   │       ├── base.py
│   │   │   │       ├── engines.py
│   │   │   │       ├── __init__.py
│   │   │   │       ├── provider.py
│   │   │   │       ├── repositories
│   │   │   │       │   ├── admin
│   │   │   │       │   │   ├── credit
│   │   │   │       │   │   │   └── admin_credit_read_repository.py
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── payment
│   │   │   │       │   │   │   └── admin_payment_read_repository.py
│   │   │   │       │   │   ├── session
│   │   │   │       │   │   │   ├── admin_session_read_repository.py
│   │   │   │       │   │   │   └── admin_session_update_repository.py
│   │   │   │       │   │   ├── session_attendance
│   │   │   │       │   │   │   └── admin_session_attendance_repository.py
│   │   │   │       │   │   └── users
│   │   │   │       │   │       ├── admin_user_creatiton_repository.py
│   │   │   │       │   │       ├── admin_user_deletion_repository_port.py
│   │   │   │       │   │       ├── admin_user_read_repository.py
│   │   │   │       │   │       └── admin_user_update_repository.py
│   │   │   │       │   ├── auth
│   │   │   │       │   │   ├── auth_creation_repository.py
│   │   │   │       │   │   ├── auth_read_repository.py
│   │   │   │       │   │   ├── auth_update_repository.py
│   │   │   │       │   │   └── __init__.py
│   │   │   │       │   ├── coach_stripe_account
│   │   │   │       │   │   ├── coach_stripe_account_creation_repository.py
│   │   │   │       │   │   ├── coach_stripe_account_read_repository.py
│   │   │   │       │   │   ├── coach_stripe_account_update_repository.py
│   │   │   │       │   │   └── __init__.py
│   │   │   │       │   ├── credit_ledger
│   │   │   │       │   │   ├── credit_ledger_creation_repository.py
│   │   │   │       │   │   ├── credit_ledger_read_repository.py
│   │   │   │       │   │   └── __init__.py
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── me
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── me_delete_repository.py
│   │   │   │       │   │   ├── me_read_repository.py
│   │   │   │       │   │   └── me_update_repository.py
│   │   │   │       │   ├── payment
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── payment_creation_repository.py
│   │   │   │       │   │   └── payment_read_repository.py
│   │   │   │       │   ├── payment_intent
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── payemnt_intent_read_repository.py
│   │   │   │       │   │   ├── payment_intent_creation_repository.py
│   │   │   │       │   │   └── payment_intent_update_repository.py
│   │   │   │       │   ├── session
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── session_creation_repository.py
│   │   │   │       │   │   ├── session_read_repository.py
│   │   │   │       │   │   └── session_update_repository.py
│   │   │   │       │   ├── session_attendance
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── session_attendance_creation_repository.py
│   │   │   │       │   │   └── session_attendance_read_repository.py
│   │   │   │       │   └── session_participation
│   │   │   │       │       ├── __init__.py
│   │   │   │       │       ├── session_participation_creation_repository.py
│   │   │   │       │       ├── session_participation_read_repository.py
│   │   │   │       │       └── session_participation_update_repository.py
│   │   │   │       ├── sessions.py
│   │   │   │       └── uow
│   │   │   │           ├── admin
│   │   │   │           │   ├── credit
│   │   │   │           │   │   └── admin_credit_uow.py
│   │   │   │           │   ├── __init__.py
│   │   │   │           │   ├── payment
│   │   │   │           │   │   └── admin_payment_uow.py
│   │   │   │           │   ├── session
│   │   │   │           │   │   ├── admin_session_system_uow.py
│   │   │   │           │   │   └── admin_session_uow.py
│   │   │   │           │   └── users
│   │   │   │           │       ├── admin_user_system_uow.py
│   │   │   │           │       └── admin_user_uow.py
│   │   │   │           ├── auth
│   │   │   │           │   ├── auth_uow.py
│   │   │   │           │   └── __init__.py
│   │   │   │           ├── coach
│   │   │   │           │   └── coach_uow.py
│   │   │   │           ├── credit
│   │   │   │           │   └── credit_uow.py
│   │   │   │           ├── me
│   │   │   │           │   ├── __init__.py
│   │   │   │           │   ├── me_system_uow.py
│   │   │   │           │   └── me_uow.py
│   │   │   │           ├── payment
│   │   │   │           │   └── payment_uow.py
│   │   │   │           ├── session
│   │   │   │           │   ├── __init__.py
│   │   │   │           │   ├── session_public_uow.py
│   │   │   │           │   └── session_uow.py
│   │   │   │           └── stripe
│   │   │   │               └── stripe_uow.py
│   │   │   ├── __pycache__
│   │   │   │   └── __init__.cpython-314.pyc
│   │   │   ├── security
│   │   │   │   ├── in_memory
│   │   │   │   │   ├── jwt.py
│   │   │   │   │   ├── password_hasher.py
│   │   │   │   │   ├── provider.py
│   │   │   │   │   ├── __pycache__
│   │   │   │   │   │   ├── jwt.cpython-314.pyc
│   │   │   │   │   │   ├── password_hasher.cpython-314.pyc
│   │   │   │   │   │   ├── refresh_token_generator.cpython-314.pyc
│   │   │   │   │   │   └── token_hasher.cpython-314.pyc
│   │   │   │   │   ├── refresh_token_generator.py
│   │   │   │   │   └── token_hasher.py
│   │   │   │   ├── jwt.py
│   │   │   │   ├── password_hasher.py
│   │   │   │   ├── provider.py
│   │   │   │   ├── refresh_token_generator.py
│   │   │   │   └── token_hasher.py
│   │   │   └── settings
│   │   │       ├── app_settings.py
│   │   │       ├── __init__.py
│   │   │       └── provider.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-314.pyc
│   │   └── shared
│   │       ├── database
│   │       │   └── sqlstate_extractor.py
│   │       ├── exceptions
│   │       │   ├── commons.py
│   │       │   └── runtime.py
│   │       ├── handlers
│   │       │   ├── auth_exception_handler.py
│   │       │   ├── common_exception_handler.py
│   │       │   ├── credit_exception_handler.py
│   │       │   ├── currency_exception_handler.py
│   │       │   ├── __init__.py
│   │       │   ├── payment_exception_handler.py
│   │       │   ├── payment_intent_exception_handler.py
│   │       │   ├── session_exception_handler.py
│   │       │   └── stripe_exception_handler.py
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   └── __init__.cpython-314.pyc
│   │       ├── rules
│   │       │   ├── currency_rules.py
│   │       │   ├── email_rules.py
│   │       │   ├── password_rules.py
│   │       │   ├── refresh_token_rules.py
│   │       │   ├── session_title_rules.py
│   │       │   └── user_profile_rules.py
│   │       ├── security
│   │       │   ├── jwt_port.py
│   │       │   ├── password_hasher_port.py
│   │       │   ├── __pycache__
│   │       │   │   ├── jwt_port.cpython-314.pyc
│   │       │   │   ├── password_hasher_port.cpython-314.pyc
│   │       │   │   ├── refresh_token_generator_port.cpython-314.pyc
│   │       │   │   └── token_hasher_port.cpython-314.pyc
│   │       │   ├── token_generator_port.py
│   │       │   └── token_hasher_port.py
│   │       └── utils
│   │           ├── __pycache__
│   │           │   └── time.cpython-314.pyc
│   │           ├── string_predicate.py
│   │           └── time.py
│   ├── Dockerfile
│   ├── package-lock.json
│   ├── requirements.txt
│   └── tests
│       └── auth
│           ├── login_test.py
│           └── __pycache__
│               └── login_test.cpython-314-pytest-8.1.1.pyc
├── db
│   ├── 00_bootstrap
│   │   ├── 00_01_app_user_role.sql
│   │   ├── 00_02_app_admin_role.sql
│   │   └── 00_03_app_system_role.sql
│   ├── 01_tables
│   │   ├── 01_01_bootstrap.sql
│   │   ├── 01_02_permissions.sql
│   │   ├── 01_03_extensions.sql
│   │   ├── 01_04_users.sql
│   │   ├── 01_05_user_profiles.sql
│   │   ├── 01_06_roles.sql
│   │   ├── 01_07_users_roles.sql
│   │   ├── 01_08_sessions.sql
│   │   ├── 01_09_payment_intent.sql
│   │   ├── 01_10_refresh_tokens.sql
│   │   ├── 01_11_invite_tokens.sql
│   │   ├── 01_12_session_participation.sql
│   │   ├── 01_13_session_attendance.sql
│   │   ├── 01_14_payments.sql
│   │   ├── 01_15_credit_ledger.sql
│   │   ├── 01_16_coach_stripe_accounts.sql
│   │   ├── 01_17_event.sql
│   │   └── 01_18_transfering_ownership_to_app_admin.sql
│   ├── 02_functions
│   │   ├── 02_01_predicate.sql
│   │   ├── 02_02_auth_functions.sql
│   │   ├── 02_03_me_functions.sql
│   │   ├── 02_04_admin_user_functions.sql
│   │   ├── 02_05_session_predicate.sql
│   │   ├── 02_06_session_functions.sql
│   │   ├── 02_07_attendance_predicate.sql
│   │   ├── 02_08_session_attendance_function.sql
│   │   ├── 02_09_session_participation_predicate.sql
│   │   ├── 02_10_session_participation_functions.sql
│   │   ├── 02_11_credit_ledger_functions.sql
│   │   ├── 02_12_payment_intent_predicate.sql
│   │   ├── 02_13_payment_intent_functions.sql
│   │   ├── 02_14_payment_predicate.sql
│   │   ├── 02_15_payment_functions.sql
│   │   ├── 02_16_coach_stripe_account_predicate.sql
│   │   └── 02_17_coach_stripe_account_functions.sql
│   ├── 03_views
│   │   └── 03_01_public_coach_profiles_view.sql
│   ├── 04_row_level_security
│   │   ├── 04_01_users_row_level_security.sql
│   │   ├── 04_02_user_profiles_row_level_security.sql
│   │   ├── 04_03_user_roles_row_level_security.sql
│   │   ├── 04_04_payment_intent_row_level_security.sql
│   │   ├── 04_05_refresh_tokens_row_level_security.sql
│   │   ├── 04_06_session_participation_row_level_security.sql
│   │   ├── 04_07_session_attendance_row_level_security.sql
│   │   ├── 04_08_credit_ledger_row_level_security.sql
│   │   ├── 04_09_payment_row_level_security.sql
│   │   └── 04_10_coach_stripe_accounts_row_level_security.sql
│   ├── 05_permissions
│   │   ├── 05_01_users_permission.sql
│   │   ├── 05_02_user_profiles_permissions.sql
│   │   ├── 05_03_roles_permissions.sql
│   │   ├── 05_04_user_roles_permissions.sql
│   │   ├── 05_05_sessions_permissions.sql
│   │   ├── 05_06_payment_intents_permissions.sql
│   │   ├── 05_07_refresh_tokens_permissions.sql
│   │   ├── 05_08_invite_tokens_permissions.sql
│   │   ├── 05_09_session_participation_permissions.sql
│   │   ├── 05_10_session_attendance_permissions.sql
│   │   ├── 05_11_credit_ledger_permissions.sql
│   │   ├── 05_12_payment_permissions.sql
│   │   ├── 05_13_event_permissions.sql
│   │   └── 05_14_public_coach_view_permissions.sql
│   ├── 06_indexes
│   │   ├── 06_01_users_indexes.sql
│   │   ├── 06_02_user_profiles_indexes.sql
│   │   ├── 06_03_user_roles_indexes.sql
│   │   ├── 06_04_sessions_indexes.sql
│   │   ├── 06_05_payment_intents_indexes.sql
│   │   ├── 06_06_refresh_tokens_indexes.sql
│   │   ├── 06_07_invite_tokens_indexes.sql
│   │   ├── 06_08_session_participation_indexes.sql
│   │   ├── 06_09_session_attendance_indexes.sql
│   │   ├── 06_10_credit_ledger_indexes.sql
│   │   └── 06_11_payment_indexes.sql
│   ├── 07_triggers
│   │   ├── 07_01_users_triggers.sql
│   │   ├── 07_02_user_profiles_triggers.sql
│   │   ├── 07_03_sessions_triggers.sql
│   │   ├── 07_04_payment_intents_triggers.sql
│   │   ├── 07_05_refresh_tokens_triggers.sql
│   │   ├── 07_06_invite_tokens_triggers.sql
│   │   ├── 07_07_session_participation_triggers.sql
│   │   ├── 07_08_session_attendance_triggers.sql
│   │   ├── 07_09_credit_ledger_triggers.sql
│   │   ├── 07_10_payment_triggers.sql
│   │   ├── 07_11_coach_stripe_accounts_triggers.sql
│   │   └── 07_12_event.sql
│   ├── 08_seeds
│   │   ├── 08_01_roles_seed.sql
│   │   └── 08_02_admin_seed.sql
│   ├── 09_dev_seeds
│   │   ├── 09_01_coach_seed.sql
│   │   └── README.md
│   ├── init-scripts
│   │   ├── 00_01_app_user_role.sql
│   │   ├── 00_02_app_admin_role.sql
│   │   ├── 00_03_app_system_role.sql
│   │   ├── 01_01_bootstrap.sql
│   │   ├── 01_02_permissions.sql
│   │   ├── 01_03_extensions.sql
│   │   ├── 01_04_users.sql
│   │   ├── 01_05_user_profiles.sql
│   │   ├── 01_06_roles.sql
│   │   ├── 01_07_users_roles.sql
│   │   ├── 01_08_sessions.sql
│   │   ├── 01_09_payment_intent.sql
│   │   ├── 01_10_refresh_tokens.sql
│   │   ├── 01_11_invite_tokens.sql
│   │   ├── 01_12_session_participation.sql
│   │   ├── 01_13_session_attendance.sql
│   │   ├── 01_14_payments.sql
│   │   ├── 01_15_credit_ledger.sql
│   │   ├── 01_16_coach_stripe_accounts.sql
│   │   ├── 01_17_event.sql
│   │   ├── 01_18_transfering_ownership_to_app_admin.sql
│   │   ├── 02_01_predicate.sql
│   │   ├── 02_02_auth_functions.sql
│   │   ├── 02_03_me_functions.sql
│   │   ├── 02_04_admin_user_functions.sql
│   │   ├── 02_05_session_predicate.sql
│   │   ├── 02_06_session_functions.sql
│   │   ├── 02_07_attendance_predicate.sql
│   │   ├── 02_08_session_attendance_function.sql
│   │   ├── 02_09_session_participation_predicate.sql
│   │   ├── 02_10_session_participation_functions.sql
│   │   ├── 02_11_credit_ledger_functionssql.sql
│   │   ├── 02_12_payment_intent_predicate.sql
│   │   ├── 02_13_payment_intent_functions.sql
│   │   ├── 02_14_payment_predicate.sql
│   │   ├── 02_15_payment_functions.sql
│   │   ├── 02_16_coach_stripe_account_predicate.sql
│   │   ├── 02_17_coach_stripe_account_functions.sql
│   │   ├── 03_01_public_coach_profiles_view.sql
│   │   ├── 04_01_users_row_level_security.sql
│   │   ├── 04_02_user_profiles_row_level_security.sql
│   │   ├── 04_03_user_roles_row_level_security.sql
│   │   ├── 04_04_payment_intent_row_level_security.sql
│   │   ├── 04_05_refresh_tokens_row_level_security.sql
│   │   ├── 04_06_session_participation_row_level_security.sql
│   │   ├── 04_07_session_attendance_row_level_security.sql
│   │   ├── 04_08_credit_ledger_row_level_security.sql
│   │   ├── 04_09_payment_row_level_security.sql
│   │   ├── 04_10_coach_stripe_accounts_row_level_security.sql
│   │   ├── 05_01_users_permission.sql
│   │   ├── 05_02_user_profiles_permissions.sql
│   │   ├── 05_03_roles_permissions.sql
│   │   ├── 05_04_user_roles_permissions.sql
│   │   ├── 05_05_sessions_permissions.sql
│   │   ├── 05_06_payment_intents_permissions.sql
│   │   ├── 05_07_refresh_tokens_permissions.sql
│   │   ├── 05_08_invite_tokens_permissions.sql
│   │   ├── 05_09_session_participation_permissions.sql
│   │   ├── 05_10_session_attendance_permissions.sql
│   │   ├── 05_11_credit_ledger_permissions.sql
│   │   ├── 05_12_payment_permissions.sql
│   │   ├── 05_13_event_permissions.sql
│   │   ├── 05_14_public_coach_view_permissions.sql
│   │   ├── 06_01_users_indexes.sql
│   │   ├── 06_02_user_profiles_indexes.sql
│   │   ├── 06_03_user_roles_indexes.sql
│   │   ├── 06_04_sessions_indexes.sql
│   │   ├── 06_05_payment_intents_indexes.sql
│   │   ├── 06_06_refresh_tokens_indexes.sql
│   │   ├── 06_07_invite_tokens_indexes.sql
│   │   ├── 06_08_session_participation_indexes.sql
│   │   ├── 06_09_session_attendance_indexes.sql
│   │   ├── 06_10_credit_ledger_indexes.sql
│   │   ├── 06_11_payment_indexes.sql
│   │   ├── 07_01_users_triggers.sql
│   │   ├── 07_02_user_profiles_triggers.sql
│   │   ├── 07_03_sessions_triggers.sql
│   │   ├── 07_04_payment_intents_triggers.sql
│   │   ├── 07_05_refresh_tokens_triggers.sql
│   │   ├── 07_06_invite_tokens_triggers.sql
│   │   ├── 07_07_session_participation_triggers.sql
│   │   ├── 07_08_session_attendance_triggers.sql
│   │   ├── 07_09_credit_ledger_triggers.sql
│   │   ├── 07_10_payment_triggers.sql
│   │   ├── 07_11_coach_stripe_accounts_triggers.sql
│   │   ├── 07_12_event.sql
│   │   ├── 08_01_roles_seed.sql
│   │   ├── 08_02_admin_seed.sql
│   │   └── 09_01_coach_seed.sql
│   ├── postgre_sql_error_codes.md
│   └── README.md
├── doc
│   ├── Stage-1-report.md
│   ├── stage-2.png
│   ├── stage-3
│   │   ├── Diagram
│   │   ├── diagram.png
│   │   ├── Diagram.png
│   │   ├── mockups
│   │   ├── plant_uml
│   │   │   ├── authentication_sequence.png
│   │   │   ├── authentication_sequence.puml
│   │   │   ├── class_diagram.png
│   │   │   ├── class_diagram.puml
│   │   │   ├── component_diagram.png
│   │   │   ├── component_diagram.puml
│   │   │   ├── registration_sequence.png
│   │   │   └── registration_sequence.puml
│   │   ├── SCM
│   │   ├── stage3_ER_diagram.png
│   │   └── User
│   └── stage3-technical-documentation.md
├── docker-compose.yaml
├── frontend
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── nginx.conf
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   ├── src
│   │   ├── app.d.ts
│   │   ├── app.html
│   │   ├── config.ts
│   │   ├── lib
│   │   │   ├── api
│   │   │   │   ├── admin.api.ts
│   │   │   │   ├── auth.api.ts
│   │   │   │   ├── client.ts
│   │   │   │   └── sessions.api.ts
│   │   │   ├── assets
│   │   │   │   └── favicon.svg
│   │   │   ├── client.ts
│   │   │   ├── config.ts
│   │   │   ├── index.ts
│   │   │   ├── stores
│   │   │   │   ├── auth.store.ts
│   │   │   │   └── session.store.ts
│   │   │   └── types
│   │   │       └── session.ts
│   │   └── routes
│   │       ├── dashboard
│   │       │   ├── admin
│   │       │   │   ├── new-session
│   │       │   │   │   └── +page.svelte
│   │       │   │   ├── +page.svelte
│   │       │   │   └── users
│   │       │   │       └── +page.svelte
│   │       │   ├── coach
│   │       │   │   └── +page.svelte
│   │       │   ├── +layout.svelte
│   │       │   ├── +page.svelte
│   │       │   └── user
│   │       │       └── +page.svelte
│   │       ├── +layout.svelte
│   │       ├── login
│   │       │   └── +page.svelte
│   │       ├── +page.svelte
│   │       └── sessions
│   │           ├── create
│   │           │   └── +page.svelte
│   │           ├── [id]
│   │           │   ├── +page.svelte
│   │           │   └── participants
│   │           │       └── +page.svelte
│   │           └── +page.svelte
│   ├── static
│   │   └── robots.txt
│   ├── svelte.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
└── README.md
```

</details>

## 🔧 What's next?

- Working on missing features:
 	- displaying of payment and credit info for the user
 	- displaying of payment and credit info for the admin
 	- displaying of payment info for the coach
 	- adding proper invite links

## 👷 Authors

- Adel, Mejrissi [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adel-mejrissi-709374172/), [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AdelMej)
- Daniel Ramirez [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](), [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)]()
