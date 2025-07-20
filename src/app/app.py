import os
import streamlit as st
from databricks.sdk import WorkspaceClient

JOB_ID = os.getenv("JOB_ID")

w = WorkspaceClient()


if st.button(f"Trigger job with ID {JOB_ID}"):
    try:
        response = w.jobs.run_now(job_id=JOB_ID)
        st.success("Job started successfully!")
    except Exception as e:
        st.error(e)
