# Render Deployment Guide

## Pre-deployment Checklist

Before deploying to Render, run the verification script:
```bash
python verify_deployment.py
```

## Environment Variables to Set in Render

When deploying to Render, you need to configure the following environment variables in your Render dashboard:

### Required Environment Variables:

1. **FLASK_ENV**
   - Value: `production`
   - Description: Sets Flask to production mode

2. **FLASK_DEBUG**
   - Value: `false`
   - Description: Disables debug mode for production

3. **MODEL_PATH**
   - Value: `best_model.pkl`
   - Description: Path to the machine learning model file

### Optional Environment Variables:

4. **LOG_LEVEL**
   - Value: `INFO` (default) or `DEBUG`, `WARNING`, `ERROR`
   - Description: Controls logging verbosity

**Note:** PORT is automatically set by Render, do not set it manually.

### How to Set Environment Variables in Render:

1. Go to your Render dashboard
2. Select your web service
3. Go to the "Environment" tab
4. Add each environment variable with its corresponding value
5. Click "Save Changes"

### Build Command:
```
pip install -r requirements.txt
```

### Start Command:
```
gunicorn main:app --host=0.0.0.0 --port=$PORT
```

## Deployment Steps:

1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create a new Web Service in Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository

3. **Configure the service:**
   - **Name:** Choose a name for your service (e.g., `heart-attack-prediction`)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app --host=0.0.0.0 --port=$PORT`

4. **Set Environment Variables** (as listed above)

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for the build and deployment to complete

## Post-deployment Verification

After deployment, test these endpoints:

1. **Health Check:**
   ```
   GET https://your-app-name.onrender.com/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "model_loaded": true,
     "environment": "production",
     "timestamp": "2025-01-14T...",
     "version": "1.0.0"
   }
   ```

2. **Model Information:**
   ```
   GET https://your-app-name.onrender.com/model-info
   ```

3. **Main Application:**
   ```
   GET https://your-app-name.onrender.com/
   ```

## Monitoring and Logs

- **Access logs:** Go to your service in Render Dashboard → "Logs" tab
- **Health monitoring:** Use the `/health` endpoint for uptime monitoring
- **Performance:** Monitor through Render's metrics dashboard

## Troubleshooting Common Issues

### 1. Model Loading Errors
```
ERROR: No se pudo cargar el modelo
```
**Solution:** Ensure `best_model.pkl` is committed to your repository and the `MODEL_PATH` environment variable is correct.

### 2. Port Binding Issues
```
Error: Port already in use
```
**Solution:** Render automatically sets the PORT environment variable. Don't override it.

### 3. Import Errors
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution:** Check `requirements.txt` includes all necessary packages.

### 4. Memory Issues
**Solution:** Consider upgrading to a higher tier Render plan if the model is large.

## Important Notes:

- **Free Tier Limitations:** Render's free tier may have cold starts and limited resources
- **File Persistence:** Uploaded files won't persist across deployments on free tier
- **Environment Variables:** Are case-sensitive
- **Logs:** Check logs regularly for any errors or warnings
- **SSL:** Render provides automatic HTTPS

## Updating Your Deployment

To update your deployed application:

1. Make changes to your code
2. Commit and push to your repository
3. Render will automatically redeploy

For environment variable changes:
1. Update variables in Render Dashboard
2. Restart the service if needed

## Custom Domain (Optional)

To use a custom domain:
1. Go to your service settings
2. Add your custom domain
3. Update your DNS records as instructed

---

**Need Help?**
- [Render Documentation](https://render.com/docs)
- [Render Support](https://render.com/support)
- Check the application logs in your Render dashboard
