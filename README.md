# 🛠️ Hướng dẫn Setup Jenkins UI

## Bước 1: Chạy Jenkins Container và hướng dẫn cấu hình đăng nhập 

Chạy lệnh này trong terminal (PowerShell hoặc Git Bash trên Windows):


**Chạy Docker Compose:**
```powershell
# Di chuyển vào thư mục jenkins
cd jenkins

# Khởi động Jenkins
docker-compose up -d

# Kiểm tra container đã chạy chưa
docker ps
```

**Đợi 30-60 giây** để Jenkins khởi động hoàn tất.

---

## Bước 1.1: Đăng nhập Jenkins

Truy cập: **http://localhost:8080**

### **Lần đầu tiên chạy Jenkins**

Nếu đây là lần đầu tiên, Jenkins sẽ yêu cầu bạn nhập **Initial Admin Password**:

```powershell
# Lấy mật khẩu đăng nhập lần đầu
docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
```

**Output ví dụ:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Các bước:**
1. Copy mật khẩu từ terminal
2. Paste vào ô **Administrator password** trên Jenkins UI
3. Click **Continue**
4. Chọn **Install suggested plugins** (hoặc **Select plugins to install** nếu muốn tùy chỉnh)
5. Đợi plugins cài xong
6. Tạo **Admin User** (username, password, email)
7. Click **Save and Continue** → **Start using Jenkins**


---

## Bước 2: Cài đặt Plugins

1. Vào **Manage Jenkins** (bên trái sidebar)
2. Click **Plugins** (hoặc **Manage Plugins**)
3. Chọn tab **Available plugins**
4. Search và tick vào các plugins sau:
   - **Git plugin** 
   - **GitHub plugin**
   - **Docker plugin**
   - **Docker Pipeline**
   - **Pipeline**
   - **Pipeline: Stage View**


5. Click **Install** (không cần restart)
6. Đợi cài đặt hoàn tất

---

## Bước 3: Cấu hình Docker Hub Credentials 

1. Vào **Manage Jenkins** → **Credentials**
2. Click vào **(global)** domain
3. Click **Add Credentials** (bên trái)
4. Điền thông tin:
   - **Kind**: `Username with password`
   - **Scope**: `Global`
   - **Username**: `<your-dockerhub-username>`
   - **Password**: `<your-dockerhub-password hoặc access-token>`
   - **ID**: `dockerhub-credentials` (QUAN TRỌNG - phải đúng tên này)
   - **Description**: `Docker Hub Credentials`
5. Click **Create**

### Cách lấy Docker Hub Access Token:
1. Đăng nhập vào https://hub.docker.com
2. Vào **Account Settings** → **Security** → **Access Tokens**
3. Click **Generate New Token**
4. Copy token và dùng làm password

---

## Bước 4: Tạo Pipeline Job 

1. Từ Dashboard, click **New Item** (bên trái)
2. Điền thông tin:
   - **Enter an item name**: `iris-ml-cicd` (hoặc tên bạn muốn)
   - **Type**: Chọn **Pipeline**
3. Click **OK**

---

## Bước 5: Cấu hình Pipeline 

### A. General Section:
-  Tick **GitHub project**
- **Project url**: `https://github.com/<your-username>/<your-repo>/`

### B. Build Triggers:
-  Tick **GitHub hook trigger for GITScm polling**
  (Để nhận trigger từ GitHub webhook)

### C. Pipeline Section:
- **Definition**: Chọn `Pipeline script from SCM`
- **SCM**: Chọn `Git`
- **Repository URL**: `https://github.com/<your-username>/<your-repo>.git`
- **Credentials**: 
  - Nếu repo public: để trống
  - Nếu repo private: Add credentials GitHub
- **Branch Specifier**: `*/main` (hoặc `*/master` nếu dùng branch master)
- **Script Path**: `Jenkinsfile`

### D. Lưu cấu hình:
Click **Save** ở cuối trang

---

## Bước 6: Cập nhật Jenkinsfile với Docker Hub Username 

1. Mở file `jenkins-code/Jenkinsfile`
2. Tìm dòng:
   ```groovy
   DOCKER_IMAGE = "your-dockerhub-username/iris-ml-api"
   ```
3. Thay `your-dockerhub-username` bằng username thật của bạn:
   ```groovy
   DOCKER_IMAGE = "myusername/iris-ml-api"
   ```
4. Save file

---

## Bước 7: Push Code lên GitHub 

```bash
# Khởi tạo git (nếu chưa có)
cd jenkins-code
git init

# Add remote repository
git remote add origin https://github.com/<your-username>/<your-repo>.git

# Add và commit
git add .
git commit -m "Setup CI/CD pipeline with Jenkins"

# Push lên GitHub
git branch -M main
git push -u origin main
```

---

## Bước 8: Setup GitHub Webhook 

### Option A: Jenkins Public (có domain hoặc IP public)
1. Vào GitHub repository → **Settings** → **Webhooks** → **Add webhook**
2. Điền:
   - **Payload URL**: `http://your-jenkins-url:8080/github-webhook/`
   - **Content type**: `application/json`
   - **Which events**: `Just the push event`
   -  Active
3. Click **Add webhook**

### Option B: Jenkins Local (dùng ngrok) 

**Nếu Jenkins chạy trên local machine:**

1. Tải ngrok: https://ngrok.com/download
2. Chạy ngrok:
   ```bash
   ngrok http 8080
   ```
3. Copy URL ngrok (ví dụ: `https://abc123.ngrok.io`)
4. Vào GitHub webhook và dùng: `https://abc123.ngrok.io/github-webhook/`

 **Lưu ý**: Mỗi lần restart ngrok, URL sẽ thay đổi (bản free)

---

## Bước 9: Test Pipeline Manually 

1. Vào job `iris-ml-cicd` trong Jenkins
2. Click **Build Now**
3. Xem Console Output để theo dõi progress
4. Pipeline sẽ chạy qua các stages:
   - ✅ Checkout
   - ✅ Setup Python Environment
   - ✅ Train Model
   - ✅ Test Model
   - ✅ Test API
   - ✅ Build Docker Image
   - ✅ Push to Docker Hub
   - ✅ Cleanup

---

## Bước 10: Test GitHub Webhook 

1. Thay đổi một file bất kỳ trong repo (ví dụ: README.md)
2. Commit và push:
   ```bash
   git add .
   git commit -m "Test webhook trigger"
   git push
   ```
3. Jenkins sẽ **TỰ ĐỘNG** trigger build!
4. Kiểm tra trong Jenkins Dashboard

---


## Troubleshooting

### Jenkins không build Docker image:
```bash
# Kiểm tra Jenkins có access Docker không
docker exec jenkins-server docker ps
```

### Permission denied khi build:
```bash
docker exec -u root jenkins-server chmod 666 /var/run/docker.sock
docker exec -u root jenkins-server chown -R jenkins:jenkins /var/jenkins_home
```

### GitHub webhook không trigger:
- Kiểm tra webhook delivery trong GitHub Settings → Webhooks → Recent Deliveries
- Đảm bảo Jenkins URL accessible từ internet (dùng ngrok nếu local)
- Kiểm tra "GitHub hook trigger" đã tick trong job config

### Build fails ở stage "Push to Docker Hub":
- Kiểm tra credentials ID đúng là `dockerhub-credentials`
- Đăng nhập Docker Hub và kiểm tra token còn valid
- Thử login thủ công: `docker login`

### Python tests fail:
```bash
# Kiểm tra requirements.txt có đầy đủ
# Kiểm tra Python version (cần >= 3.8)
```

---

##  Kết quả

Sau khi setup xong:
1. Mỗi lần push code → Jenkins tự động build
2. Model được train và test
3. API được test
4. Docker image được build và push lên Docker Hub
5. Có thể pull và chạy: 
   ```bash
   docker pull your-username/iris-ml-api:latest
   docker run -p 8000:8000 your-username/iris-ml-api:latest
   ```
6. Truy cập: http://localhost:8000/docs để test API

**Happy CI/CD! **

