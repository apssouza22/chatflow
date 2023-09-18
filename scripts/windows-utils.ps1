# PowerShell Script to Automate Chatflow Setup, On, and Off

# .\windows-utils.ps1 -action setup -apiKey [OpenAI API Key]
# .\windows-utils.ps1 -action on
# .\windows-utils.ps1 -action off

param (
    [string]$action,
    [string]$apiKey
)

# Function to display usage
function Show-Usage {
    Write-Host "Usage: .\windows-utils.ps1 -action [setup|on|off] -apiKey [Your OpenAI API Key (only for setup)]"
}

# Check for correct number of arguments
if ($action -eq $null) {
    Show-Usage
    exit 1
}

# Function to update .env file
function Update-EnvFile {
    $envPath = ".env"
    (Get-Content $envPath) -replace "OPENAI_API_KEY_GPT3=.*", ("OPENAI_API_KEY_GPT3=" + $apiKey) | Set-Content $envPath
    (Get-Content $envPath) -replace "OPENAI_API_KEY_GPT4=.*", ("OPENAI_API_KEY_GPT4=" + $apiKey) | Set-Content $envPath
}

# Setup function
function Setup {
    Write-Host "Setting up Chatflow..."
    
    # React UI Setup
    Write-Host "Setting up React UI..."
    Set-Location ..\chat-ui
    npm install
    npm run build
    
    # Backend Setup
    Write-Host "Setting up Backend..."
    Set-Location ..
    pip cache purge #fixes bug with requirement install
    pip install -r requirements-dev.txt
    Set-Location server\src
    docker-compose up -d redis postgres
    Copy-Item .env.template -Destination .env
    Update-EnvFile
    python load_data.py
    Set-Location ..\..\scripts  # Navigate back to scripts
    
    Write-Host "Chatflow set up."
}

# On function
function Turn-On {
    Write-Host "Turning on Chatflow..."
    
    # React UI
    Set-Location ..\chat-ui
    Start-Process "cmd" "/c npm start"
    
    #Backend
    Set-Location ..\server\src
    docker-compose up -d redis postgres
    Start-Process "cmd" "/c python server.py"
    Set-Location ..\..\scripts  # Navigate back to scripts
    
    Write-Host "Chatflow turned on."
}

# Off function
function Turn-Off {
    Write-Host "Turning off Chatflow..."
    
    # Stop Docker services
    Set-Location ..\server\src
    docker-compose down
    Set-Location ..\..\scripts  # Navigate back to scripts
    
    # Stop React UI and Python server
    Stop-Process -Name "node" -Force
    Stop-Process -Name "python" -Force
    
    Write-Host "Chatflow turned off."
}

# Main function to decide whether to setup, turn on, or turn off
if ($action -eq "setup") {
    if ($apiKey -eq $null) {
        Write-Host "API key is required for setup."
        Show-Usage
        exit 1
    }
    Setup
} elseif ($action -eq "on") {
    Turn-On
} elseif ($action -eq "off") {
    Turn-Off
} else {
    Show-Usage
    exit 1
}
