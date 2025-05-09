param (
    [string]$CommitMessage
)

# Obtener la fecha y hora actual en formato español
$fechaHora = Get-Date -Format "dd/MM/yyyy HH:mm:ss"

# Si no se proporciona un mensaje de commit, usar uno estándar con la fecha y hora
if ([string]::IsNullOrEmpty($CommitMessage)) {
    $CommitMessage = "Actualización automática del $fechaHora"
}

# Ejecutar los comandos de Git
Write-Host "Añadiendo todos los cambios al área de preparación..." -ForegroundColor Cyan
git add .

Write-Host "Realizando commit con el mensaje: '$CommitMessage'..." -ForegroundColor Green
git commit -m "$CommitMessage" --no-verify

Write-Host "Subiendo cambios a la rama main..." -ForegroundColor Yellow
git push origin main --no-verify

Write-Host "¡Proceso completado con éxito!" -ForegroundColor Magenta
