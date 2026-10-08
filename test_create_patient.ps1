$loginUrl = "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/auth/login"
$loginBody = @{
    email = "msami11095@gmail.com"
    password = "Sami@11095"
} | ConvertTo-Json

$login = Invoke-RestMethod -Uri $loginUrl -Method Post -ContentType "application/json" -Body $loginBody
$headers = @{
    Authorization = "Bearer " + $login.token
    "Content-Type" = "application/json"
}

# 1. Fetch available clinics
$clinics = Invoke-RestMethod -Uri "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/clinics" -Headers $headers
Write-Host "Clinics count: $($clinics.data.Count)"
$clinicId = if ($clinics.data.Count -gt 0) { $clinics.data[0].id } else { "" }
Write-Host "Using Clinic ID: $clinicId"

# 2. Test patient creation
$randomPhone = "10" + (Get-Random -Minimum 10000000 -Maximum 99999999).ToString()
$patientBody = @{
    id = [Guid]::NewGuid().ToString()
    firstName = "Test"
    lastName = "Patient"
    gender = "Male"
    dateOfBirth = "1995-05-15"
    countryCode = "+20"
    phoneNumber = $randomPhone
    contactNumber = "+20$randomPhone"
    email = "test-$randomPhone@example.com"
    address = "123 Main Street Alexandria"
    clinicId = $clinicId
} | ConvertTo-Json

try {
    $res = Invoke-RestMethod -Uri "https://clinic-api-123-a0ghf9aeb5ccawha.swedencentral-01.azurewebsites.net/api/patients" -Method Post -Headers $headers -Body $patientBody
    Write-Host "Patient created: $($res.message)" -ForegroundColor Green
} catch {
    $code = $_.Exception.Response.StatusCode
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $body = $reader.ReadToEnd()
    Write-Host "Patient create failed ($code): $body" -ForegroundColor Red
}
