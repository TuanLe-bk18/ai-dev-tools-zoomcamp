# Homework 3: Test, Containerize, and Deploy an AI-Assisted App

Submission URL: [DataTalks.Club HW3](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw3)

## Quiz Answers

### Question 1: Architecture
- **Question:** Which description matches the project's architecture?
- **Answer:** `Agents claim tasks from a DB through an HTTP API.`
- **Rationale:** [SPEC.md](SPEC.md) lines 17, 25-28: Identities, tasks, and delivery attempts are stored in a database (SQLite/PostgreSQL) and manipulated via the HTTP REST API. There is no external message broker and agents do not communicate peer-to-peer.

### Question 2: Task status
- **Question:** Which task status does the sender see after the recipient submits its result?
- **Answer:** `completed`
- **Rationale:** [SPEC.md](SPEC.md) Section 5: A successful terminal submission updates task status to `completed`. Verified by `test_integration.py`.

### Question 3: Containerization
- **Question:** Which Docker option publishes a container's port to your machine?
- **Answer:** `-p`
- **Rationale:** `docker run -p <host_port>:<container_port>` binds container ports to host network interfaces.

### Question 4: Docker Compose & PostgreSQL
- **Question:** Which hostname should the API use to connect to the postgres service in Docker Compose?
- **Answer:** `postgres`
- **Rationale:** Docker Compose creates an isolated network where service names serve as DNS hostnames.

### Question 5: Kubernetes
- **Question:** Which Kubernetes resource keeps the requested number of application replicas running and manages updates?
- **Answer:** `Deployment`
- **Rationale:** Kubernetes `Deployment` controllers declare desired replica counts and orchestrate rolling updates for Pods.

### Question 6: CI/CD
- **Question:** What should happen if a test fails in this workflow?
- **Answer:** `Keep the existing version running and stop the deployment.`
- **Rationale:** Deployments are gated on passing tests. Failing tests halt the pipeline so production remains intact on the prior healthy version.

---

## How to Run

### Run tests locally
```bash
uv sync
uv run pytest -v
```

### Run with Docker Compose (PostgreSQL + API)
```bash
docker compose up --build -d
```

### Deploy to Kubernetes
```bash
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/agent-relay.yaml
```
