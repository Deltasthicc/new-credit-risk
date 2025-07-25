$summary = "The company has ₹120 Cr annual revenue, 400 employees, and is late on regulatory filings."

$agents = @("bureau", "credit_scoring", "fraud", "compliance", "explainability")

foreach ($agent in $agents) {
    Write-Host "=== Running agent: $agent ==="
    curl.exe -X POST "http://localhost:5000/run-agent/$agent" `
      -H "Content-Type: application/json" `
      -d "{ `"summary`": `"$summary`" }"
    Write-Host "`n`n"
}