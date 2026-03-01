param(
    [ValidateSet("html", "pdf", "both")]
    [string]$Format = "html",
    [string]$SourceRoot = "",
    [string]$OutRoot = "cd_melleklet/notebooks"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = Join-Path $PSScriptRoot ".."
}

$repoRoot = (Resolve-Path $SourceRoot).Path
$targetRoot = Join-Path $repoRoot $OutRoot
New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
Write-Output "Searching notebooks under: $repoRoot"

$notebooks = Get-ChildItem -Path $repoRoot -Recurse -File -Filter *.ipynb |
    Where-Object { $_.FullName -notmatch "\\\.ipynb_checkpoints\\" }

if (-not $notebooks) {
    Write-Output "No notebooks found."
    exit 0
}

foreach ($nb in $notebooks) {
    $relative = $nb.FullName.Substring($repoRoot.Length).TrimStart("\", "/")
    $relativeDir = [System.IO.Path]::GetDirectoryName($relative)
    $outDir = if ([string]::IsNullOrWhiteSpace($relativeDir)) {
        $targetRoot
    } else {
        Join-Path $targetRoot $relativeDir
    }

    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    if ($Format -in @("html", "both")) {
        Write-Output "Export HTML: $relative"
        jupyter nbconvert --to html --output-dir "$outDir" "$($nb.FullName)"
        if ($LASTEXITCODE -ne 0) {
            throw "HTML export failed for $relative"
        }
    }

    if ($Format -in @("pdf", "both")) {
        Write-Output "Export PDF:  $relative"
        jupyter nbconvert --to webpdf --output-dir "$outDir" "$($nb.FullName)"
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "PDF export failed for $relative (webpdf). HTML export remains available."
        }
    }
}

Write-Output "Done. Exports saved under: $targetRoot"
