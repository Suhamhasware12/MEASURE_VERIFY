# MEASURE VERIFY - Testing

## Prototype Validation

The MEASURE VERIFY prototype was tested through the main verification workflow and role-based access system.

## Authentication Testing

The following roles were tested successfully:

- User
- LMO
- GATC
- Admin

## Functional Testing

### Instrument Registration

Users can register weighing and measuring instruments with instrument details, owner information and location.

### Application Submission

Users can submit verification and re-verification applications.

### Inspection Scheduling

LMO users can view pending applications and schedule inspections.

### Digital Inspection

Inspection observations, verification results, failure count and remarks can be recorded digitally.

### Risk Monitoring

The system calculates an instrument risk level using rule/statistical risk analysis.

Risk levels include:

- LOW
- MEDIUM
- HIGH

### Certificate Generation

A successful verification can generate a digital certificate with a certificate number, validity information and record hash.

### QR Verification

QR codes can be generated for certificates and used for certificate verification.

### SHA-256 Integrity Verification

The system recalculates the certificate record hash and compares it with the stored hash.

A matching hash produces:

`VERIFIED — Certificate record is intact.`

### Audit Logging

Important actions are recorded in the audit log, including:

- Login
- Logout
- Inspection scheduling
- Inspection completion
- Certificate generation

## End-to-End Workflow Tested

User Login
→ Instrument Registration
→ Application Submission
→ LMO Login
→ Inspection Scheduling
→ Digital Inspection
→ Risk Analysis
→ Certificate Generation
→ QR Verification
→ Audit Log

## Result

The main prototype workflow and role-based access functionality were successfully tested in the working MVP.
