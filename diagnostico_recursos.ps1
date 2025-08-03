# Script de diagnostico de recursos para SOUP Emprendimientos (PowerShell)
# Ejecutar con: powershell -ExecutionPolicy Bypass -File diagnostico_recursos.ps1

function Get-Percent($used, $total) {
    if ($total -eq 0) { return "N/A" }
    return [math]::Round(($used / $total) * 100, 1)
}

# Diccionario de funciones, prioridades y recursos minimos/recomendados
$procAnalysis = @{
    "Cursor" = @{ Func = "Editor/IDE principal (SOUP)"; Priority = "Alta"; MinRAM = 2048; RecRAM = 4096 }
    "node" = @{ Func = "Servidor Node.js / scripts de desarrollo"; Priority = "Media"; MinRAM = 256; RecRAM = 512 }
    "MsMpEng" = @{ Func = "Antivirus de Windows Defender"; Priority = "Media"; MinRAM = 100; RecRAM = 200 }
    "explorer" = @{ Func = "Explorador de archivos de Windows"; Priority = "Media"; MinRAM = 50; RecRAM = 100 }
    "powershell" = @{ Func = "Terminal de comandos"; Priority = "Media"; MinRAM = 50; RecRAM = 100 }
    "Memory Compression" = @{ Func = "Gestion de memoria de Windows"; Priority = "Alta"; MinRAM = 50; RecRAM = 100 }
    "svchost" = @{ Func = "Servicios de Windows"; Priority = "Media"; MinRAM = 50; RecRAM = 200 }
    "chrome" = @{ Func = "Navegador web Chrome"; Priority = "Baja"; MinRAM = 200; RecRAM = 512 }
    "firefox" = @{ Func = "Navegador web Firefox"; Priority = "Baja"; MinRAM = 200; RecRAM = 512 }
    "Teams" = @{ Func = "Microsoft Teams (comunicacion)"; Priority = "Baja"; MinRAM = 200; RecRAM = 512 }
    "OneDrive" = @{ Func = "Sincronizacion de archivos"; Priority = "Baja"; MinRAM = 50; RecRAM = 100 }
}

function Show-Diagnostico {
    Clear-Host
    Write-Host "================= DIAGNOSTICO DE RECURSOS SOUP =================" -ForegroundColor Cyan
    Write-Host "Presiona Enter para refrescar la información, o Ctrl+C para salir."
    Write-Host ""
    # CPU
    $cpu = Get-WmiObject Win32_Processor | Select-Object -First 1
    $cpuCores = $cpu.NumberOfLogicalProcessors
    $cpuName = $cpu.Name
    # RAM
    $ram = Get-WmiObject Win32_ComputerSystem
    $os = Get-WmiObject Win32_OperatingSystem
    $ramTotalMB = [math]::Round($ram.TotalPhysicalMemory/1MB,2)
    $ramFreeMB = [math]::Round($os.FreePhysicalMemory/1024,2) # FreePhysicalMemory esta en KB
    $ramUsedMB = $ramTotalMB - $ramFreeMB
    $ramUsedPct = Get-Percent $ramUsedMB $ramTotalMB
    # Disco
    $disk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"
    $diskTotalMB = [math]::Round($disk.Size/1MB,2)
    $diskFreeMB = [math]::Round($disk.FreeSpace/1MB,2)
    $diskUsedMB = $diskTotalMB - $diskFreeMB
    $diskUsedPct = Get-Percent $diskUsedMB $diskTotalMB
    # Node.js version
    $nodeVersion = try { node -v } catch { "Node no instalado" }
    # Procesos
    $allProcs = Get-Process
    $ramTotalUsedMB = ($allProcs | Measure-Object WS -Sum).Sum / 1MB
    $ramTotalUsedPct = Get-Percent $ramTotalUsedMB $ramTotalMB
    # Procesos background (sin ventana principal)
    $bgProcs = $allProcs | Where-Object { !$_.MainWindowTitle -or $_.MainWindowTitle -eq "" } | Sort-Object -Descending WS | Select-Object -First 10

    Write-Host "===== RESUMEN GENERAL =====" -ForegroundColor Yellow
    Write-Host ("CPU: {0} nucleos - {1}" -f $cpuCores, $cpuName)
    Write-Host ("RAM: {0,8} MB total | {1,8} MB libre | {2,8} MB usada ({3,5}% en uso)" -f $ramTotalMB, $ramFreeMB, $ramUsedMB, $ramUsedPct)
    Write-Host ("Disco C: {0,10} MB total | {1,10} MB libre | {2,10} MB usado ({3,5}% en uso)" -f $diskTotalMB, $diskFreeMB, $diskUsedMB, $diskUsedPct)
    Write-Host ("Version de Node.js: {0}" -f $nodeVersion)

    Write-Host "===== USO GLOBAL DE RECURSOS (Administrador de tareas) =====" -ForegroundColor Yellow
    Write-Host ("RAM usada por todos los procesos: {0,8:N1} MB ({1,5}% del total)" -f $ramTotalUsedMB, $ramTotalUsedPct)
    Write-Host ("Procesos activos: {0}" -f ($allProcs | Measure-Object).Count)

    Write-Host "===== TOP 10 PROCESOS BACKGROUND POR USO DE RAM =====" -ForegroundColor Yellow
    Write-Host ("{0,-20} {1,10} {2,10} {3,10} {4,10} {5,10} {6,10} {7,10} {8,10}" -f 'Nombre','RAM_MB','CPU','Min(MB)','Rec(MB)','Prioridad','Funcion','Sugerencia','ProcId')
    $bgProcs | ForEach-Object {
        $name = $_.ProcessName
        $ram = [math]::Round($_.WS/1MB,2)
        $cpu = $_.CPU
        $procId = $_.Id
        $info = $procAnalysis[$name]
        if ($info) {
            $func = $info.Func
            $prio = $info.Priority
            $min = $info.MinRAM
            $rec = $info.RecRAM
        } else {
            $func = "Desconocido"
            $prio = "Desconocida"
            $min = "-"
            $rec = "-"
        }
        $suggest = if ($prio -eq "Baja" -or $func -eq "Desconocido") { "CERRAR SI NO ES NECESARIO" } else { "" }
        Write-Host ("{0,-20} {1,10} {2,10} {3,10} {4,10} {5,10} {6,10} {7,10} {8,10}" -f $name, $ram, $cpu, $min, $rec, $prio, $func, $suggest, $procId)
    }

    Write-Host "===== RECURSOS MINIMOS RECOMENDADOS =====" -ForegroundColor Green
    Write-Host "- RAM: 4096 MB (minimo), 8192 MB (recomendado)"
    Write-Host "- CPU: 2 nucleos (minimo), 4 nucleos (recomendado)"
    Write-Host "- Espacio en disco: 2048 MB libres (minimo)"
    Write-Host "- Node.js: >= 18.x LTS"
    Write-Host "- Cursor IDE: 2048 MB RAM libres o mas para funcionamiento fluido"

    Write-Host "===== ANALISIS Y RECOMENDACIONES =====" -ForegroundColor Magenta
    if ($ramTotalMB -lt 4096) {
        Write-Host "[!] RAM total INSUFICIENTE para desarrollo moderno. Considera ampliar la memoria." -ForegroundColor Red
    } elseif ($ramFreeMB -lt 1024) {
        Write-Host "[!] RAM libre muy baja. Cierra aplicaciones innecesarias antes de usar Cursor o correr tests." -ForegroundColor Red
    } else {
        Write-Host "[OK] RAM suficiente para desarrollo y pruebas." -ForegroundColor Green
    }
    if ($cpuCores -lt 2) {
        Write-Host "[!] CPU con pocos nucleos. El rendimiento puede ser bajo." -ForegroundColor Red
    } else {
        Write-Host "[OK] CPU adecuada para desarrollo." -ForegroundColor Green
    }
    if ($diskFreeMB -lt 2048) {
        Write-Host "[!] Espacio en disco critico. Libera espacio en C: para evitar problemas." -ForegroundColor Red
    } else {
        Write-Host "[OK] Espacio en disco suficiente." -ForegroundColor Green
    }
    if ($nodeVersion -eq "Node no instalado") {
        Write-Host "[!] Node.js no esta instalado. Instala Node.js >= 18.x LTS." -ForegroundColor Red
    } else {
        Write-Host "[OK] Node.js detectado: $nodeVersion" -ForegroundColor Green
    }

    Write-Host "===== NOTAS ====="
    Write-Host "- Si los recursos disponibles son menores a los recomendados, es probable que Cursor, Node o los tests no funcionen correctamente."
    Write-Host "- Cierra aplicaciones innecesarias para liberar RAM y CPU."
    Write-Host "- Ejecuta este script en PowerShell como usuario normal o administrador."
}

while ($true) {
    Show-Diagnostico
    Write-Host ""
    Write-Host "Presiona Enter para refrescar la información, o Ctrl+C para salir."
    [void][System.Console]::ReadLine()
} 