# MEASURE VERIFY - Technical Architecture

## Technology Stack

- Python
- Streamlit
- SQLite
- SHA-256 hashing
- QR Code generation
- Rule/statistical risk analysis
- Git and GitHub
- Streamlit Community Cloud

## Architecture

MEASURE VERIFY follows a modular web application architecture.

### User Interface

The application uses Streamlit to provide a web-based interface.

### Authentication and RBAC

The system provides role-based access for:

- User
- LMO
- GATC
- Admin

### Application Workflow

The application workflow manages:

- Instrument registration
- Verification applications
- Re-verification
- Scheduling
- Inspection
- Certification

### Database

SQLite is used for storing:

- Users
- Instruments
- Applications
- Inspections
- Certificates
- Risk records
- Audit logs

### Risk Analysis

The system uses explainable rule/statistical analysis to calculate instrument risk based on verification history and failure patterns.

### Certificate Integrity

SHA-256 hashing is used to generate a record hash for digital certificate data.

During verification, the calculated hash is compared with the stored hash.

### QR Verification

QR codes are generated for digital certificates and contain certificate verification information.

### Audit Logging

Important system actions are recorded in audit logs for traceability.

## Data Flow

Register
→ Apply
→ Schedule
→ Inspect
→ Verify
→ Risk Analysis
→ Certificate
→ SHA-256 Hash
→ QR Verification
→ Track Validity

## Deployment

The prototype is deployed using Streamlit Community Cloud.

## Production Extension

The current implementation is an MVP. The modular architecture can be extended to a production web stack and managed database for larger-scale deployment.
