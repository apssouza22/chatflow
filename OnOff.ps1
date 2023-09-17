# PowerShell Script to Automate Chatflow On and Off
# .\OnOff.ps1 -action on -apiKey [OpenAI API Key]
# .\OnOff.ps1 -action off
param (
    [string]$action,
    [string]$apiKey
)

# Function to display usage
function Show-Usage {
    Write-Host "Usage: .\OnOff.ps1 -action [on|off] -apiKey [Your OpenAI API Key]"
}

# Check for correct number of arguments
if ($action -eq $null) {
    Show-Usage
    exit 1
}

# Function to update .env file
function Update-EnvFile {
    $envPath = ".\.env"
    (Get-Content $envPath) -replace "OPENAI_API_KEY_GPT3=.*", ("OPENAI_API_KEY_GPT3=" + $apiKey) | Set-Content $envPath
    (Get-Content $envPath) -replace "OPENAI_API_KEY_GPT4=.*", ("OPENAI_API_KEY_GPT4=" + $apiKey) | Set-Content $envPath
}

# On function
function Turn-On {
    Write-Host "Turning on Chatflow..."
    
    # React UI Setup
    Write-Host "Setting up React UI..."
    Set-Location .\chat-ui
    npm install
    npm run build
    Start-Process "cmd" "/c npm start"
    Set-Location ..  # Navigate back to the root directory
    
    # Backend Setup
    Write-Host "Setting up Backend..."
    pip cache purge #fixes bug with requirement install
    pip install -r requirements-dev.txt
    Set-Location .\server\src
    docker-compose up -d redis postgres
    Copy-Item .env.template -Destination .env
    Update-EnvFile
    python load_data.py
    Start-Process "cmd" "/c python server.py"
    Set-Location ..\..  # Navigate back to the root directory
    
    Write-Host "Chatflow turned on."
}

# Off function
function Turn-Off {
    Write-Host "Turning off Chatflow..."
    
    # Stop Docker services
    Set-Location .\server\src
    docker-compose down
    Set-Location ..\..  # Navigate back to the root directory
    
    # Stop React UI and Python server
    Stop-Process -Name "node" -Force
    Stop-Process -Name "python" -Force
    
    Write-Host "Chatflow turned off."
}

# Main function to decide whether to turn on or off
if ($action -eq "on") {
    Turn-On
} elseif ($action -eq "off") {
    Turn-Off
} else {
    Show-Usage
    exit 1
}