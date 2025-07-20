# Databricks Apps CI/CD with GitHub Actions and Databricks Asset Bundles

This repository provides a minimal example of how to automate the deployment of Databricks Apps using GitHub Actions and Databricks Asset Bundles (DABs).

For a detailed explanation, refer to the accompanying blog post: [**Automate your Databricks Apps deployments with GitHub Actions and Databricks Asset Bundles**](https://apps-cookbook.dev/blog/automate-apps-deployments-dabs).

## Deployment Instructions

### Prerequisites

- Python 3.11 or later
- Databricks CLI 0.18.0 or later
- A Databricks workspace with access to Databricks Apps

### 1. Clone the Repository

Fork this repository and clone it to your local machine:

```bash
git clone https://github.com/pbv0/databricks-apps-dabs
cd databricks-apps-dabs
```

### 2. Set Up Local Development

1. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r app/requirements.txt
   ```
2. Run the app locally:
   ```bash
   streamlit run app/app.py
   ```
3. Run unit tests:
   ```bash
   python -m pytest
   ```

### 3. Configure Databricks Environments

Update the `databricks.yml` file with your Databricks workspace URLs for the `dev` and `prod` environments:

```yaml
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: <your-dev-workspace-url>
  prod:
    mode: production
    workspace:
      host: <your-prod-workspace-url>
```

### 4. Deploy to Development Environment

1. Authenticate with Databricks CLI using OAuth:
   ```bash
   databricks auth login
   ```
2. Deploy to the development environment:
   ```bash
   databricks bundle deploy -t dev
   ```
3. Start the app in the development environment:
   ```bash
   databricks bundle run hello-world-app -t dev
   ```

### 5. Set Up GitHub Actions for CI/CD

1. Create a service principal for production deployments and note its `client ID` and `client secret`.
2. Add the following secrets to your GitHub repository:
   - `DATABRICKS_CLIENT_ID`: Service principal client ID.
   - `DATABRICKS_CLIENT_SECRET`: Service principal OAuth secret.
   - `DATABRICKS_HOST`: Your Databricks workspace URL.

### 6. Trigger Production Deployment

1. Push changes to the `main` branch or create a pull request to trigger the CI pipeline.
2. Create a new release in GitHub to trigger the production deployment workflow.

## Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Databricks CLI Documentation](https://docs.databricks.com/aws/en/dev-tools/cli/)

For more details, refer to the blog post: [**Automate your Databricks Apps deployments with GitHub Actions and Databricks Asset Bundles**](https://apps-cookbook.dev/blog/automate-apps-deployments-dabs).
