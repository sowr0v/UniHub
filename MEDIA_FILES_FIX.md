# Media Files Not Showing - 404 Error

## The Problem

You're getting:
```
GET https://unihub-fm2d.onrender.com/media/universities/Varendra_University.jpg 404 (Not Found)
```

## Root Cause

**Render's free tier has an EPHEMERAL filesystem**, which means:
- ✅ You can upload files
- ✅ Files are saved temporarily
- ❌ Files are DELETED when the service restarts/redeploys
- ❌ Media files are NOT served in production by default

## Why This Happens

1. **Ephemeral Filesystem**: On Render free tier, the filesystem resets on every deploy
2. **No Media Serving**: Django doesn't serve media files in production (DEBUG=False)
3. **No Persistent Storage**: Free tier doesn't include persistent disk

## Solutions (Choose One)

### Solution 1: Use Cloudinary (FREE & RECOMMENDED) ⭐

Cloudinary provides free cloud storage for images.

#### Step 1: Install Cloudinary
Add to `requirements.txt`:
```
cloudinary>=1.36.0
django-cloudinary-storage>=0.3.0
```

#### Step 2: Sign up for Cloudinary
1. Go to: https://cloudinary.com/users/register/free
2. Sign up (free tier: 25GB storage, 25GB bandwidth/month)
3. Get your credentials from dashboard

#### Step 3: Update Settings
Add to `unihub/settings.py`:

```python
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Update INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Add this BEFORE cloudinary
    'cloudinary',          # Add this
    'universities',
    # ... rest of your apps
]

# Update STORAGES
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

#### Step 4: Add Environment Variables on Render
```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

#### Step 5: Redeploy
All new uploads will go to Cloudinary automatically!

---

### Solution 2: Use AWS S3 (More Complex)

AWS S3 provides reliable cloud storage but requires more setup.

#### Step 1: Install boto3
Add to `requirements.txt`:
```
boto3>=1.28.0
django-storages>=1.14.0
```

#### Step 2: Create S3 Bucket
1. Sign up for AWS
2. Create S3 bucket
3. Set bucket policy for public read
4. Get access keys

#### Step 3: Update Settings
```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'

# Update INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'storages',
]

# Update STORAGES
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

---

### Solution 3: Upgrade to Render Paid Plan ($7/month)

Render's paid plan includes:
- ✅ Persistent disk storage
- ✅ Files survive restarts/redeploys
- ✅ Better performance

#### How to Enable:
1. Upgrade to paid plan
2. Add persistent disk in Render dashboard
3. Mount disk to `/opt/render/project/src/media`
4. No code changes needed!

---

### Solution 4: Temporary Fix - Serve Media in Production (NOT RECOMMENDED)

**⚠️ WARNING**: This is NOT recommended for production but works for testing.

Update `unihub/urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing urls
]

# Serve media files in production (NOT RECOMMENDED)
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Problems with this approach**:
- Files still get deleted on redeploy
- Poor performance
- Not scalable
- Security concerns

---

## Recommended Solution: Cloudinary

I recommend **Cloudinary** because:
- ✅ Free tier is generous (25GB storage)
- ✅ Easy to set up (5 minutes)
- ✅ Automatic image optimization
- ✅ CDN included (fast delivery)
- ✅ No code changes to models
- ✅ Works with Django admin
- ✅ Reliable and scalable

## Quick Setup: Cloudinary (Step by Step)

### 1. Sign Up
Visit: https://cloudinary.com/users/register/free

### 2. Get Credentials
After signup, go to Dashboard and copy:
- Cloud Name
- API Key
- API Secret

### 3. Update Code

Add to `requirements.txt`:
```
cloudinary>=1.36.0
django-cloudinary-storage>=0.3.0
```

Update `unihub/settings.py` - add after imports:
```python
import cloudinary
import cloudinary.uploader
import cloudinary.api
```

Add to `INSTALLED_APPS` (BEFORE your apps):
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Add this
    'cloudinary',          # Add this
    'universities',
    # ... rest
]
```

Update `STORAGES` section:
```python
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

Add Cloudinary config (before STORAGES):
```python
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
```

### 4. Add Environment Variables on Render

Go to Render Dashboard → Environment:
```
CLOUDINARY_CLOUD_NAME = your_cloud_name_here
CLOUDINARY_API_KEY = your_api_key_here
CLOUDINARY_API_SECRET = your_api_secret_here
```

### 5. Deploy
```bash
git add .
git commit -m "Add Cloudinary for media storage"
git push origin main
```

### 6. Re-upload Images
- Login to admin
- Re-upload university images
- They'll now be stored on Cloudinary
- Images will persist across deploys!

## Testing

After setup:
1. Upload an image in admin
2. Check the image URL - should be `res.cloudinary.com/...`
3. Image should load on the site
4. Redeploy - image should still be there!

## Comparison Table

| Solution | Cost | Setup | Persistence | Performance |
|----------|------|-------|-------------|-------------|
| **Cloudinary** | Free (25GB) | Easy | ✅ Yes | ⭐⭐⭐⭐⭐ |
| AWS S3 | ~$0.023/GB | Medium | ✅ Yes | ⭐⭐⭐⭐⭐ |
| Render Paid | $7/month | Easy | ✅ Yes | ⭐⭐⭐⭐ |
| Serve in Prod | Free | Easy | ❌ No | ⭐⭐ |

## Summary

**Current Issue**: Media files are deleted on every deploy (Render free tier limitation)

**Best Solution**: Use Cloudinary (free, easy, reliable)

**Steps**:
1. Sign up for Cloudinary (free)
2. Add cloudinary packages to requirements.txt
3. Update settings.py
4. Add environment variables on Render
5. Redeploy
6. Re-upload images

After this, all uploaded images will be stored on Cloudinary's CDN and will persist across deploys! 🎉
