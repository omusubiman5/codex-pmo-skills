[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$Version = "0.2.0"
)

$ErrorActionPreference = "Stop"

$skillNames = @(
    "codex-execution-mode-routing",
    "codex-exec-io-contract",
    "codex-ci-patch-handoff",
    "codex-sandbox-approval-boundary",
    "codex-egress-surface-governance",
    "codex-bounded-subagents",
    "codex-context-entry-routing",
    "codex-auth-boundary-selection",
    "codex-mcp-control-plane"
)

$documentNames = @(
    "README.md",
    "DISTRIBUTION.md",
    "INDEX.md",
    "GLOSSARY.md",
    "SOURCE_MANIFEST.md",
    "LICENSE"
)

& (Join-Path $PSScriptRoot "Test-Release.ps1") -RepositoryRoot $RepositoryRoot -Version $Version

$stageRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("codex-delivery-assurance-" + [guid]::NewGuid().ToString("N"))
$distRoot = Join-Path $RepositoryRoot "dist"
$zipName = "codex-delivery-assurance-$Version.zip"
$zipPath = Join-Path $distRoot $zipName
$zipChecksumPath = "$zipPath.sha256"

try {
    New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $distRoot -Force | Out-Null

    foreach ($skillName in $skillNames) {
        Copy-Item -LiteralPath (Join-Path $RepositoryRoot $skillName) -Destination $stageRoot -Recurse
    }
    foreach ($documentName in $documentNames) {
        Copy-Item -LiteralPath (Join-Path $RepositoryRoot $documentName) -Destination $stageRoot
    }

    $payloadFiles = Get-ChildItem -LiteralPath $stageRoot -Recurse -File | Sort-Object FullName
    $checksumLines = foreach ($payloadFile in $payloadFiles) {
        $relativePath = [System.IO.Path]::GetRelativePath($stageRoot, $payloadFile.FullName).Replace('\\', '/')
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $payloadFile.FullName).Hash.ToLowerInvariant()
        "$hash  $relativePath"
    }
    $checksumText = ($checksumLines -join "`n") + "`n"
    Set-Content -LiteralPath (Join-Path $stageRoot "CHECKSUMS.sha256") -Value $checksumText -Encoding utf8NoBOM -NoNewline
    Set-Content -LiteralPath (Join-Path $RepositoryRoot "CHECKSUMS.sha256") -Value $checksumText -Encoding utf8NoBOM -NoNewline

    if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    Compress-Archive -Path (Join-Path $stageRoot '*') -DestinationPath $zipPath -CompressionLevel Optimal

    $zipHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
    Set-Content -LiteralPath $zipChecksumPath -Value "$zipHash  $zipName`n" -Encoding utf8NoBOM -NoNewline
}
finally {
    if (Test-Path -LiteralPath $stageRoot) { Remove-Item -LiteralPath $stageRoot -Recurse -Force }
}

& (Join-Path $PSScriptRoot "Test-Release.ps1") -RepositoryRoot $RepositoryRoot -Version $Version -RequirePackage

Write-Output "Built $zipPath"
