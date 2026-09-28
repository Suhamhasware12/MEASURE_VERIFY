import sqlite3
from datetime import datetime, date, timedelta

import streamlit as st

from database import initialize_database
from auth import authenticate_user
from instrument import (
    register_instrument,
    get_user_instruments
)
from application import (
    create_application,
    get_user_applications
)
from inspection import (
    get_pending_applications,
    get_scheduled_applications,
    schedule_inspection,
    record_inspection
)
from risk_analysis import (
    calculate_risk,
    get_instrument_risk,
    get_all_risk_records
)
from certificate import (
    create_certificate,
    get_certificate_by_application,
    get_all_certificates
)
from qr_verification import (
    generate_qr,
    verify_certificate,
    get_qr_file
)
from audit import (
    log_action,
    get_audit_logs
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MEASURE VERIFY",
    page_icon="⚖️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_connection():
    conn = sqlite3.connect(
        "data/measure_verify.db"
    )
    conn.row_factory = sqlite3.Row
    return conn


def get_dashboard_counts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM instruments"
    )
    instruments = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications"
    )
    applications = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Pending'"
    )
    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Scheduled'"
    )
    scheduled = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM certificates"
    )
    certificates = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM risk_records WHERE risk_level = 'HIGH'"
    )
    high_risk = cursor.fetchone()[0]

    conn.close()

    return {
        "instruments": instruments,
        "applications": applications,
        "pending": pending,
        "scheduled": scheduled,
        "certificates": certificates,
        "high_risk": high_risk
    }


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title("⚖️ MEASURE VERIFY")

    st.subheader(
        "Digital, Traceable & Risk-Based Legal Metrology Verification"
    )

    st.caption(
        "From Manual Verification to Digital, Traceable Certification"
    )

    st.divider()

    st.markdown("### 🔐 Secure Login")

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button(
        "Login",
        type="primary",
        width="stretch"
    ):

        if not username or not password:

            st.warning(
                "Please enter username and password."
            )

        else:

            user = authenticate_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                log_action(
                    username,
                    "LOGIN",
                    "USER",
                    None,
                    "User logged into MEASURE VERIFY"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    st.divider()

    st.info(
        "Demo accounts: user / user123 | "
        "lmo / lmo123 | gatc / gatc123 | admin / admin123"
    )

    st.caption(
        "MEASURE VERIFY | Smart India Hackathon 2026 | SIH26036"
    )


# ============================================================
# USER DASHBOARD
# ============================================================

def user_dashboard():

    user = st.session_state.user

    st.title("👤 User Dashboard")

    st.write(
        f"Welcome, **{user['full_name']}**"
    )

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "⚖️ Register Instrument",
        "📝 Apply for Verification",
        "📋 My Applications",
        "📜 My Certificates"
    ])

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    with tab1:

        st.subheader("My Instruments")

        instruments = get_user_instruments(
            user["full_name"]
        )

        if instruments:

            st.dataframe(
                instruments,
                width="stretch"
            )

        else:

            st.info(
                "No instruments registered yet."
            )

        st.divider()

        st.subheader(
            "🔄 Verification Workflow"
        )

        workflow = [
            "Register",
            "Apply",
            "Schedule",
            "Inspect",
            "Verify",
            "Certify",
            "Renew"
        ]

        cols = st.columns(len(workflow))

        for col, step in zip(
            cols,
            workflow
        ):

            with col:

                st.markdown(
                    f"**{step}**"
                )

    # --------------------------------------------------------
    # REGISTER INSTRUMENT
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "⚖️ Register New Instrument"
        )

        instrument_number = st.text_input(
            "Instrument Number *",
            placeholder="Example: WM-2026-002"
        )

        instrument_type = st.selectbox(
            "Instrument Type *",
            [
                "Weighing Scale",
                "Electronic Weighing Machine",
                "Platform Scale",
                "Retail Weighing Scale",
                "Measuring Instrument",
                "Other"
            ]
        )

        manufacturer = st.text_input(
            "Manufacturer",
            placeholder="Example: ABC Instruments"
        )

        model = st.text_input(
            "Model",
            placeholder="Example: ABC-500"
        )

        capacity = st.text_input(
            "Capacity",
            placeholder="Example: 50 kg"
        )

        owner_name = st.text_input(
            "Owner Name",
            value=user["full_name"]
        )

        location = st.text_input(
            "Instrument Location",
            placeholder="Example: Pune, Maharashtra"
        )

        if st.button(
            "Register Instrument",
            type="primary",
            width="stretch"
        ):

            if not instrument_number:

                st.warning(
                    "Instrument Number is required."
                )

            elif not owner_name:

                st.warning(
                    "Owner Name is required."
                )

            else:

                success, message = register_instrument(
                    instrument_number,
                    instrument_type,
                    manufacturer,
                    model,
                    capacity,
                    owner_name,
                    location
                )

                if success:

                    log_action(
                        user["username"],
                        "REGISTER_INSTRUMENT",
                        "INSTRUMENT",
                        None,
                        f"Instrument {instrument_number} registered"
                    )

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    if "UNIQUE" in message:

                        st.error(
                            "This Instrument Number already exists."
                        )

                    else:

                        st.error(
                            f"Registration failed: {message}"
                        )

    # --------------------------------------------------------
    # APPLY FOR VERIFICATION
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "📝 Apply for Verification"
        )

        instruments = get_user_instruments(
            user["full_name"]
        )

        if not instruments:

            st.warning(
                "Please register an instrument before applying."
            )

        else:

            instrument_options = {}

            for instrument in instruments:

                instrument_options[
                    instrument["instrument_number"]
                ] = instrument["id"]

            selected_instrument = st.selectbox(
                "Select Instrument *",
                list(instrument_options.keys())
            )

            verification_type = st.selectbox(
                "Verification Type *",
                [
                    "Initial Verification",
                    "Periodic Verification",
                    "Re-verification"
                ]
            )

            st.info(
                "Submit your verification application. "
                "The application will initially be marked as Pending."
            )

            if st.button(
                "Submit Verification Application",
                type="primary",
                width="stretch"
            ):

                instrument_id = instrument_options[
                    selected_instrument
                ]

                application_number = create_application(
                    instrument_id,
                    user["username"],
                    user["full_name"],
                    verification_type
                )

                log_action(
                    user["username"],
                    "SUBMIT_APPLICATION",
                    "APPLICATION",
                    None,
                    f"Application {application_number} submitted"
                )

                st.success(
                    "Verification application submitted successfully."
                )

                st.markdown(
                    f"### Application ID: `{application_number}`"
                )

                st.info(
                    "Keep this Application ID for tracking."
                )

    # --------------------------------------------------------
    # MY APPLICATIONS
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "📋 My Verification Applications"
        )

        applications = get_user_applications(
            user["username"]
        )

        if applications:

            st.dataframe(
                applications,
                width="stretch"
            )

        else:

            st.info(
                "No verification applications submitted yet."
            )

    # --------------------------------------------------------
    # MY CERTIFICATES
    # --------------------------------------------------------

    with tab5:

        st.subheader(
            "📜 My Digital Certificates"
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.certificate_number,
                i.instrument_number,
                i.instrument_type,
                c.issue_date,
                c.valid_until,
                c.verification_result,
                c.status
            FROM certificates c
            JOIN instruments i
                ON c.instrument_id = i.id
            WHERE i.owner_name = ?
            ORDER BY c.id DESC
        """, (
            user["full_name"],
        ))

        certificates = cursor.fetchall()

        conn.close()

        if certificates:

            st.dataframe(
                certificates,
                width="stretch"
            )

        else:

            st.info(
                "No certificates issued yet."
            )


# ============================================================
# LMO DASHBOARD
# ============================================================

def lmo_dashboard():

    user = st.session_state.user

    st.title("👷 LMO Dashboard")

    st.write(
        f"Welcome, **{user['full_name']}**"
    )

    st.caption(
        "Legal Metrology Officer / Verification Officer"
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 Pending Applications",
        "📅 Scheduled Inspections",
        "🔍 Inspection",
        "⚠️ Risk Monitoring"
    ])

    # --------------------------------------------------------
    # PENDING APPLICATIONS
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "📥 Pending Verification Applications"
        )

        applications = get_pending_applications()

        if not applications:

            st.success(
                "No pending applications."
            )

        else:

            for application in applications:

                with st.expander(
                    f"{application['application_number']} — "
                    f"{application['instrument_number']}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Applicant:** {application['applicant_name']}"
                        )

                        st.write(
                            f"**Instrument:** {application['instrument_number']}"
                        )

                        st.write(
                            f"**Type:** {application['instrument_type']}"
                        )

                        st.write(
                            f"**Manufacturer:** {application['manufacturer']}"
                        )

                        st.write(
                            f"**Model:** {application['model']}"
                        )

                    with col2:

                        st.write(
                            f"**Verification:** {application['verification_type']}"
                        )

                        st.write(
                            f"**Capacity:** {application['capacity']}"
                        )

                        st.write(
                            f"**Location:** {application['location']}"
                        )

                        st.write(
                            f"**Status:** {application['status']}"
                        )

                    st.divider()

                    st.markdown(
                        "### Schedule Inspection"
                    )

                    schedule_date = st.date_input(
                        "Inspection Date",
                        value=date.today() + timedelta(days=1),
                        key=f"date_{application['id']}"
                    )

                    schedule_time = st.time_input(
                        "Inspection Time",
                        value=datetime.now().replace(
                            second=0,
                            microsecond=0
                        ).time(),
                        key=f"time_{application['id']}"
                    )

                    if st.button(
                        "Schedule & Assign Inspection",
                        key=f"schedule_{application['id']}",
                        type="primary",
                        width="stretch"
                    ):

                        scheduled_datetime = (
                            f"{schedule_date} "
                            f"{schedule_time}"
                        )

                        schedule_inspection(
                            application["id"],
                            scheduled_datetime,
                            user["username"]
                        )

                        log_action(
                            user["username"],
                            "SCHEDULE_INSPECTION",
                            "APPLICATION",
                            application["id"],
                            f"Inspection scheduled for {scheduled_datetime}"
                        )

                        st.success(
                            "Inspection scheduled successfully."
                        )

                        st.rerun()

    # --------------------------------------------------------
    # SCHEDULED INSPECTIONS
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "📅 My Scheduled Inspections"
        )

        scheduled = get_scheduled_applications(
            user["username"]
        )

        if not scheduled:

            st.info(
                "No scheduled inspections."
            )

        else:

            st.dataframe(
                scheduled,
                width="stretch"
            )

    # --------------------------------------------------------
    # DIGITAL INSPECTION
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "🔍 Digital Inspection"
        )

        scheduled = get_scheduled_applications(
            user["username"]
        )

        if not scheduled:

            st.info(
                "No scheduled inspections available."
            )

        else:

            inspection_options = {}

            for application in scheduled:

                label = (
                    f"{application['application_number']} — "
                    f"{application['instrument_number']}"
                )

                inspection_options[
                    label
                ] = application

            selected_label = st.selectbox(
                "Select Application",
                list(inspection_options.keys())
            )

            selected = inspection_options[
                selected_label
            ]

            st.info(
                f"Instrument: {selected['instrument_number']} | "
                f"Type: {selected['instrument_type']} | "
                f"Applicant: {selected['applicant_name']}"
            )

            observations = st.text_area(
                "Inspection Observations",
                placeholder=(
                    "Enter inspection observations, "
                    "measurement results and remarks..."
                )
            )

            result = st.selectbox(
                "Verification Result",
                [
                    "PASS",
                    "FAIL"
                ]
            )

            failure_count = st.number_input(
                "Failure Count",
                min_value=0,
                max_value=20,
                value=0,
                step=1
            )

            remarks = st.text_area(
                "Inspector Remarks",
                placeholder="Enter final inspection remarks..."
            )

            if st.button(
                "Submit Inspection Result",
                type="primary",
                width="stretch"
            ):

                if not observations:

                    st.warning(
                        "Please enter inspection observations."
                    )

                else:

                    record_inspection(
                        selected["id"],
                        user["username"],
                        observations,
                        result,
                        failure_count,
                        remarks
                    )

                    # Calculate risk after inspection
                    risk = calculate_risk(
                        selected["instrument_id"]
                    )

                    log_action(
                        user["username"],
                        "COMPLETE_INSPECTION",
                        "APPLICATION",
                        selected["id"],
                        f"Inspection result: {result}"
                    )

                    st.success(
                        "Inspection result recorded successfully."
                    )

                    st.markdown(
                        "### ⚠️ Instrument Risk Analysis"
                    )

                    st.write(
                        f"**Risk Level:** {risk['risk_level']}"
                    )

                    st.write(
                        f"**Risk Score:** {risk['risk_score']}"
                    )

                    st.write(
                        f"**Explanation:** {risk['explanation']}"
                    )

                    if result == "PASS":

                        st.success(
                            "Instrument passed verification."
                        )

                        certificate_number = create_certificate(
                            selected["id"],
                            selected["instrument_id"],
                            "VERIFIED",
                            365
                        )

                        if certificate_number:

                            qr_file = generate_qr(
                                certificate_number
                            )

                            log_action(
                                user["username"],
                                "GENERATE_CERTIFICATE",
                                "CERTIFICATE",
                                None,
                                f"Certificate {certificate_number} generated"
                            )

                            st.success(
                                "Digital certificate generated successfully."
                            )

                            st.markdown(
                                f"### 📜 Certificate: `{certificate_number}`"
                            )

                            if qr_file:

                                st.image(
                                    qr_file,
                                    caption="Certificate QR Code",
                                    width=220
                                )

                    else:

                        st.error(
                            "Instrument failed verification. "
                            "Certificate will not be issued."
                        )

                    st.rerun()

    # --------------------------------------------------------
    # RISK MONITORING
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "⚠️ Instrument Risk Monitoring"
        )

        risk_records = get_all_risk_records()

        if risk_records:

            st.dataframe(
                risk_records,
                width="stretch"
            )

        else:

            st.info(
                "No risk analysis records available yet."
            )


# ============================================================
# GATC DASHBOARD
# ============================================================

def gatc_dashboard():

    user = st.session_state.user

    st.title("🏢 GATC Dashboard")

    st.write(
        f"Welcome, **{user['full_name']}**"
    )

    st.caption(
        "Government Approved Test Centre"
    )

    st.divider()

    st.info(
        "GATC workflow uses the same digital verification "
        "process for assigned inspections."
    )

    scheduled = get_scheduled_applications(
        user["username"]
    )

    if scheduled:

        st.subheader(
            "📅 Assigned Inspections"
        )

        st.dataframe(
            scheduled,
            width="stretch"
        )

    else:

        st.info(
            "No inspections are currently assigned to this GATC account."
        )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():

    user = st.session_state.user

    st.title("🏛️ Admin Dashboard")

    st.write(
        f"Welcome, **{user['full_name']}**"
    )

    st.caption(
        "System Administration & Monitoring"
    )

    st.divider()

    counts = get_dashboard_counts()

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:

        st.metric(
            "Instruments",
            counts["instruments"]
        )

    with col2:

        st.metric(
            "Applications",
            counts["applications"]
        )

    with col3:

        st.metric(
            "Pending",
            counts["pending"]
        )

    with col4:

        st.metric(
            "Scheduled",
            counts["scheduled"]
        )

    with col5:

        st.metric(
            "Certificates",
            counts["certificates"]
        )

    with col6:

        st.metric(
            "High Risk",
            counts["high_risk"]
        )

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚖️ Instruments",
        "📝 Applications",
        "📜 Certificates",
        "⚠️ Risk Monitoring",
        "📋 Audit Logs"
    ])

    # --------------------------------------------------------
    # INSTRUMENTS
    # --------------------------------------------------------

    with tab1:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                instrument_number,
                instrument_type,
                manufacturer,
                model,
                capacity,
                owner_name,
                location,
                registration_date,
                status
            FROM instruments
            ORDER BY id DESC
        """)

        instruments = cursor.fetchall()

        conn.close()

        if instruments:

            st.dataframe(
                instruments,
                width="stretch"
            )

        else:

            st.info(
                "No instruments found."
            )

    # --------------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------------

    with tab2:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.application_number,
                a.applicant_name,
                i.instrument_number,
                a.verification_type,
                a.application_date,
                a.scheduled_date,
                a.assigned_to,
                a.status,
                a.remarks
            FROM applications a
            LEFT JOIN instruments i
                ON a.instrument_id = i.id
            ORDER BY a.id DESC
        """)

        applications = cursor.fetchall()

        conn.close()

        if applications:

            st.dataframe(
                applications,
                width="stretch"
            )

        else:

            st.info(
                "No applications found."
            )

    # --------------------------------------------------------
    # CERTIFICATES
    # --------------------------------------------------------

    with tab3:

        certificates = get_all_certificates()

        if certificates:

            st.dataframe(
                certificates,
                width="stretch"
            )

        else:

            st.info(
                "No certificates issued yet."
            )

    # --------------------------------------------------------
    # RISK MONITORING
    # --------------------------------------------------------

    with tab4:

        risk_records = get_all_risk_records()

        if risk_records:

            st.dataframe(
                risk_records,
                width="stretch"
            )

        else:

            st.info(
                "No risk records available."
            )

    # --------------------------------------------------------
    # AUDIT LOGS
    # --------------------------------------------------------

    with tab5:

        logs = get_audit_logs()

        if logs:

            st.dataframe(
                logs,
                width="stretch"
            )

        else:

            st.info(
                "No audit logs available."
            )


# ============================================================
# CERTIFICATE VERIFICATION PAGE
# ============================================================

def certificate_verification_page():

    st.title(
        "🔎 Certificate Verification"
    )

    st.write(
        "Verify a MEASURE VERIFY digital certificate "
        "using its certificate number."
    )

    certificate_number = st.text_input(
        "Certificate Number",
        placeholder="Example: CERT-20260928-ABC123"
    )

    if st.button(
        "Verify Certificate",
        type="primary",
        width="stretch"
    ):

        if not certificate_number:

            st.warning(
                "Please enter a certificate number."
            )

        else:

            result = verify_certificate(
                certificate_number
            )

            if result["valid"]:

                st.success(
                    "✅ VERIFIED — Certificate record is intact."
                )

                certificate = result["certificate"]

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Certificate:** "
                        f"{certificate['certificate_number']}"
                    )

                    st.write(
                        f"**Instrument:** "
                        f"{certificate['instrument_number']}"
                    )

                    st.write(
                        f"**Issue Date:** "
                        f"{certificate['issue_date']}"
                    )

                with col2:

                    st.write(
                        f"**Valid Until:** "
                        f"{certificate['valid_until']}"
                    )

                    st.write(
                        f"**Result:** "
                        f"{certificate['verification_result']}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{certificate['status']}"
                    )

                st.divider()

                st.markdown(
                    "### SHA-256 Integrity Check"
                )

                st.code(
                    result["stored_hash"]
                )

                qr_file = get_qr_file(
                    certificate_number
                )

                if qr_file:

                    st.image(
                        qr_file,
                        caption="Certificate QR Code",
                        width=220
                    )

            else:

                st.error(
                    result["message"]
                )

                if "stored_hash" in result:

                    st.write(
                        "**Stored Hash:**"
                    )

                    st.code(
                        result["stored_hash"]
                    )

                    st.write(
                        "**Calculated Hash:**"
                    )

                    st.code(
                        result["calculated_hash"]
                    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def dashboard():

    user = st.session_state.user

    role = user["role"]

    # Sidebar
    with st.sidebar:

        st.title("⚖️ MEASURE VERIFY")

        st.write(
            f"**User:** {user['full_name']}"
        )

        st.write(
            f"**Role:** {role}"
        )

        st.divider()

        if st.button(
            "🔎 Certificate Verification",
            width="stretch"
        ):

            st.session_state.show_verification = True

        if st.button(
            "🏠 Dashboard",
            width="stretch"
        ):

            st.session_state.show_verification = False

        st.divider()

        if st.button(
            "🚪 Logout",
            width="stretch"
        ):

            log_action(
                user["username"],
                "LOGOUT",
                "USER",
                None,
                "User logged out"
            )

            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.show_verification = False

            st.rerun()

    if "show_verification" not in st.session_state:

        st.session_state.show_verification = False

    if st.session_state.show_verification:

        certificate_verification_page()

        return

    # Role-based dashboard
    if role == "User":

        user_dashboard()

    elif role == "LMO":

        lmo_dashboard()

    elif role == "GATC":

        gatc_dashboard()

    elif role == "Admin":

        admin_dashboard()

    else:

        st.error(
            "Unknown user role."
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if st.session_state.logged_in:

    dashboard()

else:

    login_page()