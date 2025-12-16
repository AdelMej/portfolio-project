# Stage 1 report

## Roles

- Daniel frontend developer, UI designer, UX designer, agile developer
  - strength in frontend design and architecture
  - skilled in HTML, CSS

- Adel backend developer, agile developer, project manager
  - strength in backend development
  - good with object oriented programming concepts

## Communication and collaboration media

- Discord, Jira

## Stackholders

- Emilie Office manager, app client, feedback and administrator
  - manage accounts
  - gives rights to the coach to plan sessions
- Maëva Executive Assistant, app client, feedback and administrator
  - help manage accounts
  - manage payments

## Project ideas

Web app for managing access to Actual digital gym:

- coach access and scheduling
- user access and subscription
- payment system
- administrator access
- attendance list for human resources

Kessia, a platform for medical writing

- connection between researchers and writers
- airbnb styling for scientific writing
- automatically generate contracts
- payment for the contract
- review system

“How Might We” Questions:

- How might we simplify gym scheduling for human resources?
- How might we integrate payment and payment options?
- How might we handle gym session management for coaches?

## Priorities

- potential impact
  - Less management needs for the administrators
  - Easier access to the gym via subscription
  - Convenience for the coach and human resources

- scalability
  - Internal app so low scalability needs
  - aiming at handling hundreds of request per second
  - server or small app need for defining db needs

- Technical alignment
  - SQL because clear relational structures present with users and sessions
  - Python FastAPI because experience in Python and object oriented programming concepts
  - HTML 5, CSS, JavaScript classic frontend stack framework not yet chosen because of lack of experience
  - Stripe because of availability, payment options and popularity

- Risks
  - no experience with frameworks
  - no experience with Stripe
  - tech choice define development speed
  - no prior knowledge on the database

---

- MVP 🔴 → Mandatory task to make the site functional.
- Important 🟡 → For a better experience for the client.
- Future 🔵 → Improve the future roadmap and scaling the website.

| Feature  |  Notes  | Feasibility   | Risks   | Priorities  |
|---|---|---|---|---|
| user access + session subscription |  User subscription to any available gym session | 5/5  | None  | 🔴 |
| user payment  | Payment option for each session  | 3/5  | Must learn payment technologies and options  | 🔴 |
| coach session creation and management  | Coaches can create session, their content and number of participant  | 4/5  | administration and coach scope can overlap  | 🔴  |
| generating attendance lists | Human resource want an attendance list for each session | 5/5 | None | 🟡 |
| administration of users, session and coaches | management of all moving parts of the app | 3/5 | high complexity must manage 3 tables at once and payment | 🔴  |
| user review| user can review each session | 5/5 | out of scope | 🔵  |

## Final MVP decision: Actual digital gym management website

The Actual digital gym app project solve management time concerns make scheduling and subscription easier for the user

### Goals

Web app for handling gym subscription attendance
coach can create and handle gym session
administrator panel for the app
payment solution for user subscription

### Targeted audience

Company workers, internal tool

### Project scope

- users can subscribe and pay for a gym session
- coach can create session
- administrator can have access to session and users
