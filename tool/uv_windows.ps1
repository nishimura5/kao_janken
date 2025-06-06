# install_uv.ps1

Write-Host "[1/3] Checking execution policy..." -ForegroundColor Cyan
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -notin @("Unrestricted", "RemoteSigned", "Bypass")) {
    Write-Warning "Your current execution policy is '$policy'."
    Write-Host "Changing it to 'RemoteSigned' for this session..."
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
}

Write-Host "[2/3] Installing uv..." -ForegroundColor Cyan
Invoke-Expression (Invoke-RestMethod https://astral.sh/uv/install.ps1)

$cargoBin = "$env:USERPROFILE\.cargo\bin"
$envPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

if ($envPath -notlike "*$cargoBin*") {
    Write-Host "Adding $cargoBin to user PATH..." -ForegroundColor Cyan
    [System.Environment]::SetEnvironmentVariable("Path", "$cargoBin;$envPath", "User")
} else {
    Write-Host "$cargoBin is already in PATH." -ForegroundColor Yellow
}

Write-Host "[3/3] Installation complete. Please restart your terminal." -ForegroundColor Green
