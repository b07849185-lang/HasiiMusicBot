# Hasii Music Bot - Systemd Service Guide

## 🎯 What This Does

Converts your bot from manual process to a **system service** that:
- ✅ Runs automatically in background
- ✅ Auto-restarts on crashes
- ✅ Auto-starts after server reboot
- ✅ Quick updates (3-5 seconds downtime)
- ✅ Professional log management

---

## 📋 Prerequisites

Before starting, make sure:
- ✅ Bot works with `bash start` command
- ✅ You have root/sudo access on VPS
- ✅ Bot is currently stopped (Ctrl+C)

---

## 🚀 Step-by-Step Setup on VPS

### **Step 1: Update Code on VPS**
```bash
cd /root/HasiiMusicBot
git pull
```

### **Step 2: Make Scripts Executable**
```bash
chmod +x setup_service.sh
chmod +x update_bot.sh
```

### **Step 3: Run Setup (One-Time)**
```bash
sudo ./setup_service.sh
```

**What happens:**
- Installs bot as system service
- Starts bot automatically
- Enables auto-start on server reboot

**Expected output:**
```
✅ Setup Complete!
● hasiimusic.service - Hasii Music Bot
     Loaded: loaded
     Active: active (running)
```

---

## 📱 Daily Usage

### **Check Bot Status**
```bash
systemctl status hasiimusic
```

### **View Live Logs**
```bash
journalctl -u hasiimusic -f
```
*(Press Ctrl+C to exit)*

### **Restart Bot**
```bash
systemctl restart hasiimusic
```

### **Stop Bot**
```bash
systemctl stop hasiimusic
```

### **Start Bot**
```bash
systemctl start hasiimusic
```

---

## 🔄 Updating Bot (New Way)

### **Option 1: Quick Update (Recommended)**
```bash
cd /root/HasiiMusicBot
./update_bot.sh
```
*Downtime: 3-5 seconds*

### **Option 2: Manual Update**
```bash
cd /root/HasiiMusicBot
git pull
systemctl restart hasiimusic
```

### **For Private Files (gitignored):**
```bash
# From your local machine:
scp tournament_player.py tournament_admin.py dicegame.py root@your-vps:/root/HasiiMusicBot/temp/
# Then move them on VPS and restart
```

---

## 🔧 Reverting to Old Way

If you want to go back to manual `bash start`:

```bash
# Stop and disable service
systemctl stop hasiimusic
systemctl disable hasiimusic

# Remove service file
sudo rm /etc/systemd/system/hasiimusic.service
systemctl daemon-reload

# Go back to manual mode
bash start
```

---

## ❓ Troubleshooting

### **Bot won't start after setup**
```bash
journalctl -u hasiimusic -n 50
```
Look for error messages at the bottom.

### **Check if service is running**
```bash
systemctl is-active hasiimusic
```
Should output: `active`

### **View full service configuration**
```bash
systemctl cat hasiimusic
```

### **Force restart**
```bash
systemctl restart hasiimusic
systemctl status hasiimusic
```

---

## 📊 Monitoring

### **Check if bot survived reboot**
```bash
# Reboot VPS
sudo reboot

# After reboot, check:
systemctl status hasiimusic
```

Should show `active (running)` automatically!

---

## ✅ Benefits You'll Notice

| Before | After |
|--------|-------|
| Terminal locked when bot runs | Terminal free, bot in background |
| Manual restart after crash | Auto-restart in 10 seconds |
| Manual start after reboot | Auto-start on reboot |
| 1-2 min update downtime | 3-5 sec update downtime |
| Logs scattered | Organized with journalctl |
| Must keep SSH open | Close SSH safely |

---

## 🎓 Learning Resources

- [systemd basics](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [journalctl guide](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)

---

**Ready to proceed? Follow the steps above carefully!**
