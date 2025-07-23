import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()


@st.cache_data
def get_job_ids():
    """Get job IDs by name matching and cache them"""
    try:
        jobs = list(w.jobs.list())
        job_ids = {}

        for job in jobs:
            name = job.settings.name
            # Match jobs containing our base names
            if "Main Job" in name:
                job_ids["main"] = job.job_id
                job_ids["main_name"] = name
            elif "Well Job" in name:
                job_ids["well"] = job.job_id
                job_ids["well_name"] = name

        return job_ids
    except Exception as e:
        st.error(f"Error getting job IDs: {str(e)}")
        return {}


def trigger_job_by_id(job_id, job_name="Job"):
    """Trigger a job using its ID"""
    try:
        response = w.jobs.run_now(job_id=job_id)
        st.success(f"{job_name} started successfully! Run ID: {response.run_id}")
        return response
    except Exception as e:
        st.error(f"Failed to trigger {job_name}: {str(e)}")
        return None


# Get job IDs once and cache them
job_ids = get_job_ids()

# UI
st.title("Databricks Job Trigger")

if job_ids:
    col1, col2 = st.columns(2)

    with col1:
        if "main" in job_ids:
            if st.button("Trigger Main Job", use_container_width=True):
                trigger_job_by_id(job_ids["main"], "Main Job")
        else:
            st.error("Main Job not found")

    with col2:
        if "well" in job_ids:
            if st.button("Trigger Well Job", use_container_width=True):
                trigger_job_by_id(job_ids["well"], "Well Job")
        else:
            st.error("Well Job not found")

    # Debug section
    with st.expander("Debug: Job Information"):
        if "main" in job_ids:
            st.write(
                f"Main Job ID: {job_ids['main']} (Name: {job_ids.get('main_name', 'Unknown')})"
            )
        if "well" in job_ids:
            st.write(
                f"Well Job ID: {job_ids['well']} (Name: {job_ids.get('well_name', 'Unknown')})"
            )
else:
    st.error("No jobs found. Check service principal permissions.")

##############################3

# import os
# import streamlit as st
# from databricks.sdk import WorkspaceClient
# from databricks.sdk.errors import DatabricksError


# w = WorkspaceClient()


# def debug_workspace_client():
#     """Debug WorkspaceClient authentication and permissions"""
#     try:
#         # Test basic workspace connection
#         current_user = w.current_user.me()
#         st.write(f"✅ Connected as: {current_user.user_name}")
#         st.write(f"✅ Workspace URL: {w.config.host}")

#         # Test jobs API specifically
#         try:
#             jobs = list(w.jobs.list())
#             st.write(f"✅ Jobs API accessible: Found {len(jobs)} jobs")
#             if len(jobs) == 0:
#                 st.warning("Jobs API returns empty list - possible permissions issue")
#         except DatabricksError as e:
#             st.error(f"❌ Jobs API error: {e}")

#         # Test workspace permissions
#         try:
#             workspace_info = w.workspace.get_status("/")
#             st.write(f"✅ Workspace access: {workspace_info.object_type}")
#         except DatabricksError as e:
#             st.error(f"❌ Workspace access error: {e}")

#     except Exception as e:
#         st.error(f"❌ WorkspaceClient initialization failed: {e}")


# def debug_jobs():
#     """Debug function to see all available jobs"""
#     try:
#         jobs = list(w.jobs.list())
#         st.write(f"Found {len(jobs)} jobs:")
#         for job in jobs:
#             st.write(f"- Job ID: {job.job_id}, Name: '{job.settings.name}'")
#         return jobs
#     except Exception as e:
#         st.error(f"Error listing jobs: {str(e)}")
#         return []


# def get_job_id_by_name(job_name):
#     """Get job ID by searching for job name with better error handling"""
#     try:
#         jobs = list(w.jobs.list())
#         st.write(f"Searching for '{job_name}' among {len(jobs)} jobs")

#         for job in jobs:
#             current_name = job.settings.name
#             st.write(f"Checking: '{current_name}'")
#             if current_name == job_name:
#                 return job.job_id

#         # If exact match fails, try case-insensitive
#         for job in jobs:
#             if job.settings.name.lower() == job_name.lower():
#                 st.warning(f"Found job with case mismatch: '{job.settings.name}'")
#                 return job.job_id

#         return None
#     except Exception as e:
#         st.error(f"Error finding job {job_name}: {str(e)}")
#         return None


# def trigger_job_by_name(job_name):
#     """Trigger a job by name"""
#     job_id = get_job_id_by_name(job_name)
#     if not job_id:
#         st.error(f"Job '{job_name}' not found")
#         return None

#     try:
#         response = w.jobs.run_now(job_id=job_id)
#         st.success(f"{job_name} started successfully! Run ID: {response.run_id}")
#         return response
#     except Exception as e:
#         st.error(f"Failed to trigger {job_name}: {str(e)}")
#         return None


# # UI
# with st.expander("Debug: Available Jobs"):
#     debug_jobs()

# with st.expander("Debug: WorkspaceClient Status"):
#     debug_workspace_client()

# st.title("Databricks Job Trigger")

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Trigger Main Job", use_container_width=True):
#         trigger_job_by_name("Main Job")

# with col2:
#     if st.button("Trigger Well Job", use_container_width=True):
#         trigger_job_by_name("Well Job")
