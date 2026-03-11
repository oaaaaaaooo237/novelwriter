param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Remote = 'origin',
    [switch]$Push
)

$ErrorActionPreference = 'Stop'
$devBranch = "codex/v$Version"
$currentBranch = (git branch --show-current).Trim()
$status = git status --porcelain

if ($status) {
    throw 'Working tree is not clean. Commit or stash changes first.'
}

if ($currentBranch -ne 'main') {
    throw "Current branch must be main, got: $currentBranch"
}

git checkout -b $devBranch

if ($Push) {
    git push -u $Remote $devBranch
}

Write-Host "Started version branch: $devBranch"
