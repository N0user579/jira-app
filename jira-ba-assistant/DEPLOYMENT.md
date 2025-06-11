# Vercel Deployment Instructions

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket
3. **API Keys**: Have your Jira and Gemini API credentials ready

## Step 1: Prepare Your Repository

1. **Push your code** to your Git repository with the new Vercel-compatible structure
2. **Ensure all files** are in the correct locations:
   - `api/` folder contains Python serverless functions
   - `public/` folder contains static files (HTML, CSS, JS)
   - `vercel.json` is in the root directory

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your Git repository**
4. **Configure the project**:
   - Framework Preset: `Other`
   - Root Directory: `./` (leave as default)
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   \`\`\`bash
   npm i -g vercel
   \`\`\`

2. **Login to Vercel**:
   \`\`\`bash
   vercel login
   \`\`\`

3. **Deploy from your project directory**:
   \`\`\`bash
   vercel
   \`\`\`

## Step 3: Configure Environment Variables

In your Vercel project dashboard, go to **Settings > Environment Variables** and add:

### Required Environment Variables

\`\`\`
JIRA_BASE_URL=https://projectmajorvd25.atlassian.net
JIRA_EMAIL=projectmajorvd25@gmail.com
JIRA_API_TOKEN=ATATT3xFfGF0q6zrwXK9XZ41sPd45L5k_tDT5jiMEN-eNVpUUqEZf59in2eTEHx5My088ze37UWE9YaZoMv5FSEnffxQA9Lv-24FI3e-yUPsvJ8tbC4ivhTIvg4FP-Bc9wf0Rv9SSHhEmubio670X4gIQcAWlqjkljTR-jFj2AD7hwyEx5mG_mw=EB60AD91
GEMINI_API_KEY=AIzaSyCX7vTo9sXovapnD-cvKiJbe2NKpP7bBXs
\`\`\`

### How to Add Environment Variables

1. **In Vercel Dashboard**:
   - Go to your project
   - Click **Settings** tab
   - Click **Environment Variables** in the sidebar
   - Add each variable with its value
   - Select **Production**, **Preview**, and **Development** for each

2. **Via Vercel CLI**:
   \`\`\`bash
   vercel env add JIRA_BASE_URL
   vercel env add JIRA_EMAIL
   vercel env add JIRA_API_TOKEN
   vercel env add GEMINI_API_KEY
   \`\`\`

## Step 4: Redeploy

After adding environment variables:

1. **Trigger a new deployment**:
   - Push a new commit to your repository, OR
   - In Vercel dashboard, go to **Deployments** and click **Redeploy**

## Step 5: Test Your Deployment

1. **Visit your Vercel URL** (e.g., `https://your-project.vercel.app`)
2. **Test the main features**:
   - Projects should load on the homepage
   - Project pages should display correctly
   - AI generation should work
   - Issue creation should work

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Ensure `requirements.txt` is in the root directory
   - Check that all Python dependencies are listed

2. **Environment variables not working**:
   - Verify all variables are set in Vercel dashboard
   - Ensure you've redeployed after adding variables
   - Check variable names match exactly

3. **API endpoints not working**:
   - Check the `vercel.json` configuration
   - Ensure API files are in the `api/` directory
   - Verify function names match the file names

4. **Static files not loading**:
   - Ensure CSS/JS files are in the `public/` directory
   - Check file paths in HTML files start with `/`

### Debug Mode

To enable debug logging:

1. **Add environment variable**:
   \`\`\`
   DEBUG=1
   \`\`\`

2. **Check function logs** in Vercel dashboard under **Functions** tab

### Performance Optimization

1. **Cold starts**: Serverless functions may have cold start delays
2. **Caching**: Vercel automatically caches static files
3. **Function timeout**: Default is 10 seconds, can be increased in Pro plans

## Custom Domain (Optional)

1. **In Vercel Dashboard**:
   - Go to **Settings > Domains**
   - Add your custom domain
   - Follow DNS configuration instructions

## Monitoring

1. **Analytics**: Available in Vercel dashboard
2. **Error tracking**: Check **Functions** tab for errors
3. **Performance**: Monitor response times in dashboard

## Security Notes

1. **Environment variables** are encrypted and secure in Vercel
2. **API tokens** are not exposed to the client-side
3. **HTTPS** is enabled by default on all Vercel deployments

Your Jira BA Assistant should now be successfully deployed on Vercel! 🚀
