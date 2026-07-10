# WSL Migration To D

## Goal

Move the current `Ubuntu` WSL distro from `C:` to `D:` safely, because `C:` is too full.

Target location:

- distro archive: `D:\WSL\Ubuntu-export-clean.tar`
- imported distro directory: `D:\WSL\Ubuntu-D`
- new distro name: `Ubuntu-D`

## Important

This migration must be done from **Windows PowerShell**, not from the current WSL terminal.

At some point you must close this CLI because `wsl --shutdown` will stop the running distro.

## What will change

- WSL storage moves to `D:`
- your Linux environment should work almost the same
- `C:` will be freed only after the old distro is removed

## What will NOT change much

- you still use `wsl`
- Ubuntu still works the same way
- your Linux tools and files should still be there after import

## Before starting

## 1. Save your current work

In the current WSL terminal, if you have uncommitted work:

```bash
git status
```

If needed, commit or copy anything important.

## 2. Close Docker Desktop if possible

Recommended but optional.

This reduces file activity during export/import.

## 3. Close WSL terminals

Close:

- this CLI
- any Ubuntu terminal
- any VS Code remote WSL window

## PowerShell commands to run

Open **Windows PowerShell** as your normal user first.

If a command fails because of permissions, reopen PowerShell as Administrator.

## Step 1. Check current WSL distros

```powershell
wsl --list --verbose
```

You should see at least:

- `Ubuntu`

## Step 2. Create target folder on D

```powershell
New-Item -ItemType Directory -Force -Path D:\WSL
```

## Step 3. Remove or rename the previous broken export file if it exists

This is important because a previous export attempt already left a large tar file.

```powershell
if (Test-Path D:\WSL\Ubuntu.tar) {
    Rename-Item D:\WSL\Ubuntu.tar Ubuntu_old_incomplete.tar -Force
}
```

## Step 4. Stop WSL completely

```powershell
wsl --shutdown
```

Wait 10 to 15 seconds.

## Step 5. Export Ubuntu cleanly

```powershell
wsl --export Ubuntu D:\WSL\Ubuntu-export-clean.tar
```

Expected duration:

- 10 to 40 minutes or more depending on disk speed

## Step 6. Verify the export file exists

```powershell
Get-Item D:\WSL\Ubuntu-export-clean.tar
```

Optional size check:

```powershell
Get-ChildItem D:\WSL\Ubuntu-export-clean.tar | Select-Object Name,Length,LastWriteTime
```

## Step 7. Import the distro on D under a new name

```powershell
wsl --import Ubuntu-D D:\WSL\Ubuntu-D D:\WSL\Ubuntu-export-clean.tar --version 2
```

Expected duration:

- 10 to 30 minutes or more

## Step 8. Verify the new distro exists

```powershell
wsl --list --verbose
```

You should now see both:

- `Ubuntu`
- `Ubuntu-D`

## Step 9. Start the new distro once

```powershell
wsl -d Ubuntu-D
```

Inside it, run:

```bash
whoami
pwd
ls
```

If your home and files look correct, exit:

```bash
exit
```

## Step 10. Set the new distro as default

```powershell
wsl --set-default Ubuntu-D
```

## Step 11. Test that default WSL opens the new distro

```powershell
wsl
```

Inside WSL, verify:

```bash
whoami
pwd
```

Then exit:

```bash
exit
```

## Step 12. Only after validation, remove the old distro from C

Warning:

- this is the destructive step
- do it only after confirming `Ubuntu-D` works

```powershell
wsl --unregister Ubuntu
```

This is the step that actually frees the large WSL storage from `C:`.

## Step 13. Optional cleanup

After everything works, you can remove the export tar to reclaim `D:` space:

```powershell
Remove-Item D:\WSL\Ubuntu-export-clean.tar
```

You can also remove the incomplete old export if still present:

```powershell
Remove-Item D:\WSL\Ubuntu_old_incomplete.tar -Force
```

## Step 14. Reopen your tools

Now you can reopen:

- Windows Terminal
- VS Code
- Docker Desktop
- this project CLI

## After migration

When you reopen WSL, verify:

```bash
wsl.exe --list --verbose
pwd
df -h
```

If you come back to this project, also verify:

```bash
cd /mnt/d/ws/MLOps
source .venv/bin/activate
pytest
```

## What to do if the import fails

If `wsl --import` fails:

1. do not unregister `Ubuntu`
2. keep the old distro intact
3. note the exact error
4. retry only after checking disk space on `D:`

## What to do if the new distro opens but user/home is wrong

Imported distros sometimes start as `root` by default.

If that happens, do not panic.

First inspect:

```bash
cat /etc/passwd | grep /home
ls /home
```

Then we can set the default user afterwards.

## Safe summary

The safe sequence is:

1. close this CLI
2. `wsl --shutdown`
3. `wsl --export Ubuntu D:\WSL\Ubuntu-export-clean.tar`
4. `wsl --import Ubuntu-D D:\WSL\Ubuntu-D D:\WSL\Ubuntu-export-clean.tar --version 2`
5. test `Ubuntu-D`
6. `wsl --set-default Ubuntu-D`
7. only then `wsl --unregister Ubuntu`
