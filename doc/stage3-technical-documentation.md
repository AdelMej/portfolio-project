# Technical documentation

## Overview

This document contains the technical documentation for this project:
- User stories
- Architecture diagram
- Wireframe
- Mockup
- UML Diagrams (sequence, component, class)
- API specifications
- SCM and QA strategies


## Summary
- [User stories](#user-stories-moscow-prioritization)
- [Architecture diagram](#architecture-diagram)
- [Wireframe]()
- [Mockup]()
- [UML diagrams]()
 - [Component diagram]()
 - [Class diagram]()
 - [Sequence diagrams]()
- [API specifications]()
- [SCS and QA strategies]()


## User stories (MoSCoW Prioritization)

### Must have (MVP)

#### User
As a user, I want to create an account and log in, so that I can access the gym platform.
As a user, I want to view available gym sessions, so that I can choose a session that fits my schedule.
As a user, I want to subscribe to a gym session, so that I can participate in it.
As a user, I want to pay for a gym session online, so that my subscription is confirmed.

#### Coach
As a coach, I want to create gym sessions, so that users can subscribe to them.
As a coach, I want to define the maximum number of participants per session, so that sessions are not overbooked.

#### Administrator
As an administrator, I want to manage users, coaches, and sessions, so that the platform remains organized and functional.
As an administrator, I want to view session subscriptions, so that I can monitor gym usage.

### Should have

As a coach, I want to view the list of subscribed users, so that I can prepare my sessions.
As a human resources manager, I want to generate an attendance list for each session, so that I can track employee participation.
As a user, I want to view my subscribed sessions, so that I can manage my gym schedule.

### Could have

As a user, I want to leave a review for a gym session, so that I can provide feedback to the coach.

### Won’t Have (Out of scope for MVP)

As a user, I want to receive personalized session recommendations, so that I can discover new workouts.
As a user, I want to receive push notifications, so that I am reminded of upcoming sessions.

---

## Architecture diagram

![Architecture diagram](./stage-3/Diagram.png)

### Front-end (Svelte)

The web application communicates with the backend API using secure HTTPS requests. It allows users to browse sessions, register, and perform payments.

### Backend API (FastAPI)

This is the core of the application. It handles the main business logic through two modules:
 - Auth, Session and Registration → manages user authentication, sessions, and user registrations.
 - Session Management → handles session creation, availability, and attendance validation.

### Database (PostgreSQL & NoSQL)

PostgreSQL stores structured data such as users, sessions, registrations, and payment status.
The NoSQL database is used for logs and activity tracking.
Only the backend API accesses the databases.

### Stripe (Payments)

Stripe is used as an external payment service. The backend sends payment requests to Stripe, and Stripe sends webhooks back to the API to confirm payment results.
