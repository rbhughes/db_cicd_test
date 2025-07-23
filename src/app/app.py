import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError


w = WorkspaceClient()


def debug_workspace_client():
    """Debug WorkspaceClient authentication and permissions"""
    try:
        # Test basic workspace connection
        current_user = w.current_user.me()
        st.write(f"✅ Connected as: {current_user.user_name}")
        st.write(f"✅ Workspace URL: {w.config.host}")

        # Test jobs API specifically
        try:
            jobs = list(w.jobs.list())
            st.write(f"✅ Jobs API accessible: Found {len(jobs)} jobs")
            if len(jobs) == 0:
                st.warning("Jobs API returns empty list - possible permissions issue")
        except DatabricksError as e:
            st.error(f"❌ Jobs API error: {e}")

        # Test workspace permissions
        try:
            workspace_info = w.workspace.get_status("/")
            st.write(f"✅ Workspace access: {workspace_info.object_type}")
        except DatabricksError as e:
            st.error(f"❌ Workspace access error: {e}")

    except Exception as e:
        st.error(f"❌ WorkspaceClient initialization failed: {e}")


def debug_jobs():
    """Debug function to see all available jobs"""
    try:
        jobs = list(w.jobs.list())
        st.write(f"Found {len(jobs)} jobs:")
        for job in jobs:
            st.write(f"- Job ID: {job.job_id}, Name: '{job.settings.name}'")
        return jobs
    except Exception as e:
        st.error(f"Error listing jobs: {str(e)}")
        return []


def get_job_id_by_name(job_name):
    """Get job ID by searching for job name with better error handling"""
    try:
        jobs = list(w.jobs.list())
        st.write(f"Searching for '{job_name}' among {len(jobs)} jobs")

        for job in jobs:
            current_name = job.settings.name
            st.write(f"Checking: '{current_name}'")
            if current_name == job_name:
                return job.job_id

        # If exact match fails, try case-insensitive
        for job in jobs:
            if job.settings.name.lower() == job_name.lower():
                st.warning(f"Found job with case mismatch: '{job.settings.name}'")
                return job.job_id

        return None
    except Exception as e:
        st.error(f"Error finding job {job_name}: {str(e)}")
        return None


def trigger_job_by_name(job_name):
    """Trigger a job by name"""
    job_id = get_job_id_by_name(job_name)
    if not job_id:
        st.error(f"Job '{job_name}' not found")
        return None

    try:
        response = w.jobs.run_now(job_id=job_id)
        st.success(f"{job_name} started successfully! Run ID: {response.run_id}")
        return response
    except Exception as e:
        st.error(f"Failed to trigger {job_name}: {str(e)}")
        return None


# UI
with st.expander("Debug: Available Jobs"):
    debug_jobs()

with st.expander("Debug: WorkspaceClient Status"):
    debug_workspace_client()

st.title("Databricks Job Trigger")

col1, col2 = st.columns(2)

with col1:
    if st.button("Trigger Main Job", use_container_width=True):
        trigger_job_by_name("Main Job")

with col2:
    if st.button("Trigger Well Job", use_container_width=True):
        trigger_job_by_name("Well Job")


# import os
# import streamlit as st
# import requests
# from databricks.sdk import WorkspaceClient

# JOB_ID = os.getenv("JOB_ID")

# w = WorkspaceClient()

# DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
# DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
# WELL_JOB_NAME = "Well Job"  # Must match job.name in databricks.yml


# def trigger_well_job():
#     # Get the job ID by name
#     response = requests.get(
#         f"{DATABRICKS_HOST}/api/2.1/jobs/list",
#         headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
#     )
#     response.raise_for_status()
#     jobs = response.json().get("jobs", [])
#     job = next((j for j in jobs if j["settings"]["name"] == WELL_JOB_NAME), None)

#     if not job:
#         st.error(f"Job '{WELL_JOB_NAME}' not found.")
#         return

#     # Trigger a run
#     run_resp = requests.post(
#         f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
#         headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
#         json={"job_id": job["job_id"]},
#     )
#     run_resp.raise_for_status()
#     st.success(f"Triggered Well Job! Run ID: {run_resp.json().get('run_id')}")


# st.code(f"DATABRICKS_HOST={DATABRICKS_HOST}")
# st.code(f"DATABRICKS_TOKEN={DATABRICKS_TOKEN}")
# st.code(f"WELL_JOB_NAME={WELL_JOB_NAME}")
# st.code(f"JOB_ID={JOB_ID}")

# if st.button(f"Trigger job with ID {JOB_ID}"):
#     print(w)
#     try:
#         response = w.jobs.run_now(job_id=JOB_ID)
#         st.success("Job started successfully!")
#     except Exception as e:
#         st.error(e)

# if st.button("Run well job"):
#     trigger_well_job()
