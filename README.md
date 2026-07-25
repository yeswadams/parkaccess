# Parking & Vehicle Access Management System (PVAMS)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![ORM](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![Serialization](https://img.shields.io/badge/schema-Marshmallow-orange.svg)](https://marshmallow.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An open-source, multi-court estate security and parking management solution engineered to solve vehicle tracking, access verification, blocking incident resolutions, and estate movement analytics.

---

## Table of Contents
- [1. Executive Summary & Core Rationale](#1-executive-summary--core-rationale)
- [2. Architectural & System Architecture](#2-architectural--system-architecture)
- [3. Domain Data Model & ERD Rationale](#3-domain-data-model--erd-rationale)
- [4. Tech Stack & Software Architecture](#4-tech-stack--software-architecture)
- [5. Database Schema & Data Dictionary](#5-database-schema--data-dictionary)
- [6. API Blueprint & Endpoints](#6-api-blueprint--endpoints)
- [7. Known Simplifications & Architectural Tradeoffs](#7-known-simplifications--architectural-tradeoffs)
- [8. Developer Setup & Installation Guide](#8-developer-setup--installation-guide)
- [9. Contribution Guidelines](#9-contribution-guidelines)
- [10. Roadmap & Future Scope](#10-roadmap--future-scope)
- [11. License](#11-license)

---

## 1. Executive Summary & Core Rationale

In multi-court residential estates, traditional paper-based and siloed security management systems create severe operational friction:
1. **Redundant Registrations**: Visitors and residents are required to re-register at every inner checkpoint or court gate after already passing through the main perimeter gate.
2. **Blocking Vehicle Deadlocks**: When a vehicle is parked illegitimately or blocks another vehicle, security personnel struggle to instantly identify and contact the vehicle owner, leading to manual paper-ledger searches and physical escalations.

### Core Schema Solutions
The **Parking & Vehicle Access Management System (PVAMS)** directly attacks these pain points through two core domain design decisions:

* **Single Source of Truth (`vehicles` table)**: Keyed by a uniquely indexed `plate_number`, vehicle records are created **once** at the main perimeter gate. Every downstream table references `vehicle_id`. Court-level security checkpoints perform lookup operations (`checkpoint_logs`) rather than re-registering vehicles.
* **First-Class Blocking Modeling (`blocking_incidents` table)**: Blocking events explicitly capture the relation between a `blocked_vehicle_id` and a `blocker_vehicle_id`. Finding a blocking owner is reduced from manual searching to a single indexed lookup:
  $$	ext{plate\_number} \longrightarrow 	ext{vehicle\_id} \longrightarrow 	ext{owner\_contact}$$

---

## 2. Architectural & System Architecture

```
                                  +-----------------------+
                                  |   Main Perimeter Gate  |
                                  | (checkpoint.type='main')|
                                  +-----------+-----------+
                                              |
                                     Registers / Verifies
                                              |
                                              v
                                  +-----------------------+
                                  |    `vehicles` Table   |
                                  | (Single Source Truth) |
                                  +-----------+-----------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        |   Court A Checkpoint    |                       |   Court B Checkpoint    |
        | (checkpoint.type='court')|                       | (checkpoint.type='court')|
        +------------+------------+                       +------------+------------+
                     |                                                 |
             Log Pass / Lookup                                 Log Pass / Lookup
                     |                                                 |
                     +------------------------+------------------------+
                                              |
                                              v
                                  +-----------------------+
                                  |   `parking_records`   |
                                  |  (Occupancy & Slots)  |
                                  +-----------+-----------+
                                              |
                                    Triggers Incident on
                                       Blocking Event
                                              |
                                              v
                                  +-----------------------+
                                  | `blocking_incidents`  |
                                  +-----------+-----------+
                                              |
                                    Dispatches Notifications
                                              |
                                              v
                                  +-----------------------+
                                  |    `notifications`    |
                                  |  (SMS / Call / Push)  |
                                  +-----------------------+
```

---

## 3. Domain Data Model & ERD Rationale

### Entity Breakdown & Justifications

| Entity | Domain Reasoning & Rationale |
| :--- | :--- |
| `estates` $
ightarrow$ `courts` $
ightarrow$ `checkpoints` | Mirrors physical hierarchy. Enables distinguishing main gates (`checkpoint.type = 'main_gate'`) from court gates (`checkpoint.type = 'court_gate'`) dynamically without separate application logic. |
| `residents` vs. `visitors` | **Residents** are permanent, associated with units; **Visitors** are transient and tied to host residents (`host_resident_id`). Splitting prevents nullable fields across a generic table and enforces guest accountability. |
| `vehicles.owner_resident_id` / `owner_visitor_id` | Enforces ownership. Exactly one FK is set per vehicle record, bypassing complex polymorphic structures while ensuring integrity. |
| `checkpoint_logs` vs. `parking_records` | **`checkpoint_logs`** monitors access flow (gate passages). **`parking_records`** tracks spatial state (current parking position). Separating them optimizes spatial dashboard queries. |
| `blocking_incidents` $
ightarrow$ `parking_records` | Links blocking events to spatial location and slot IDs. Enables historical reporting on recurring bottleneck zones across estate courts. |
| `notifications` (Decoupled 1-to-Many) | Outbound communication (SMS, automated voice calls, push) is asynchronous and subject to carrier failures. Decoupling allows retry queues and channel escalation (SMS $
ightarrow$ Call $
ightarrow$ Push). |
| `movement_history` (Flattened Log) | Purely optimized for dashboard performance. Avoids dynamic 5-table joins across high-throughput telemetry data at MVP scale. |
| `parking_slots` (Optional) | Supports strict assigned-slot estates and flexible unmapped-lot estates via `location_description` fallbacks. |

---

## 4. Tech Stack & Software Architecture

* **Backend Language**: Python 3.10+
* **Web Framework**: Flask
* **Database ORM**: Flask-SQLAlchemy (SQLAlchemy 2.0+)
* **Serialization/Validation**: Flask-Marshmallow / Marshmallow-SQLAlchemy
* **Database Engine**: PostgreSQL (Production) / SQLite (Local Dev & Testing)
* **Migrations**: Flask-Migrate (Alembic)

### Folder Structure
```
pvams/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── estate.py
│   │   ├── user.py
│   │   ├── vehicle.py
│   │   ├── parking.py
│   │   └── incident.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── vehicle_schema.py
│   │   ├── parking_schema.py
│   │   └── incident_schema.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── checkpoints.py
│   │   ├── vehicles.py
│   │   ├── parking.py
│   │   └── incidents.py
│   └── services/
│       ├── notification_service.py
│       └── movement_logger.py
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

## 5. Database Schema & Data Dictionary

### Key Tables & Field Specification

#### 1. `estates`, `courts`, `checkpoints`
* `estates`: `id` (PK, UUID), `name` (String(100)), `created_at` (Timestamp)
* `courts`: `id` (PK, UUID), `estate_id` (FK -> estates.id), `name` (String(100))
* `checkpoints`: `id` (PK, UUID), `court_id` (FK -> courts.id, Nullable), `estate_id` (FK -> estates.id), `name` (String(100)), `type` (Enum: `'main_gate'`, `'court_gate'`)

#### 2. `residents` & `visitors`
* `residents`: `id` (PK, UUID), `full_name` (String(100)), `phone_number` (String(20), Indexed), `unit_number` (String(20)), `created_at` (Timestamp)
* `visitors`: `id` (PK, UUID), `full_name` (String(100)), `phone_number` (String(20), Indexed), `host_resident_id` (FK -> residents.id), `expected_departure` (Timestamp)

#### 3. `vehicles`
* `id` (PK, UUID)
* `plate_number` (String(15), Unique, Indexed)
* `model` (String(50))
* `color` (String(30))
* `owner_resident_id` (FK -> residents.id, Nullable)
* `owner_visitor_id` (FK -> visitors.id, Nullable)
* `created_at` (Timestamp)

#### 4. `checkpoint_logs`
* `id` (PK, UUID)
* `checkpoint_id` (FK -> checkpoints.id)
* `vehicle_id` (FK -> vehicles.id)
* `entry_time` (Timestamp)
* `logged_by_user_id` (FK -> users.id)

#### 5. `parking_slots` & `parking_records`
* `parking_slots`: `id` (PK, UUID), `court_id` (FK -> courts.id), `slot_number` (String(20)), `is_occupied` (Boolean, Default: False)
* `parking_records`: `id` (PK, UUID), `vehicle_id` (FK -> vehicles.id), `parking_slot_id` (FK -> parking_slots.id, Nullable), `location_description` (String(255), Nullable), `parked_at` (Timestamp), `exited_at` (Timestamp, Nullable), `status` (Enum: `'parked'`, `'cleared'`, `'blocked'`)

#### 6. `blocking_incidents`
* `id` (PK, UUID)
* `parking_record_id` (FK -> parking_records.id)
* `blocked_vehicle_id` (FK -> vehicles.id)
* `blocker_vehicle_id` (FK -> vehicles.id)
* `reported_at` (Timestamp)
* `resolved_at` (Timestamp, Nullable)
* `status` (Enum: `'active'`, `'notified'`, `'resolved'`)

#### 7. `notifications`
* `id` (PK, UUID)
* `incident_id` (FK -> blocking_incidents.id)
* `recipient_phone` (String(20))
* `channel` (Enum: `'SMS'`, `'CALL'`, `'IN_APP'`)
* `delivery_status` (Enum: `'pending'`, `'sent'`, `'failed'`)
* `sent_at` (Timestamp)

#### 8. `movement_history`
* `id` (PK, UUID)
* `vehicle_id` (FK -> vehicles.id)
* `plate_number` (String(15))
* `event_type` (String(50))
* `location_name` (String(100))
* `timestamp` (Timestamp)

---

## 6. API Blueprint & Endpoints

### 1. Vehicle Verification & Main Gate Registration
`POST /api/v1/vehicles/check-in`
* **Request Body**:
  ```json
  {
    "plate_number": "KDA-123X",
    "checkpoint_id": "uuid-main-gate-01",
    "vehicle_details": {
      "model": "Toyota RAV4",
      "color": "Silver"
    },
    "owner_type": "visitor",
    "visitor_details": {
      "full_name": "Jane Doe",
      "phone_number": "+254712345678",
      "host_resident_id": "uuid-resident-88"
    }
  }
  ```
* **Behavior**: Checks if `plate_number` exists. If yes, logs `checkpoint_logs` entry. If no, creates `vehicles` and `visitors` record before logging entry.

### 2. Vehicle Search by License Plate
`GET /api/v1/vehicles/lookup?plate_number=KDA-123X`
* **Response**:
  ```json
  {
    "vehicle_id": "uuid-vehicle-01",
    "plate_number": "KDA-123X",
    "model": "Toyota RAV4",
    "color": "Silver",
    "owner": {
      "type": "visitor",
      "name": "Jane Doe",
      "phone": "+254712345678",
      "host_unit": "Court B - Unit 4"
    },
    "current_status": "parked",
    "current_location": "Court B - Slot 12"
  }
  ```

### 3. Log Blocking Incident
`POST /api/v1/incidents/blocking`
* **Request Body**:
  ```json
  {
    "blocked_plate": "KDA-123X",
    "blocker_plate": "KBB-999Z",
    "parking_record_id": "uuid-parking-44"
  }
  ```
* **Behavior**: Instantly creates `blocking_incidents` record, fetches owner contact for `blocker_plate`, and triggers a dispatch to `notifications`.

---

## 7. Known Simplifications & Architectural Tradeoffs

Contributors and evaluators should note the following intentional tradeoffs made for MVP scope:

1. **Explicit Dual Nullable FKs vs. Polymorphic Relations**:
   * *Tradeoff*: `vehicles` uses `owner_resident_id` and `owner_visitor_id` instead of a polymorphic table target.
   * *Rationale*: Avoids complex ORM queries while maintaining strict foreign key constraints at the database level for MVP simplicity.
2. **Denormalized `movement_history`**:
   * *Tradeoff*: Duplicates data derivable from `checkpoint_logs` and `parking_records`.
   * *Rationale*: Speeds up security dashboard audit trails by turning dynamic multi-table joins into single table reads.
3. **Flat Role Strings (`users.role`)**:
   * *Tradeoff*: Uses flat strings (e.g., `'guard'`, `'admin'`) instead of full RBAC models (`roles`, `permissions`, `user_roles`).
   * *Rationale*: Sufficient for single-tier security guard access during MVP deployment.

---

## 8. Developer Setup & Installation Guide

### Prerequisites
* Python 3.10 or higher
* PostgreSQL (or SQLite for quick testing)
* Git

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-org/pvams.git
   cd pvams
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@localhost:5432/pvams_db
   ```

5. **Initialize Database Migrations**:
   ```bash
   flask db upgrade
   ```

6. **Seed Initial Data (Optional)**:
   ```bash
   python seed.py
   ```

7. **Run Application**:
   ```bash
   flask run
   ```

---

## 9. Contribution Guidelines

We welcome open-source contributions! To keep code clean and maintainable, follow these steps:

1. **Fork & Branch**: Create a feature branch off `main` (`git checkout -b feature/amazing-feature`).
2. **Code Style**: Adhere to PEP 8 standard formatting.
3. **Marshmallow Schemas**: Ensure all new API endpoints utilize Marshmallow schemas for input validation and output serialization.
4. **Testing**: Write unit tests for new API blueprints or model methods in `tests/`. Run tests via:
   ```bash
   pytest
   ```
5. **Pull Request**: Open a PR against `main` describing your changes and referencing related issues.

---

## 10. Roadmap & Future Scope

* [ ] Implement full Role-Based Access Control (RBAC) tables.
* [ ] Integrate Twilio / SMS Gateway for real-time dispatching.
* [ ] Add License Plate Recognition (ANPR / LPR) camera integration.
* [ ] Support Resident Mobile App notifications via WebSockets / Firebase Cloud Messaging.

---

## 11. License

Distributed under the MIT License. See `LICENSE` for more information.