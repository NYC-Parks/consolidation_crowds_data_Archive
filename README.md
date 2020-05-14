# This is an IPM template_repo !
This repo can be cloned to jump start a new IPM repository. 

## To clone this repo and name it something meaningful (locally) for your new project:
```
git clone git@github.com:NYC-Parks/template_repo.git --recursive my_new_project
```
### If you forgot the `--recursive` tag, the IPM_Shared_Code submodule may not have been cloned correctly. You can fix this by doing:
```
git submodule update --init
```
### If that still didn't work, you may need to update git:

```
git update-git-for-windows
```
### To update the submodule to its most current state, go to the parent directory (eg, `cd Projects/my_new_project`) and do:
```
git submodule update --remote IPM_Shared_Code
```
