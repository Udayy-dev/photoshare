# Cloud Project Report: PhotoShare on Google App Engine

**Scenario:** A startup hires a junior cloud developer to prototype a photo-sharing tool quickly, without managing VMs, load balancers or downtime. Chosen platform: Google Cloud (PaaS: App Engine).

## Task 1 – Infrastructure, CapEx vs OpEx
Illustrative estimates for ~10,000 users (prices approximate; check current pricing).

| | On-premise (traditional) | Google Cloud (PaaS) |
|---|---|---|
| **CapEx** (one-time) | 2 servers ~₹6,00,000; storage array ~₹3,00,000; load balancer ~₹2,00,000; switches/firewall ~₹1,50,000; UPS/rack/cooling ~₹1,50,000. **≈ ₹14 lakh** | **₹0** |
| **OpEx** (monthly) | Electricity, internet, sysadmin salary, maintenance, backups: **≈ ₹80,000–1,00,000/mo** | App Engine F1 instances (free quota, then ~₹5/hr each), Cloud Storage ~₹1.7/GB/mo, egress: **≈ ₹0–3,000/mo at prototype scale** |
| Scaling | Buy hardware in advance | Automatic, pay per use |
| Downtime mgmt | You | Google (99.95% SLA) |

**Conclusion:** the cloud converts CapEx to OpEx, which suits a startup.

## Task 2 – Application and deployment
App: **PhotoShare** (upload and view photos and mp4 videos). Stack: Flask on App Engine Standard + Cloud Storage. Code is in `main.py`, config in `app.yaml`, steps in `deploy.md`.
**Auto-scaling verification:** `app.yaml` sets min 0, max 5 instances and a 50% CPU target. Run `loadtest.sh`, then open Console → App Engine → Instances to see the count rise from 1 to several and drop back to 0 when idle. Screenshot this for submission.

## Task 3 – App Engine vs AWS EC2
| Feature | Google App Engine (PaaS) | AWS EC2 (IaaS) |
|---|---|---|
| Service model | PaaS | IaaS |
| Server management | None; Google patches OS/runtime | You manage OS, patches, security |
| Load balancing | Built in | Set up ELB/ALB yourself |
| Auto-scaling | Built in, scales to zero | Auto Scaling Groups, configured by you |
| Control | Limited (runtime sandbox) | Full root access, any software |
| Pricing | Per instance-hour of use, free quota | Per hour while the VM runs, even idle |
| Setup speed | `gcloud app deploy` | Launch VM, install, configure |
| **Common to both** | Pay-as-you-go, multi-region, HTTPS, monitoring (Cloud Monitoring / CloudWatch), integrates with storage (GCS / S3), free tier available |

For a prototype with no ops team, App Engine fits best. EC2 fits when custom OS-level software is needed.

## Task 4 – Images/videos, security, privacy, free tier
- **Media storage:** Cloud Storage bucket (object storage), not on instance disk.
- **Security:** HTTPS enforced (`secure: always`); file-type allowlist and 25 MB limit; random filenames (no path traversal); IAM least-privilege service account (Storage Object Admin on that bucket only).
- **Privacy:** bucket is private with public-access prevention on; the app serves media through `/media/`, so you can add login or per-user checks. Data is encrypted at rest by default and in transit via TLS.
- **Free tier ("freewares"):** App Engine F1 free quota, 5 GB Cloud Storage (US regions), Cloud Shell, Flask/gunicorn (open source).
- **Deploy and configure:** see `deploy.md`.

## Task 5 – Google File System (GFS) in this app
GFS (Ghemawat et al., 2003) is Google's internal distributed file system. It is not a public service, but Cloud Storage is built on its successor, Colossus, so PhotoShare uses its design indirectly. Its principles:
- Files are split into **64 MB chunks**, each **replicated on 3 chunkservers** (fault tolerance, so an uploaded photo survives disk or machine failure).
- A single **master** holds metadata (file → chunk mapping); clients then talk to chunkservers directly for data.
- Optimized for large files and append-heavy writes, which suits photos and videos.

**Flow:** the user uploads → App Engine → Cloud Storage → stored as replicated chunks. Read: the app fetches the object and streams it to the browser.
**Implementing it yourself** (concept demo): run a master plus 3 chunkserver VMs on Compute Engine, split uploads into chunks and store each on 3 servers. For the assignment, explaining the architecture plus using Cloud Storage is the practical answer.
