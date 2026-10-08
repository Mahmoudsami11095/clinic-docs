$loginUrl = "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/auth/login"
$loginPayload = @{
    email = "msami11095@gmail.com"
    password = "Sami@11095"
} | ConvertTo-Json

Write-Host "Attempting live login..."
try {
    $loginRes = Invoke-RestMethod -Uri $loginUrl -Method Post -ContentType "application/json" -Body $loginPayload
    Write-Host "Login Success! User: $($loginRes.data.name), Role: $($loginRes.data.role), ClinicId: $($loginRes.data.clinicId)" -ForegroundColor Green
    $token = $loginRes.token
} catch {
    Write-Host "Login failed: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host "Response Body: $($reader.ReadToEnd())"
    }
    exit 1
}

$headers = @{
    Authorization = "Bearer $token"
    "X-Debug" = "true"
}

$endpoints = @(
    "/api/patients",
    "/api/appointments",
    "/api/doctors",
    "/api/billing",
    "/api/Radiology/records",
    "/api/materials/low-stock",
    "/api/clinics",
    "/api/subscriptions/status"
)

Write-Host ""
Write-Host "Testing dashboard endpoints with live token..."
foreach ($ep in $endpoints) {
    $url = "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net$ep"
    try {
        $res = Invoke-WebRequest -Uri $url -Method Get -Headers $headers -TimeoutSec 15 -UseBasicParsing
        Write-Host "  -> $ep : $($res.StatusCode) OK" -ForegroundColor Green
    } catch {
        $code = $_.Exception.Response.StatusCode
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $raw = $reader.ReadToEnd()
        try {
            $json = $raw | ConvertFrom-Json
            Write-Host "  -> $ep : $code - Message: $($json.message) | Detail: $($json.detail.Substring(0, [Math]::Min(120, $json.detail.Length)))" -ForegroundColor Red
        } catch {
            Write-Host "  -> $ep : $code - Body: $raw" -ForegroundColor Red
        }
    }
}
