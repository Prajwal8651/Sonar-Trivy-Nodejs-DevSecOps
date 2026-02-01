# DevSecOps Landing Page (FastAPI)

A simple Python FastAPI application used to demonstrate **SonarQube** (code quality) and **Trivy** (security) scans within a Jenkins CI/CD pipeline.

# travia installation

cd /tmp
wget https://github.com/aquasecurity/trivy/releases/download/v0.56.2/trivy_0.56.2_Linux-64bit.tar.gz
tar zxvf trivy_0.56.2_Linux-64bit.tar.gz
sudo mv trivy /usr/local/bin/
trivy --version

sonar initialization:
docker run -d --name sonarqube \
  -p 9000:9000 sonarqube:community


## 🚀 Features
- Lightweight FastAPI web app
- Dockerized
- Integrated with SonarQube and Trivy
- Jenkins pipeline ready

## 🛠️ Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## 🐳 Build Docker Image
```bash
docker build -t devsecops-landing-page .
docker run -d -p 8000:8000 devsecops-landing-page
```

