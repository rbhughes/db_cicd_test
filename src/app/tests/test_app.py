from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def test_app_loads():
    with patch("databricks.sdk.WorkspaceClient") as mock_workspace_client:
        mock_workspace_client.return_value = None

        at = AppTest.from_file("../app.py").run()

        assert not at.exception
