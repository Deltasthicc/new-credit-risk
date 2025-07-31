# PowerShell script to test all MCP agent endpoints with edge cases

# 🌐 Base NGROK URL (change here only)
$NGROK_URL = "https://be2c4e1372e8.ngrok-free.app"

# 🔍 Standard financial summary
$summary = 'XYZ Ltd. is a fintech company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India.'

# 🚀 Test standard POST /
Write-Host "`n🚀 Running test with summary data (POST /)"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d "{`"summary`": `"$summary`"}"

# 📊 Test structured data
Write-Host "`n📊 Running test with structured data (POST /)"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{"Revenue": 2500000000, "Net_Income": 200000000, "Total_Assets": 3000000000, "Industry": "IT Services", "Country": "India"}'

# 🧪 Edge Case: All zero values
Write-Host "`n🧪 Test with all zero values"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{"Revenue": 0, "Net_Income": 0, "Total_Assets": 0, "Industry": "IT Services", "Country": "India"}'

# 🧪 Edge Case: Extremely large values
Write-Host "`n🧪 Test with extremely large values"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{"Revenue": 99999999999999, "Net_Income": 88888888888888, "Total_Assets": 77777777777777, "Industry": "AI Megacorp", "Country": "Utopia"}'

# 🧪 Edge Case: Missing keys
Write-Host "`n🧪 Test with missing keys"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{"Revenue": 1000000000}'

# 🧪 Edge Case: Empty body
Write-Host "`n🧪 Test with empty body"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{}'

# 🧪 Edge Case: Invalid JSON (unquoted key)
Write-Host "`n🧪 Test with invalid JSON"
curl.exe -X POST "$NGROK_URL/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  --data "{summary: 'Missing quotes'}"

# 🔍 Individual agents
Write-Host "`n🔍 Running fraud detection (POST /fraud)"
curl.exe -X POST "$NGROK_URL/fraud" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d "{`"summary`": `"$summary`"}"

Write-Host "`n📈 Running credit scoring (POST /credit)"
curl.exe -X POST "$NGROK_URL/credit" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d "{`"summary`": `"$summary`"}"

Write-Host "`n⚖️ Running compliance check (POST /compliance)"
curl.exe -X POST "$NGROK_URL/compliance" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d "{`"summary`": `"$summary`"}"

# ❤️ Health and ℹ️ Info
Write-Host "`n❤️ Checking health (GET /health)"
curl.exe -X GET "$NGROK_URL/health"

Write-Host "`nℹ️ Checking info (GET /info)"
curl.exe -X GET "$NGROK_URL/info"
