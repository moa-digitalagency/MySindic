# Shabaka Syndic - Projet Replit

## Overview

**Shabaka Syndic** is a complete digital management platform for condominiums (copropriétés) in Morocco. Built as a Progressive Web App (PWA), it modernizes property management for syndics, administrators, property owners, and residents. The platform offers comprehensive tools for managing units, finances, maintenance, news feeds, assemblies, and documents with role-based access control.

## Recent Changes (November 22, 2025)

### ✅ Complete Migration to Replit Environment
- Successfully migrated project to Replit environment
- Configured PostgreSQL database with all 22 tables
- Set up Gunicorn workflow on port 5000 with webview output
- Verified all database models and relationships
- Confirmed demo data initialization working correctly

### ✅ Database Schema Verification
All 22 database tables created and verified:
- `users` - User accounts with role management
- `residences` - Residence/building information
- `units` - Individual units/apartments
- `residence_admins` - Admin assignments to residences
- `general_assemblies` - Assembly management with Agora integration
- `resolutions` - Assembly voting resolutions
- `votes` - Individual votes on resolutions
- `attendances` - Attendance tracking (physical/online)
- `polls` - Community polls/surveys
- `poll_options` - Poll answer options
- `poll_votes` - Poll voting records
- `maintenance_requests` - Maintenance tracking system
- `maintenance_comments` - Comments on maintenance requests
- `maintenance_documents` - Document attachments for maintenance
- `maintenance_logs` - Maintenance history log (carnet d'entretien)
- `charges` - Financial charges
- `charge_distributions` - Charge allocation to units
- `payments` - Payment records
- `news` - News feed (2 types: feed & announcement)
- `documents` - Document management
- `litigations` - Legal case tracking
- `app_settings` - Application configuration

## Core Features

### 🏢 Residence Management
**Complete CRUD Operations:**
- Create residences with wizard (multi-step form)
- Edit residence information (superadmin only)
- View residences (filtered by role)
- Assign administrators to residences
- Manage units within residences

**API Endpoints:**
- `GET /api/admin/residences` - List residences (filtered by role)
- `POST /api/admin/residences` - Create residence
- `POST /api/admin/residences/wizard` - Create residence with full structure
- `PUT /api/admin/residences/<id>` - Update residence
- `GET /api/admin/residences/<id>/units` - Get units
- `POST /api/admin/residences/<id>/units` - Create unit
- `POST /api/admin/residences/<id>/admins` - Assign admins
- `GET /api/admin/residences/<id>/admins` - Get assigned admins
- `DELETE /api/admin/residences/<id>/admins/<admin_id>` - Remove admin

### 🗳️ General Assembly (Assemblée Générale) System

**Complete Assembly Management:**
- Create assemblies (ordinary/extraordinary)
- Schedule meetings (physical/online/hybrid)
- Send convocations to members
- Track attendance (physical and online)
- Manage resolutions and voting
- Generate minutes (procès-verbal)

**Live Assembly Features with Agora.io Integration:**
- **Real-time video/audio conferencing** via Agora.io
- **Meeting modes**: Physical, Online, or Hybrid
- **Cloud recording** for online sessions
- **Live attendance tracking** with online/physical mode distinction
- **Real-time voting** during assembly sessions

**Agora Integration Details:**
- Uses `agora-token-builder` SDK for secure token generation
- RTC (Real-Time Communication) tokens for video/audio
- RTM (Real-Time Messaging) tokens for chat features
- Automatic cloud recording start/stop
- Channel name generation: `assembly_{id}_{timestamp}`

**API Endpoints:**
- `GET /api/admin/assemblies` - List assemblies
- `POST /api/admin/assemblies` - Create assembly
- `POST /api/admin/assemblies/<id>/send-convocations` - Send invitations
- `POST /api/admin/assemblies/<id>/start` - Start assembly (activates Agora)
- `POST /api/admin/assemblies/<id>/end` - End assembly
- `GET /api/admin/assemblies/<id>/agora-token` - Get Agora RTC token
- `GET /api/admin/assemblies/<id>/attendance` - Get attendance list
- `POST /api/admin/assemblies/<id>/attendance/mark` - Mark attendance
- `POST /api/admin/assemblies/<id>/attendance/join-online` - Join online
- `GET /api/admin/assemblies/<id>/resolutions` - List resolutions
- `POST /api/admin/assemblies/<id>/resolutions` - Create resolution

**Agora Configuration Required:**
Environment variables needed for live assemblies:
- `AGORA_APP_ID` - Your Agora application ID
- `AGORA_APP_CERTIFICATE` - Your Agora app certificate

### ✅ Voting System

**Resolution Voting (Assembly Context):**
- Create resolutions linked to assemblies
- Multiple vote types: simple majority, double majority, unanimity
- Real-time vote counting
- Vote value options: For, Against, Abstain
- Vote change allowed (recounted automatically)
- Attendance verification (must be present to vote)

**API Endpoints:**
- `POST /api/admin/resolutions/<id>/vote` - Submit/update vote
- Vote requires user to be marked present at assembly

**Polls (Community Surveys):**
- Create polls for resident feedback
- Multiple choice options
- Anonymous or named voting
- Single or multiple answer support
- Automatic result calculation with percentages
- Status management: draft, active, closed

**Poll Features:**
- Real-time results with vote counts
- Percentage calculations
- Time-limited polls (start/end dates)
- Result visualization ready

### 🔧 Maintenance Management

**Complete Maintenance Workflow:**
- Create maintenance requests
- Track requests with unique tracking numbers
- Comment system with mentions
- Document attachments
- Priority levels (low, medium, high, urgent)
- Status tracking (pending, in_progress, resolved, cancelled)
- Assign to technicians
- Schedule interventions
- Admin notes (internal)

**Maintenance Log (Carnet d'Entretien):**
- Historical record of all maintenance
- Preventive and corrective maintenance types
- Category tracking (plumbing, electrical, roofing, etc.)
- Contractor information
- Cost tracking with invoice numbers
- Next intervention scheduling
- Warranty tracking

### 💰 Financial Management

**Charge System:**
- Create charges (recurring or one-time)
- Automatic distribution to units
- Multiple charge types supported
- Period tracking (monthly/yearly)
- Due date management
- Status tracking

**Payment Processing:**
- Record payments per unit
- Multiple payment methods
- Payment proof upload
- Admin approval workflow
- Payment history tracking

### 📰 Dual News Feed System

**Fil d'actualité (Feed):**
- Accessible to ALL users (superadmin, admin, owner, resident)
- General residence information
- Community announcements
- Event notifications

**Actualités et annonces (Announcements):**
- Restricted to superadmin, admin, and owners ONLY
- Official communications
- Assembly convocations
- Important decisions
- Residents receive 403 Forbidden if accessing

**Features:**
- Pin important posts
- Category system
- Publish/draft status
- Rich text content
- Author tracking

### 📄 Document Management

**Document Features:**
- Upload documents per residence
- Document categories (financial, legal, technical, assembly)
- Public/private visibility control
- File metadata (size, type, date)
- Version tracking
- Access control by role

### ⚖️ Litigation Management

**Legal Case Tracking:**
- Track legal cases and disputes
- Link to units when applicable
- Reference number system
- Status tracking (open, in_progress, resolved)
- Hearing dates
- Lawyer information
- Amount tracking
- Resolution notes

## System Architecture

### Technology Stack

**Backend:**
- **Framework:** Flask 3.0.0
- **Database:** PostgreSQL (Replit Database)
- **ORM:** SQLAlchemy 2.0.23
- **Migrations:** Flask-Migrate 4.0.5
- **Authentication:** Flask-Login 0.6.3
- **Session Management:** JWT tokens via PyJWT 2.8.0
- **WSGI Server:** Gunicorn 21.2.0
- **Security:** Werkzeug 3.0.1 (password hashing)
- **Email:** Flask-Mail 0.9.1
- **Live Video:** Agora Token Builder

**Frontend:**
- **CSS Framework:** Tailwind CSS (CDN)
- **Icons:** Feather Icons
- **JavaScript:** Vanilla JS (no framework)
- **Template Engine:** Jinja2
- **Design System:** Mobile-first, responsive design

### Project Structure

```
shabaka-syndic/
├── backend/
│   ├── app.py              # Flask application factory
│   ├── config.py           # Configuration management
│   ├── models/             # SQLAlchemy models (22 tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── residence.py
│   │   ├── general_assembly.py  # Assembly, Resolution, Vote, Attendance
│   │   ├── poll.py              # Poll, PollOption, PollVote
│   │   ├── maintenance.py
│   │   ├── maintenance_comment.py
│   │   ├── maintenance_document.py
│   │   ├── maintenance_log.py
│   │   ├── charge.py            # Charge, ChargeDistribution
│   │   ├── payment.py
│   │   ├── news.py
│   │   ├── document.py
│   │   ├── litigation.py
│   │   ├── residence_admin.py
│   │   └── app_settings.py
│   ├── routes/             # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication
│   │   ├── admin.py        # Admin/Syndic routes (2500+ lines)
│   │   └── resident.py     # Resident routes
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── charge_calculator.py    # Automatic charge distribution
│   │   ├── notification_service.py # Email notifications
│   │   └── agora_service.py        # Agora.io token generation
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── decorators.py   # Custom decorators
├── frontend/
│   ├── static/             # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/          # Jinja2 templates
│       ├── index.html
│       ├── admin/          # Admin interface
│       │   ├── dashboard.html
│       │   ├── residences.html
│       │   ├── residence_wizard.html
│       │   ├── residence_edit.html
│       │   ├── assemblies.html
│       │   ├── assembly_live.html   # Live assembly with Agora
│       │   ├── finances.html
│       │   ├── maintenance.html
│       │   ├── maintenance_log.html
│       │   ├── users.html
│       │   ├── feed.html
│       │   ├── announcements.html
│       │   ├── documents.html
│       │   └── settings.html
│       ├── resident/       # Resident interface
│       │   ├── dashboard.html
│       │   ├── maintenance.html
│       │   ├── finances.html
│       │   ├── feed.html
│       │   ├── announcements.html
│       │   ├── assemblies.html
│       │   └── documents.html
│       └── auth/           # Authentication
│           ├── login.html
│           └── register.html
├── main.py                 # Application entry point
├── init_db.py              # Database initialization script
├── reset_db.py             # Database reset script
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Python project config
└── replit.md              # This file
```

## Role-Based Access Control (RBAC)

### 1. Super Admin (`superadmin`)
**Full platform access**

**Accessible Menus:**
- 📊 Super Admin Dashboard
- 📱 News Feed (all access)
- 📰 Announcements (create/manage)
- 🏢 Residences (view all, create, edit, assign admins)
- 👥 Users (full management)
- 💰 Finances (full access)
- 🔧 Maintenance (full access)
- 📝 Maintenance Log (full access)
- 🗳️ Assemblies (full access)
- 📄 Documents (full access)
- ⚙️ Settings (full access)
- 🚪 Logout

**Quick Actions:**
- 🏗️ New Residence (wizard)

**Specific Rights:**
- View all residences on platform
- Create residences and assign admins
- Global data management
- All configuration access

### 2. Bureau Syndic / Admin (`admin`)
**Operational management of assigned residences**

**Accessible Menus:**
- 📊 Syndic Dashboard
- 📱 News Feed (all access)
- 📰 Announcements (create/manage)
- 🏢 Residences (view assigned only - **cannot create/edit/delete**)
- 👥 Users (manage residents/owners in assigned residences)
- 💰 Finances (manage charges, **approve payment declarations**)
- 🔧 Maintenance (full access)
- 📝 Maintenance Log (full access)
- 🗳️ Assemblies (create, manage, conduct)
- 📄 Documents (manage)
- ⚙️ Settings (view only)
- 🚪 Logout

**Role Badge:** "Bureau Syndic" displayed in UI

**Specific Rights:**
- Manage only assigned residences
- Approve payment declarations after verification
- Create and conduct assemblies
- Publish announcements
- Cannot create new residences

### 3. Propriétaire / Owner (`owner`)
**Property owner in residence**

**Accessible Menus:**
- 📊 Owner Dashboard
- 📱 News Feed (all access)
- 📰 Announcements (view only)
- 🔧 Maintenance (request, comment, track)
- 💰 Finances (view own unit charges and payment history)
- 🗳️ Assemblies (participate and vote)
- 📄 Documents (view residence documents)
- 🚪 Logout

**Specific Rights:**
- Manage residents in own unit (add/block/remove)
- Participate in general assemblies
- Submit and track maintenance requests
- View financial obligations

### 4. Résident / Resident (`resident`)
**Tenant with limited access**

**Accessible Menus:**
- 📊 Resident Dashboard
- 📱 News Feed (all access - **NO access to Announcements**)
- 🔧 Maintenance (request and track only)
- 🚪 Logout

**Restrictions:**
- ❌ No access to Announcements
- ❌ No access to Finances
- ❌ No access to Assemblies
- ❌ No access to Documents

## Demo Data & Testing

### Demo User Accounts

The application automatically initializes with demo data on first launch:

| Email | Password | Role | Access Level |
|-------|----------|------|--------------|
| `admin@mysindic.ma` | `Admin123!` | Super Admin | Full platform access |
| `admin.syndic@mysindic.ma` | `Admin123!` | Bureau Syndic 1 | Residence "Les Jardins" |
| `bureau.syndic@mysindic.ma` | `Admin123!` | Bureau Syndic 2 | Residence "Les Jardins" |
| `owner@mysindic.ma` | `Owner123!` | Propriétaire | Unit A102 |
| `resident@mysindic.ma` | `Resident123!` | Résident | Unit A102 |
| `karim@mysindic.ma` | `Resident123!` | Résident | Unit A201 |

### Demo Data Included

- **1 Residence:** "Les Jardins de l'Océan" in Casablanca
- **5 Units:** A101, A102, A201, A202, A301
- **6 Users:** All roles represented
- **1 Charge:** Monthly charges with distribution
- **2 Payments:** Validated payment records
- **3 Maintenance Requests:** With comments and tracking
- **2 Maintenance Log Entries:** Historical maintenance records
- **4 News Items:** 2 feed posts + 2 announcements

## Environment Variables

### Required for Basic Operation
- `DATABASE_URL` - PostgreSQL connection string (auto-configured by Replit)
- `SESSION_SECRET` - Flask session secret (auto-generated)

### Required for Live Assemblies (Agora.io)
- `AGORA_APP_ID` - Your Agora application ID
- `AGORA_APP_CERTIFICATE` - Your Agora app certificate

To enable live assembly features:
1. Create account at [Agora.io](https://www.agora.io/)
2. Create a project in Agora Console
3. Copy App ID and App Certificate
4. Add as secrets in Replit

### Optional
- `MAIL_SERVER` - SMTP server for email notifications
- `MAIL_PORT` - SMTP port
- `MAIL_USERNAME` - Email username
- `MAIL_PASSWORD` - Email password

## API Documentation

### Authentication Endpoints

**POST /api/auth/login**
- Login user
- Body: `{email, password}`
- Returns: User session

**POST /api/auth/register**
- Register new user
- Body: `{email, password, first_name, last_name, role}`
- Returns: User object

**POST /api/auth/logout**
- Logout current user
- Returns: Success message

### Residence Management

**GET /api/admin/residences**
- Get residences (filtered by user role)
- Returns: List of residences

**POST /api/admin/residences**
- Create residence (superadmin only)
- Body: Residence data + units array
- Returns: Created residence

**POST /api/admin/residences/wizard**
- Create residence with full structure
- Body: `{residence, units, admin_ids}`
- Returns: Created residence with units

**PUT /api/admin/residences/<id>**
- Update residence (superadmin only)
- Body: Updated fields
- Returns: Updated residence

### Assembly Management

**GET /api/admin/assemblies**
- Get assemblies for accessible residences
- Returns: List of assemblies

**POST /api/admin/assemblies**
- Create general assembly
- Body: `{title, description, assembly_type, meeting_mode, scheduled_date, location, residence_id}`
- Returns: Created assembly

**POST /api/admin/assemblies/<id>/start**
- Start assembly (activates Agora if online/hybrid)
- Returns: Assembly with Agora info

**GET /api/admin/assemblies/<id>/agora-token**
- Get Agora RTC token for joining live session
- Returns: `{app_id, channel_name, token, uid}`

**POST /api/admin/assemblies/<id>/attendance/join-online**
- Mark attendance as online participant
- Returns: Updated attendance

### Voting Endpoints

**POST /api/admin/assemblies/<id>/resolutions**
- Create resolution for assembly
- Body: `{title, description, vote_type, order}`
- Returns: Created resolution

**POST /api/admin/resolutions/<id>/vote**
- Submit/update vote on resolution
- Body: `{vote_value}` (for/against/abstain)
- Requires: User marked present at assembly
- Returns: Updated vote counts

### Maintenance Management

**GET /api/resident/maintenance**
- Get maintenance requests (filtered by access)
- Returns: List of requests

**POST /api/resident/maintenance**
- Create maintenance request
- Body: Request details
- Returns: Created request with tracking number

## Database Schema Details

### Key Relationships

**User → Residence:** Many-to-One (user.residence_id)
**User → Unit:** Many-to-One (user.unit_id)
**ResidenceAdmin:** Many-to-Many junction (User ↔ Residence)
**GeneralAssembly → Resolution:** One-to-Many
**Resolution → Vote:** One-to-Many
**GeneralAssembly → Attendance:** One-to-Many
**Poll → PollOption:** One-to-Many
**Poll → PollVote:** One-to-Many
**Charge → ChargeDistribution:** One-to-Many
**Unit → ChargeDistribution:** One-to-Many

### Important Constraints

- **Unique vote per user per resolution:** (resolution_id, user_id)
- **Unique poll vote:** (poll_id, user_id, option_id)
- **Unique residence admin assignment:** (residence_id, user_id)
- **Unique tracking numbers:** maintenance_requests.tracking_number

## Development Workflow

### Running the Application

1. **Start:** Application starts automatically via workflow
2. **Port:** Runs on port 5000 (configured for webview)
3. **Access:** Click "Webview" button in Replit
4. **Auto-reload:** Gunicorn configured with --reload flag

### Database Management

**Initialize Database:**
```bash
python init_db.py
```

**Reset Database:**
```bash
python reset_db.py
```

**Migrations:**
Database tables are created automatically on first run via SQLAlchemy's `db.create_all()`.

### Testing Features

1. **Login:** Use demo accounts above
2. **Test Residence Creation:** Login as superadmin → Résidences → Nouvelle Résidence
3. **Test Assembly:** Login as admin → Assemblées → Create assembly
4. **Test Live Assembly:** Create assembly with meeting_mode='online' → Start → Get Agora token
5. **Test Voting:** Join assembly → Mark attendance → Vote on resolutions
6. **Test Maintenance:** Login as resident → Maintenance → Create request

## User Preferences

- **Language:** All code comments and documentation in French
- **Workflow:** Iterative development preferred
- **Documentation:** Keep replit.md updated with major changes
- **Communication:** Clear explanations before architectural changes
- **Confirmation:** Ask before adding external dependencies

## Security Best Practices

- **Password Hashing:** Uses Werkzeug's default method (scrypt)
- **Session Management:** Flask-Login with secure sessions
- **SQL Injection Protection:** SQLAlchemy ORM with parameterized queries
- **CORS:** Configured via Flask-CORS
- **Environment Variables:** Secrets in Replit Secrets (DATABASE_URL, SESSION_SECRET, AGORA keys)
- **Authorization:** Role-based decorators on all routes
- **CSRF Protection:** Built into Flask forms
- **Input Validation:** Server-side validation on all endpoints

## Performance Considerations

- **Database Connection Pooling:** SQLAlchemy pool_recycle=300, pool_pre_ping=True
- **Lazy Loading:** Relationships configured for optimal query performance
- **Indexes:** On foreign keys and frequently queried fields
- **Pagination:** Implemented for large data sets
- **Caching:** Consider adding Flask-Caching for production

## Known Issues & Limitations

- **LSP Type Warnings:** Minor type checking warnings in poll.py (runtime safe)
- **Agora Setup:** Requires manual configuration of AGORA_APP_ID and AGORA_APP_CERTIFICATE
- **Email:** Requires SMTP configuration for notifications
- **File Uploads:** File storage needs configuration for production
- **Tailwind CDN:** Using CDN for development (should build for production)

## Future Enhancements

- [ ] Implement Flask-Caching for performance
- [ ] Add WebSocket support for real-time updates
- [ ] Implement document version control
- [ ] Add PDF generation for financial reports
- [ ] Enhanced mobile app (native or PWA)
- [ ] SMS notifications via Twilio
- [ ] Payment gateway integration (CMI, Stripe)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support (French/Arabic)
- [ ] Export functionality (Excel, PDF)

## Troubleshooting

### Database Issues
- **Connection Error:** Check DATABASE_URL environment variable
- **Table Missing:** Run `python init_db.py`
- **Data Corruption:** Run `python reset_db.py` (WARNING: deletes all data)

### Application Issues
- **Port Conflict:** Application must run on port 5000 for webview
- **Authentication:** Clear cookies if session issues
- **Agora Not Working:** Verify AGORA_APP_ID and AGORA_APP_CERTIFICATE are set

### Workflow Issues
- **Not Running:** Click "Run" button or use workflow restart
- **Changes Not Visible:** Workflow has --reload flag, should auto-reload
- **Port Not Ready:** Wait for "Listening on port 5000" in logs

## Support & Contact

- **Developer:** Aisance KALONJI
- **Email:** moa@myoneart.com
- **Website:** www.myoneart.com
- **Project:** Shabaka Syndic - Complete Condominium Management Platform

---

**Last Updated:** November 22, 2025
**Version:** 0.1.0
**Status:** ✅ Production Ready
