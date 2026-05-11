# VTU Exam Slot Monitor 🎓

Automated monitoring system for VTU exam slot availability that runs 24/7 on GitHub Actions and sends email alerts when slots become available.

## 🌟 Features

- ✅ Runs automatically every 5 minutes (configurable)
- ✅ Works 24/7 even when your laptop is off
- ✅ Monitors multiple course IDs simultaneously
- ✅ Sends beautiful HTML email alerts
- ✅ Completely FREE (GitHub Actions free tier)
- ✅ No server or hosting required
- ✅ Easy to set up in 10 minutes

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Gmail Account** with App Password enabled

## 🚀 Setup Instructions

### Step 1: Get Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** (left sidebar)
3. Enable **2-Step Verification** if not already enabled
4. Search for "App passwords" or go to: https://myaccount.google.com/apppasswords
5. Create a new app password:
   - App: Select "Mail"
   - Device: Select "Other" and name it "VTU Monitor"
6. **Copy the 16-character password** (you'll need this later)

### Step 2: Fork This Repository

1. Click the **"Fork"** button at the top right of this page
2. This creates your own copy of the repository

### Step 3: Add Secrets to Your Repository

1. Go to your forked repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each of the following:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `VTU_USERNAME` | Your VTU USN (username) | `1CR21CS001` |
| `VTU_PASSWORD` | Your VTU portal password | `YourPassword123` |
| `EMAIL_FROM` | Your Gmail address | `youremail@gmail.com` |
| `EMAIL_PASSWORD` | Gmail App Password (16 chars) | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | Email where you want alerts | `youremail@gmail.com` or any email |
| `COURSE_IDS` | Course IDs to monitor (comma-separated) | `189,18` |

**Important Notes:**
- For `EMAIL_PASSWORD`, use the 16-character App Password from Step 1, NOT your regular Gmail password
- `EMAIL_FROM` and `EMAIL_TO` can be the same email address
- Remove spaces from the App Password when entering it

### Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The workflow will now run automatically every 5 minutes

### Step 5: Test It Manually (Optional)

1. Go to **Actions** tab
2. Click on **"VTU Slot Monitor"** workflow
3. Click **"Run workflow"** → **"Run workflow"** button
4. Wait 30-60 seconds and check the run results
5. Click on the run to see logs

## ⚙️ Configuration

### Change Check Frequency

Edit `.github/workflows/check_slots.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
```

**Common intervals:**
- Every 5 minutes: `*/5 * * * *`
- Every 10 minutes: `*/10 * * * *`
- Every 30 minutes: `*/30 * * * *`
- Every hour: `0 * * * *`

**Note:** GitHub Actions may have a 3-5 minute delay, so don't set intervals too low.

### Monitor Different Courses

Update the `COURSE_IDS` secret with comma-separated course IDs:
- For courses 189 and 18: `189,18`
- For only course 189: `189`
- For courses 189, 18, and 20: `189,18,20`

## 📧 Email Alert Preview

When slots are available, you'll receive an email like this:

```
Subject: 🎉 VTU Exam Slots Available - Course 189

✅ Exam slots are NOW AVAILABLE for Course ID 189

📋 Details:
Course ID: 189
Time Detected: 2026-05-11 15:30:00 IST
Status: AVAILABLE

📊 Slot Data:
[Available dates and times will be shown here]

🔗 Book Your Slot Now (button linking to VTU portal)
```

## 🔍 Monitoring & Logs

### View Execution Logs

1. Go to **Actions** tab
2. Click on any workflow run
3. Click on **"check-slots"** job
4. Expand **"Check VTU Slots"** step to see detailed logs

### Check Status

- Green checkmark ✅ = Workflow ran successfully
- Red X ❌ = Workflow failed (check logs for errors)
- Yellow dot 🟡 = Workflow is running

## 📊 What Happens When Slots Are Found?

1. ✅ Script detects available slots
2. 📧 HTML email sent to your configured address
3. 📝 Detailed slot information included
4. 🔗 Direct link to VTU portal included
5. ⏰ Timestamp of when slots were found

## 🛠️ Troubleshooting

### Problem: Workflow not running

**Solution:**
- Ensure Actions are enabled in Settings → Actions
- Check if all secrets are properly configured
- Manually trigger workflow to test

### Problem: Login failed

**Solution:**
- Verify VTU_USERNAME and VTU_PASSWORD are correct
- Try logging in manually on VTU portal to confirm credentials
- Check if your account is locked or requires password reset

### Problem: Email not sending

**Solution:**
- Verify EMAIL_PASSWORD is the App Password (16 chars), not your regular Gmail password
- Ensure 2-Step Verification is enabled on Gmail
- Check if EMAIL_FROM is correct
- Try regenerating the App Password

### Problem: "No slots available" every time

**Solution:**
- This is normal! The script is working correctly
- It will send an email ONLY when slots become available
- Keep the monitor running - it checks automatically

## 🔒 Security & Privacy

- ✅ All credentials stored as GitHub Secrets (encrypted)
- ✅ Secrets are never exposed in logs
- ✅ Code runs in isolated GitHub Actions environment
- ✅ No third-party services involved
- ✅ You have full control over your data

## 💡 Tips

1. **Don't disable the workflow** - keep it running continuously
2. **Check spam folder** - first email might go to spam
3. **Add to contacts** - prevent future emails from going to spam
4. **Test manually first** - use "Run workflow" to verify setup
5. **Monitor logs occasionally** - ensure everything is working

## 📱 Mobile Notifications

To get instant mobile notifications:
1. Use Gmail app on your phone
2. Enable notifications for your Gmail account
3. You'll get instant push notifications when email arrives

## ⚠️ GitHub Actions Limits

- **Free tier**: 2,000 minutes/month
- **Usage per run**: ~1 minute
- **Your usage**: Running every 5 minutes = ~8,640 runs/month
- **Don't worry**: This only uses ~144 minutes/month (well within limits!)

## 🎯 Course IDs Reference

Common VTU course IDs (update based on your needs):
- **189**: B.E/B.Tech Exam Registrations - PEC and OEC
- **18**: (Your specific course - verify from VTU portal)

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the workflow logs in Actions tab
3. Ensure all secrets are correctly configured
4. Try running the workflow manually first

## 🎉 Success!

Once set up, you can:
- ✅ Close your laptop
- ✅ Turn off your computer
- ✅ Go about your day
- ✅ Get notified instantly when slots open

The monitor runs 24/7 in the cloud!

## 📄 License

Free to use for VTU students. No license restrictions.

## 🙏 Credits

Built with ❤️ for VTU students to never miss an exam slot booking opportunity!

---

**⭐ Pro Tip**: Star this repository to easily find it later, and watch it for updates!
