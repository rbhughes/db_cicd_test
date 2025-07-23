import os
import streamlit as st
import requests
from databricks.sdk import WorkspaceClient

JOB_ID = os.getenv("JOB_ID")

w = WorkspaceClient()

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
WELL_JOB_NAME = "Well Job"  # Must match job.name in databricks.yml


def trigger_well_job():
    # Get the job ID by name
    response = requests.get(
        f"{DATABRICKS_HOST}/api/2.1/jobs/list",
        headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
    )
    response.raise_for_status()
    jobs = response.json().get("jobs", [])
    job = next((j for j in jobs if j["settings"]["name"] == WELL_JOB_NAME), None)

    if not job:
        st.error(f"Job '{WELL_JOB_NAME}' not found.")
        return

    # Trigger a run
    run_resp = requests.post(
        f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
        headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
        json={"job_id": job["job_id"]},
    )
    run_resp.raise_for_status()
    st.success(f"Triggered Well Job! Run ID: {run_resp.json().get('run_id')}")


st.code(f"DATABRICKS_HOST={DATABRICKS_HOST}")
st.code(f"DATABRICKS_TOKEN={DATABRICKS_TOKEN}")
st.code(f"WELL_JOB_NAME={WELL_JOB_NAME}")
st.code(f"JOB_ID={JOB_ID}")

if st.button(f"Trigger job with ID {JOB_ID}"):
    print(w)
    try:
        response = w.jobs.run_now(job_id=JOB_ID)
        st.success("Job started successfully!")
    except Exception as e:
        st.error(e)

if st.button(f"Run well job"):
    trigger_well_job()
