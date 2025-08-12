# Auto-Install Python Dependencies Script
# This script runs python main.py and automatically installs missing modules

$MaxAttempts = 10
$PythonCommand = "python"
$PipCommand = "pip"

Write-Host "Starting Python Auto-Installer Script" -ForegroundColor Green
Write-Host "Max attempts: $MaxAttempts" -ForegroundColor Yellow

$attempt = 1
$installedModules = @()

while ($attempt -le $MaxAttempts) {
    Write-Host "`n--- Attempt $attempt ---" -ForegroundColor Cyan

    try {
        # Execute python main.py and capture both stdout and stderr
        $process = Start-Process -FilePath 'flask' -ArgumentList "run" -NoNewWindow -Wait -PassThru -RedirectStandardError "error.txt" -RedirectStandardOutput "output.txt"

        if ($process.ExitCode -eq 0) {
            Write-Host "SUCCESS: python main.py executed successfully!" -ForegroundColor Green

            # Display output if any
            $output = Get-Content "output.txt" -ErrorAction SilentlyContinue
            if ($output) {
                Write-Host "`nOutput:" -ForegroundColor Yellow
                $output | ForEach-Object { Write-Host $_ }
            }

            break
        } else {
            # Read error output
            $errorOutput = Get-Content "error.txt" -ErrorAction SilentlyContinue -Raw
            Write-Host "Python script failed with exit code: $($process.ExitCode)" -ForegroundColor Red
            Write-Host "Error output:" -ForegroundColor Red
            Write-Host $errorOutput -ForegroundColor Red

            # Parse error for missing modules
            $missingModule = $null

            # Common patterns for missing module errors
            $patterns = @(
                "ModuleNotFoundError: No module named '([^']+)'",
                "ImportError: No module named ([^\s]+)",
                "ImportError: No module named '([^']+)'",
                "ModuleNotFoundError: No module named ([^\s]+)",
                "ImportError: cannot import name '[^']+' from '([^']+)'",
                "from ([^\s]+) import.*ImportError",
                "import ([^\s]+).*ModuleNotFoundError"
            )

            foreach ($pattern in $patterns) {
                if ($errorOutput -match $pattern) {
                    $missingModule = $matches[1]
                    break
                }
            }

            if ($missingModule) {
                # Clean up module name (remove any extra characters)
                $missingModule = $missingModule.Trim().Split('.')[0]

                # Skip if already tried to install this module
                if ($installedModules -contains $missingModule) {
                    Write-Host "Already attempted to install '$missingModule'. Possible version conflict or other issue." -ForegroundColor Yellow
                    break
                }

                Write-Host "`nDetected missing module: '$missingModule'" -ForegroundColor Yellow
                Write-Host "Installing with: $PipCommand install $missingModule" -ForegroundColor Yellow

                # Install the missing module
                $pipProcess = Start-Process -FilePath $PipCommand -ArgumentList "install", $missingModule -NoNewWindow -Wait -PassThru -RedirectStandardError "pip_error.txt" -RedirectStandardOutput "pip_output.txt"

                if ($pipProcess.ExitCode -eq 0) {
                    Write-Host "Successfully installed '$missingModule'" -ForegroundColor Green
                    $installedModules += $missingModule

                    # Show pip output
                    $pipOutput = Get-Content "pip_output.txt" -ErrorAction SilentlyContinue
                    if ($pipOutput) {
                        Write-Host "Pip output:" -ForegroundColor Gray
                        $pipOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
                    }
                } else {
                    $pipError = Get-Content "pip_error.txt" -ErrorAction SilentlyContinue -Raw
                    Write-Host "Failed to install '$missingModule'" -ForegroundColor Red
                    Write-Host "Pip error: $pipError" -ForegroundColor Red

                    # Try alternative installation methods
                    Write-Host "Trying alternative installation methods..." -ForegroundColor Yellow

                    # Try with --user flag
                    $pipProcess2 = Start-Process -FilePath $PipCommand -ArgumentList "install", "--user", $missingModule -NoNewWindow -Wait -PassThru
                    if ($pipProcess2.ExitCode -eq 0) {
                        Write-Host "Successfully installed '$missingModule' with --user flag" -ForegroundColor Green
                        $installedModules += $missingModule
                    } else {
                        # Try common package name variations
                        $alternativeNames = @{
                            "PIL" = "Pillow"
                            "cv2" = "opencv-python"
                            "sklearn" = "scikit-learn"
                            "yaml" = "PyYAML"
                            "flask_login" = "Flask-Login"
                            "flask_sqlalchemy" = "Flask-SQLAlchemy"
                            "flask_cors" = "Flask-CORS"
                            "bs4" = "beautifulsoup4"
                        }

                        if ($alternativeNames.ContainsKey($missingModule)) {
                            $altName = $alternativeNames[$missingModule]
                            Write-Host "Trying alternative package name: '$altName'" -ForegroundColor Yellow

                            $pipProcess3 = Start-Process -FilePath $PipCommand -ArgumentList "install", $altName -NoNewWindow -Wait -PassThru
                            if ($pipProcess3.ExitCode -eq 0) {
                                Write-Host "Successfully installed '$altName' (alternative for '$missingModule')" -ForegroundColor Green
                                $installedModules += $missingModule
                            } else {
                                Write-Host "All installation attempts failed for '$missingModule'" -ForegroundColor Red
                                break
                            }
                        } else {
                            Write-Host "No known alternative package name for '$missingModule'" -ForegroundColor Red
                            break
                        }
                    }
                }
            } else {
                Write-Host "`nError does not appear to be a missing module issue." -ForegroundColor Yellow
                Write-Host "Manual intervention may be required." -ForegroundColor Yellow
                break
            }
        }
    }
    catch {
        Write-Host "Unexpected error: $_" -ForegroundColor Red
        break
    }
    finally {
        # Clean up temporary files
        Remove-Item "error.txt", "output.txt", "pip_error.txt", "pip_output.txt" -ErrorAction SilentlyContinue
    }

    $attempt++
}

if ($attempt -gt $MaxAttempts) {
    Write-Host "`nReached maximum attempts ($MaxAttempts). Stopping." -ForegroundColor Red
}