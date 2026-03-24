# 🔐 DevSecOps Lab

A hands-on DevSecOps project demonstrating security vulnerability detection and remediation in a Python Flask web application.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)
![Docker](https://img.shields.io/badge/Docker-secure-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.35.1-blue)
![Security](https://img.shields.io/badge/Security-Hardened-brightgreen)

## 📋 Overview

This project simulates a real-world DevSecOps pipeline by:
- Building a deliberately vulnerable Flask application
- Scanning it with multiple security tools (SAST, DAST, SCA)
- Fixing all identified vulnerabilities
- Re-scanning to verify fixes
- Deploying to Kubernetes with security hardening

## 🛠️ Tools Used

| Category | Tool | Purpose |
|----------|------|---------|
| SAST | Bandit | Python static analysis |
| SAST | Semgrep | Advanced static analysis |
| SCA | pip-audit | Dependency vulnerability scanning |
| Secret Scanning | detect-secrets | Hardcoded secret detection |
| Container | Trivy | Docker image vulnerability scanning |
| Kubernetes | Kubescape | K8s security posture scanning |
| DAST | OWASP ZAP | Dynamic application security testing |
| CI/CD | GitHub Actions | Automated security pipeline |

## 🚨 Vulnerabilities Found & Fixed

### Application (app.py)
| # | Vulnerability | Severity | Status |
|---|--------------|----------|--------|
| 1 | Hardcoded secret key | High | ✅ Fixed |
| 2 | Hardcoded DB credentials | High | ✅ Fixed |
| 3 | Weak MD5 password hashing | High | ✅ Fixed |
| 4 | SQL Injection in /login | Medium | ✅ Fixed |
| 5 | SQL Injection in /notes | Medium | ✅ Fixed |
| 6 | Command Injection in /ping | High | ✅ Fixed |
| 7 | Insecure YAML loading | Medium | ✅ Fixed |
| 8 | Sensitive data exposure | Medium | ✅ Fixed |
| 9 | Debug mode enabled | High | ✅ Fixed |

### Docker
| # | Vulnerability | Status |
|---|--------------|--------|
| D1 | Old base image (python:3.9) | ✅ Fixed |
| D2 | Running as root | ✅ Fixed |
| D3 | Copying sensitive files | ✅ Fixed |
| D4 | No health check | ✅ Fixed |

## 📊 Security Scan Results

### Before Fixes
| Tool | Findings |
|------|---------|
| Bandit | 15 issues (4 High) |
| pip-audit | 48 CVEs |
| Semgrep | 25 findings |
| detect-secrets | 23 secrets |
| Trivy | 168 CVEs (4 Critical) |
| Kubescape | 1 failure |

### After Fixes
| Tool | Findings |
|------|---------|
| Bandit | 3 issues (0 High) ✅ |
| pip-audit | 0 CVEs ✅ |
| Semgrep | 0 findings ✅ |
| detect-secrets | 0 in app code ✅ |
| Trivy | 77 CVEs (0 Critical) ✅ |
| Kubescape | 0 failures ✅ |

## 🏗️ Project Structure
```
devsecops_lab/
├── app/
│   ├── app.py          ← Flask application
│   ├── config.py       ← Configuration
│   └── requirements.txt
├── tests/
│   └── test_app.py     ← Security tests
├── k8s/
│   ├── deployment.yaml ← K8s deployment
│   ├── service.yaml    ← K8s service
│   └── networkpolicy.yaml ← Network policy
├── .github/
│   └── workflows/
│       └── devsecops.yml ← CI/CD pipeline
├── Dockerfile
└── reports/            ← Scan reports
```

## 🚀 Running the Project

### Prerequisites
- Python 3.13+
- Docker Desktop
- Minikube
- kubectl

### Local Setup
```bash
git clone git@github.com:EmDev17/devsecops_lab.git
cd devsecops_lab
python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
python app/app.py
```

### Run Security Scans
```bash
bandit -r app/
pip-audit -r app/requirements.txt
semgrep --config=auto app/
detect-secrets scan --all-files
```

### Deploy to Kubernetes
```bash
minikube start --driver=docker
kubectl apply -f k8s/
minikube service devsecops-lab-service --url
```

## 👩‍💻 Author
Emma Tataryan — DevSecOps Lab Project
