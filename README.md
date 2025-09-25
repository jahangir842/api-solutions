# 📂 `api-management-solutions`


This repository contains **hands-on labs, Infrastructure as Code (IaC), and automation scripts** for learning and implementing **API Gateways and API Management solutions**.  

As a DevOps engineer, you’ll use this repo to:
- Learn API gateway concepts (Kong, Azure APIM, AWS API Gateway, GCP Apigee).
- Practice with Docker, Kubernetes, Terraform, Ansible, and PowerShell.
- Explore security best practices (JWT, OAuth2, mTLS, WAF).
- Monitor and log API usage with Prometheus, Grafana, CloudWatch, and Azure Monitor.
- Automate API deployments with CI/CD (GitHub Actions, Azure DevOps, GitLab).

---

## 🏗 Repository Structure

```bash
api-management-labs/
├── README.md                # Overview of repo
├── docs/                    # Documentation and theory
│   ├── intro-to-api-gateway.md
│   ├── kong-vs-azure-vs-aws.md
│   ├── security-best-practices.md
│   ├── monitoring-and-logging.md
│   ├── governance.md
│   └── glossary.md
├── kong/                    # Kong API Gateway
│   ├── docker-compose/
│   │   ├── docker-compose.yml
│   │   └── kong.yml
│   ├── kubernetes/
│   │   ├── manifests/
│   │   │   ├── kong-deployment.yaml
│   │   │   ├── ingress-example.yaml
│   │   │   └── rate-limiting-plugin.yaml
│   ├── terraform/
│   │   └── main.tf
│   ├── ansible/
│   │   └── install-kong.yml
│   └── labs.md
├── azure-apim/
│   ├── terraform/
│   │   └── main.tf
│   ├── powershell/
│   │   ├── create-apim.ps1
│   │   └── policies.ps1
│   ├── policies/
│   │   ├── rate-limit.xml
│   │   ├── jwt-validation.xml
│   │   └── cors.xml
│   └── labs.md
├── aws-apigateway/
│   ├── terraform/
│   │   ├── rest-api.tf
│   │   ├── websocket-api.tf
│   │   └── lambda-integration.tf
│   ├── ansible/
│   │   └── create-api.yml
│   └── labs.md
├── gcp-apigee/
│   ├── terraform/
│   │   └── main.tf
│   └── labs.md
├── security/
│   ├── jwt-oauth2.md
│   ├── mTLS.md
│   └── waf.md
├── monitoring/
│   ├── kong-prometheus.md
│   ├── azure-apim-appinsights.md
│   ├── aws-cloudwatch.md
│   └── grafana-dashboards/
│       └── kong-dashboard.json
└── ci-cd/
    ├── github-actions/
    │   └── deploy-kong.yml
    ├── azure-devops/
    │   └── deploy-apim-pipeline.yml
    └── gitlab-ci/
        └── aws-apigateway-ci.yml
```

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* Kubernetes (Minikube / Kind / AKS / EKS)
* Terraform & Ansible
* PowerShell (for Azure APIM)
* GitHub Actions / Azure DevOps / GitLab CI

### How to Use

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/api-management-labs.git
   cd api-management-labs
   ```

2. Start with [docs/intro-to-api-gateway.md](docs/intro-to-api-gateway.md).

3. Pick a lab (e.g., `kong/docker-compose`) and follow the instructions.

4. Deploy the same API on different gateways (Kong vs Azure APIM vs AWS API Gateway).

5. Compare features, security, and monitoring.

---

## 📚 Topics Covered

* Kong API Gateway
* Azure API Management (APIM)
* AWS API Gateway
* GCP Apigee
* API Security (JWT, OAuth2, mTLS, WAF)
* Monitoring (Prometheus, Grafana, CloudWatch, Azure Monitor)
* CI/CD Pipelines for API lifecycle management

---

## 📖 Learning Path

1. **Basics** → API Gateway concepts.
2. **Kong** → Local + Kubernetes + Terraform + Ansible.
3. **Azure APIM** → Policies + PowerShell + Terraform.
4. **AWS API Gateway** → Lambda integration + Terraform + Ansible.
5. **Security** → OAuth2/JWT, mTLS, WAF.
6. **Monitoring** → Prometheus, Grafana, CloudWatch, App Insights.
7. **CI/CD** → GitHub Actions, Azure DevOps, GitLab CI.

---

## 🛡 License

MIT License – free to use and share.



---


