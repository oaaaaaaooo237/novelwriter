param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$Remote = 'origin'
)

$ErrorActionPreference = 'Stop'
$releaseBranch = "release/v$Version"
$tagName = "v$Version"
$currentBranch = (git branch --show-current).Trim()
$status = git status --porcelain

if ($status) {
    throw 'Working tree is not clean. Commit or stash changes first.'
}

if ($currentBranch -ne 'main') {
    throw "Current branch must be main before publishing, got: $currentBranch"
}

$existingRelease = git branch --list $releaseBranch
if (-not $existingRelease) {
    git branch $releaseBranch
}

$existingTag = git tag --list $tagName
if (-not $existingTag) {
    git tag $tagName
}

git push $Remote main
git push $Remote $releaseBranch
git push $Remote $tagName

Write-Host "Published release branch: $releaseBranch"
Write-Host "Published tag: $tagName"
