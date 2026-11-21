# STEP 16 - DEPLOYMENT PLAN
## D17 | Loan Disbursement Trend Analysis

**Target:** Streamlit Community Cloud | **Status:** Deploy-ready locally; publication requires owner account/repository

## 1. Deployment objective

Provide the academic synthetic-data Streamlit app for demonstration through a version-controlled repository while protecting secrets and disclosing that hosted local SQLite persistence is not durable.

## 2. Target configuration

- Repository name requested by the brief: `mca2-da-loan-disbursement-trend-analysis`; remote URL is not supplied.
- Entrypoint: `app.py` at repository root.
- Runtime dependencies: root `requirements.txt`; development/test/notebook extras are in `requirements-dev.txt`.
- Streamlit configuration: `.streamlit/config.toml`; sample is bundled and no secrets are required.
- SQLite database: local file under `data/`; app creates schema and reloads the synthetic sample if the active dataset is absent.
- Synthetic records only; no private credentials or real customer data.

## 3. Release procedure

1. Ensure automated tests pass and review the committed artifact inventory.
2. Push to a GitHub repository owned or administered by SH-001; include runtime `requirements.txt` and `app.py`.
3. In Streamlit Community Cloud, connect the authorized GitHub account, choose repository and branch, set main file to `app.py`, select a compatible Python version if needed, then deploy. Streamlit documents this repository/branch/entrypoint workflow and requires repository admin access ([deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [GitHub access requirements](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account)).
4. Open the deployed URL and verify the data notice, sample load, filters, KPIs, charts, preview and CSV download. Inspect logs for exceptions.
5. Record URL, deployed commit/tag, deployment date, smoke outcome and account owner.

## 4. Secrets and access

No secret is required for the synthetic MVP. If future integrations require a secret, configure it in the platform secret manager; never commit credentials, `.streamlit/secrets.toml`, tokens or private data. Restrict repository write access to authorized collaborators.

## 5. Persistence, reset and rollback

Treat hosted local disk as ephemeral. If the active DB is missing, app startup creates schema and reloads the versioned sample. Re-deploying a previous Git commit/tag is the rollback path. The SQLite file and user exports are not durable backups. Any persistent user-entered data would require a separately reviewed managed store.

## 6. Deployment checklist

- [ ] Remote URL and owner/admin confirmed (OQ-009).
- [ ] Root runtime `requirements.txt` matches tested app dependencies.
- [ ] Entrypoint and Python version selected.
- [ ] Tests and local smoke run pass.
- [ ] No real personal data, secret or credential committed.
- [ ] Synthetic notice and no-durability warning visible.
- [ ] Owner deploys and records cloud smoke evidence.
- [ ] URL, tag and date recorded; rollback path documented.

## 7. Current blocker and responsible action

No Git remote URL, Streamlit Community Cloud account, or named-account publishing authorization was supplied. The local package is deployment-ready, but publication cannot be claimed. Streamlit expects a `requirements.txt` at repository root or beside the app entrypoint ([dependency guidance](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)). SH-001 must connect an authorized repository and deploy under their own account; no credentials should be shared in chat. OQ-009 remains open until a URL and smoke test are recorded.

## 8. Operational limitations

Community Cloud runtime/Python support can change; follow current official platform setup instructions. This is a demonstration, not a production service: no SLA, authentication, durable storage, or operational support is promised.
