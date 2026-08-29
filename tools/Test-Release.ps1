[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$Version = "0.2.0",
    [switch]$RequirePackage
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

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

foreach ($skillName in $skillNames) {
    $skillDirectory = Join-Path $RepositoryRoot $skillName
    Assert-Condition (Test-Path -LiteralPath $skillDirectory -PathType Container) "Missing skill directory: $skillName"

    foreach ($fileName in @("SKILL.md", "acceptance.json", "test-prompts.json", "test-results.md")) {
        Assert-Condition (Test-Path -LiteralPath (Join-Path $skillDirectory $fileName) -PathType Leaf) "Missing $skillName/$fileName"
    }

    $skillText = Get-Content -Raw -LiteralPath (Join-Path $skillDirectory "SKILL.md")
    $nameMatch = [regex]::Match($skillText, '(?m)^name:\s*([^\r\n]+)$')
    Assert-Condition $nameMatch.Success "Missing frontmatter name in $skillName/SKILL.md"
    Assert-Condition ($nameMatch.Groups[1].Value.Trim() -eq $skillName) "Frontmatter name mismatch in $skillName/SKILL.md"

    $null = Get-Content -Raw -LiteralPath (Join-Path $skillDirectory "acceptance.json") | ConvertFrom-Json
    $prompts = Get-Content -Raw -LiteralPath (Join-Path $skillDirectory "test-prompts.json") | ConvertFrom-Json
    Assert-Condition ($null -ne $prompts) "Empty test prompts in $skillName"
}

$markdownFiles = Get-ChildItem -LiteralPath $RepositoryRoot -Recurse -File -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.FullName -notmatch '[\\/]dist[\\/]' }

foreach ($markdownFile in $markdownFiles) {
    $text = Get-Content -Raw -LiteralPath $markdownFile.FullName
    foreach ($match in [regex]::Matches($text, '\[[^\]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)')) {
        $relativeTarget = [uri]::UnescapeDataString($match.Groups[1].Value)
        $resolvedTarget = Join-Path $markdownFile.DirectoryName $relativeTarget
        Assert-Condition (Test-Path -LiteralPath $resolvedTarget) "Broken relative link in $($markdownFile.FullName): $relativeTarget"
    }
}

$productSurfaces = @($skillNames | ForEach-Object { Join-Path $RepositoryRoot $_ }) + @(
    (Join-Path $RepositoryRoot "README.md"),
    (Join-Path $RepositoryRoot "DISTRIBUTION.md"),
    (Join-Path $RepositoryRoot "DELIVERY_MANIFEST.md"),
    (Join-Path $RepositoryRoot "INDEX.md")
)
$forbidden = & rg -n -i 'beads|beads studio' @productSurfaces 2>$null
Assert-Condition ($LASTEXITCODE -eq 1) "Unrelated product reference found:`n$($forbidden -join [Environment]::NewLine)"

if ($RequirePackage) {
    $zipName = "codex-delivery-assurance-$Version.zip"
    $zipPath = Join-Path $RepositoryRoot "dist/$zipName"
    $zipChecksumPath = "$zipPath.sha256"
    Assert-Condition (Test-Path -LiteralPath $zipPath -PathType Leaf) "Missing package: $zipPath"
    Assert-Condition (Test-Path -LiteralPath $zipChecksumPath -PathType Leaf) "Missing package checksum: $zipChecksumPath"

    $expectedHash = ((Get-Content -Raw -LiteralPath $zipChecksumPath) -split '\s+')[0].ToLowerInvariant()
    $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
    Assert-Condition ($expectedHash -eq $actualHash) "ZIP checksum mismatch"

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
    try {
        $entries = @($archive.Entries | ForEach-Object { $_.FullName.Replace('\\', '/') })
        foreach ($skillName in $skillNames) {
            Assert-Condition (($entries | Where-Object { $_ -like "$skillName/*" }).Count -gt 0) "ZIP is missing $skillName"
        }
        Assert-Condition (($entries | Where-Object { $_ -like 'codex-pmo-orchestration/*' }).Count -eq 0) "ZIP must not contain codex-pmo-orchestration"
        Assert-Condition ($entries.Contains("CHECKSUMS.sha256")) "ZIP is missing CHECKSUMS.sha256"
    }
    finally {
        $archive.Dispose()
    }
}

Write-Output "PASS: 9 skills, JSON, frontmatter names, relative links, forbidden references, and package checks"
$global:LASTEXITCODE = 0
