# MEASURE VERIFY

### From Manual Verification to Digital, Traceable Certification

**Smart India Hackathon 2026**

**Problem Statement ID:** SIH26036  
**Problem Statement:** Development of an Online Verification System for Weighing and Measuring Instruments  
**Category:** Software  
**Theme:** Miscellaneous  
**Team Name:** GLITCH BUSTERS  
**Team ID:** 173726

---

## 📌 Overview

MEASURE VERIFY is a web-based digital verification and certification platform designed to streamline the verification and re-verification lifecycle of weighing and measuring instruments.

The system converts a manual and paperwork-heavy workflow into a centralized digital process covering:

**Register → Apply → Schedule → Inspect → Verify → Risk Analysis → Certify → QR Verify → Track → Renew**

The platform provides role-based access for Users, Legal Metrology Officers (LMOs), Government Approved Test Centres (GATCs), and Administrators.

---

## 🎯 Problem Statement

Under the Legal Metrology framework, weighing and measuring instruments used in transactions or for protection require periodic verification and stamping.

Traditional processes can involve:

- Manual application submission
- Physical documentation
- Manual scheduling and allocation
- Paper-based inspection records
- Physical certificates
- Difficulty tracking verification history
- Manual monitoring of validity and expiry
- Limited centralized visibility of records

MEASURE VERIFY addresses these challenges through a centralized digital verification workflow.

---

## 💡 Proposed Solution

MEASURE VERIFY provides a secure and user-friendly platform for managing the complete verification lifecycle of weighing and measuring instruments.

### Core capabilities

- Online stakeholder login
- Role-based access control
- Instrument registration
- Verification and re-verification applications
- Digital inspection scheduling
- Digital inspection observations and results
- Instrument-wise verification history
- Rule/statistical risk analysis
- Digital certificate generation
- SHA-256 certificate record integrity
- QR-based certificate verification
- Validity tracking
- Risk monitoring
- Audit logging
- Dashboards and record retrieval

---

# 🚀 Key Features

## 1. Instrument Registration

Users can register weighing and measuring instruments with details including:

- Instrument number
- Instrument type
- Manufacturer
- Model
- Capacity
- Owner name
- Location

Each instrument receives a centralized digital record.

---

## 2. Online Verification Application

Users can submit verification or re-verification applications online.

The system records:

- Application number
- Instrument details
- Applicant information
- Verification type
- Application date
- Application status

---

## 3. Digital Scheduling

LMO users can view pending applications and schedule inspections.

The system records:

- Scheduled date
- Assigned inspector
- Application status

---

## 4. Digital Inspection

Inspection information can be recorded digitally, including:

- Inspection observations
- Verification result
- Failure count
- Remarks
- Evidence/document support

The application status is updated according to the inspection result.

---

# 🧠 Instrument Risk Intelligence

MEASURE VERIFY includes an explainable **rule/statistical risk analysis module**.

The system analyzes verification history and identifies patterns such as:

- Previous failed inspections
- Repeated failures
- Higher failure counts
- Overdue verification
- Abnormal verification patterns

The system assigns:

- 🟢 LOW
- 🟡 MEDIUM
- 🔴 HIGH

risk levels.

This helps identify instruments that may require closer monitoring or priority re-verification.

> The current MVP uses explainable rule/statistical analysis and does not claim AI/ML-based prediction.

---

# 📜 Digital Certificate

After successful verification, the system generates a digital certificate containing information such as:

- Certificate number
- Application reference
- Instrument number
- Issue date
- Validity date
- Verification result
- Certificate status
- Record integrity hash

Certificates are stored digitally and can be retrieved through the application.

---

# 🔐 SHA-256 Certificate Integrity

MEASURE VERIFY uses **SHA-256 hashing** to check the integrity of certificate records.

### Verification process

1. Certificate data is created.
2. A SHA-256 hash is generated from the certificate record.
3. The hash is stored with the certificate.
4. During verification, the certificate data is hashed again.
5. The calculated hash is compared with the stored hash.

If the hashes match:

**VERIFIED — Certificate record is intact.**

If the hashes do not match:

**ALTERED / INVALID — Hash mismatch detected.**

This provides an integrity check for the stored certificate record.

---

# 📱 QR-Based Certificate Verification

Each digital certificate can have an associated QR code.

The QR code contains certificate verification information that can be used to retrieve and verify the certificate record.

The verification process checks:

- Certificate number
- Application reference
- Instrument information
- Certificate record
- SHA-256 integrity

---

# 👥 User Roles

### 👤 User

Users can:

- Register instruments
- Submit verification applications
- Submit re-verification applications
- Track application status
- View certificate records

### 👨‍💼 Legal Metrology Officer (LMO)

LMOs can:

- View pending applications
- Schedule inspections
- Record inspection observations
- Enter verification results
- Generate certificates
- Monitor instrument risk
- Review verification history

### 🏢 Government Approved Test Centre (GATC)

GATC users can participate in the digital verification workflow for assigned inspections through role-based access.

### 👨‍💻 Administrator

Administrators can:

- Monitor instruments
- Monitor applications
- View certificates
- Monitor risk records
- Review audit logs
- Monitor system activity

---

# 🔄 System Workflow

```text
Register Instrument
        ↓
Apply for Verification
        ↓
Schedule Inspection
        ↓
Digital Inspection
        ↓
Verification Result
        ↓
Risk Analysis
        ↓
Digital Certificate
        ↓
SHA-256 Integrity Check
        ↓
QR Verification
        ↓
Validity Tracking
        ↓
Renewal / Re-verification

🔒 Security & Trust
Role-Based Access Control

Different users receive access according to their role:

User
LMO
GATC
Admin
Password Protection

User passwords are stored using SHA-256 password hashing rather than plain-text passwords.

Certificate Integrity

SHA-256 record hashes are used to detect changes to stored certificate records.

Audit Logging

Important system activities are recorded, including:

Login
Logout
Inspection scheduling
Inspection completion
Certificate generation

📊 Dashboards & Monitoring

The system provides dashboards for monitoring:

Registered instruments
Applications
Pending applications
Scheduled inspections
Certificates
Risk levels
Verification status
Audit activities

📁 Project Structure

MEASURE_VERIFY/
│
├── app.py
├── database.py
├── auth.py
├── instrument.py
├── application.py
├── inspection.py
├── risk_analysis.py
├── certificate.py
├── qr_verification.py
├── audit.py
├── create_users.py
├── risk_engine.py
├── requirements.txt
├── .gitignore
│
├── assets/
├── data/
└── certificates/

🧪 Prototype Validation

The working MVP has been tested through the main verification workflow.
User Login
    ↓
Instrument Registration
    ↓
Application Submission
    ↓
LMO Login
    ↓
Inspection Scheduling
    ↓
Digital Inspection
    ↓
Risk Analysis
    ↓
Certificate Generation
    ↓
SHA-256 Integrity Verification
    ↓
QR Verification
    ↓
Audit Log
Tested Role-Based Access
User ✅
LMO ✅
GATC ✅
Admin ✅
Certificate Verification

The prototype successfully verifies certificate integrity by comparing the calculated SHA-256 hash with the stored certificate record hash.

🌱 Future Scope

The current implementation is an MVP designed for rapid validation and demonstration.

Future extensions can include:

Dedicated mobile field application
Offline inspection support with synchronization
Large-scale managed database deployment
State-wide and multi-state deployment
Integration with existing government systems where APIs are made available
Advanced analytics and reporting
Automated notification services
Integration with additional verification and compliance services

These are future extensions and are not claimed as implemented features of the current MVP.

📈 Scalability

The system can evolve from:
Pilot
  ↓
State-Level Deployment
  ↓
Multi-State Deployment
The current MVP uses SQLite for lightweight validation.

For production-scale deployment, the database and infrastructure can be migrated to managed and scalable services.

🏆 Smart India Hackathon 2026

Problem Statement ID: SIH26036

Project: MEASURE VERIFY

Team: GLITCH BUSTERS

Theme: Miscellaneous

Category: Software

💎 Core Innovation

Risk Intelligence + Tamper-Evident Certification

MEASURE VERIFY moves beyond simple digital record keeping by connecting the verification lifecycle with explainable risk monitoring and certificate record integrity verification.

📄 Project Status

Current Status: Working MVP

Deployment: Streamlit Community Cloud

Repository:https://github.com/Suhamhasware12/MEASURE_VERIFY.git


