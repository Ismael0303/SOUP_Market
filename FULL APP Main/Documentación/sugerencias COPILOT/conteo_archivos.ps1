$exts = @("py","js","ts","json","md","txt","sql","yml","yaml","sh","bat","ps1","html","css","jpg","png","svg")
$descs = @{
    "py"="(Código backend, scripts, modelos, routers)"
    "js"="(Frontend JS, lógica de UI)"
    "ts"="(Frontend TypeScript, lógica de UI)"
    "json"="(Configuraciones, datos, package.json)"
    "md"="(Documentación Markdown)"
    "txt"="(Textos, scripts, logs)"
    "sql"="(Migraciones, queries SQL)"
    "yml"="(Config YAML, CI/CD)"
    "yaml"="(Config YAML, CI/CD)"
    "sh"="(Scripts Bash)"
    "bat"="(Scripts Windows)"
    "ps1"="(Scripts PowerShell)"
    "html"="(Plantillas HTML)"
    "css"="(Estilos CSS)"
    "jpg"="(Imágenes JPG)"
    "png"="(Imágenes PNG)"
    "svg"="(Vectores SVG)"
}
# Carpetas a ignorar (node_modules, venv, .venv, dist, build, .git, .pytest_cache, coverage, htmlcov, __pycache__, site-packages, pip-* y más)
$ignoreDirs = @('node_modules', 'venv', '.venv', 'dist', 'build', '.git', '.pytest_cache', 'coverage', 'htmlcov', '__pycache__', 'site-packages', 'pip-*', 'lib', 'Scripts', 'bin', 'share', 'include', 'Lib', 'EGG-INFO', 'symlinked', 'symlink_target', 'shadowed_core')

function ShouldIgnore($path) {
    foreach ($dir in $ignoreDirs) {
        if ($path -match "\\$dir(\\|$)") { return $true }
        if ($path -match "\\$dir\\") { return $true }
    }
    return $false
}

foreach ($ext in $exts) {
    $count = 0
    Get-ChildItem -Recurse -Filter "*.$ext" -File | Where-Object { -not (ShouldIgnore $_.FullName) } | ForEach-Object { $count++ }
    if ($count -gt 0) {
        Write-Host ("{0}: {1} {2}" -f $ext, $count, $descs[$ext])
    }
}
