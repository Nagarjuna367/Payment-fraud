# Network Access Configuration

## Flask App is Now Running on All Network Interfaces ✅

The fraud detection application is now accessible from **any device on your network**.

---

## 📍 How to Access

### From the Same Computer (where Flask is running):
```
http://127.0.0.1:5000
http://localhost:5000
```

### From Other Devices on the Network:
Your machine has these network IPs:
```
http://192.168.56.1:5000
http://192.168.55.103:5000
```

**Choose one of the above depending on which network interface the other device connects to.**

---

## 🌐 Available Routes from Any Device

Once you access the app from another device, you can use:

- **Home Page**: `http://[YOUR_IP]:5000/`
- **Prediction Form**: `http://[YOUR_IP]:5000/predict`
- **Results Page**: `http://[YOUR_IP]:5000/submit` (POST from form)
- **API Predict**: `http://[YOUR_IP]:5000/api/predict` (POST JSON)
- **API Stats**: `http://[YOUR_IP]:5000/api/stats`
- **API Health**: `http://[YOUR_IP]:5000/api/health`

Replace `[YOUR_IP]` with either `192.168.56.1` or `192.168.55.103`

---

## 📱 Examples

### From Laptop on Same Network:
```
Open Browser: http://192.168.56.1:5000/predict
```

### From Mobile Phone on Same Network:
```
Open Browser: http://192.168.56.1:5000/
```

### From Another Computer:
```
Open Browser: http://192.168.55.103:5000/predict
```

---

## 🔌 API Usage from Other Devices

```bash
curl -X POST http://192.168.56.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "step": 100,
    "type": "TRANSFER",
    "amount": 1500.00,
    "oldbalanceOrg": 50000.00,
    "newbalanceOrig": 48500.00,
    "oldbalanceDest": 30000.00,
    "newbalanceDest": 31500.00,
    "currency": "USD"
  }'
```

---

## ⚙️ Technical Configuration

**Flask Configuration Changed:**
- **Before**: `host='127.0.0.1'` (localhost only)
- **After**: `host='0.0.0.0'` (all network interfaces)
- **Port**: 5000 (same)
- **Debug**: Enabled for development

---

## ✅ What Works Now

1. ✅ Access web interface from any device on network
2. ✅ Submit fraud detection forms from other devices
3. ✅ Use API endpoints from other devices
4. ✅ All features work identically without disturbance
5. ✅ Same currency support (USD, EUR, GBP, INR, JPY)
6. ✅ Real-time results and predictions

---

## ⚠️ Troubleshooting

**Can't connect from another device?**
1. Ensure both devices are on same network (WiFi or LAN)
2. Check Windows Firewall allows port 5000:
   ```powershell
   netsh advfirewall firewall add rule name="Flask" dir=in action=allow protocol=tcp localport=5000
   ```
3. Try the other IP address (192.168.56.1 or 192.168.55.103)
4. Ping the server from other device:
   ```
   ping 192.168.56.1
   ```

---

## 📊 Server Status

To check if server is running and accessible:
```
http://[YOUR_IP]:5000/api/health
```

This will return JSON showing server status, model loaded status, and current timestamp.

---

**The Flask app will continue running until you press CTRL+C in the terminal.**
