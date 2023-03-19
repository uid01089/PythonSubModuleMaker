
import os
from pathlib import Path, PurePath
import shutil
from typing import Tuple
import PythonLib.Git

startpath = PurePath("h:\\var\\01_computer\\3d_printing\\src\\Marlin.git\\Marlin")
gitHubDir = PurePath("h:\\var\\01_computer\\3d_printing\\src\\Marlin.git\\Marlin")
gitWorkDir = PurePath("h:\\var\\01_computer\\3d_printing\\src\\Marlin.git\\Marlin")
path2repo = {}


def initAndClone(path: Path) -> Tuple[Path, Path]:
    # Create Bare repo
    repDir = Path(gitHubDir, path.name)
    repDir.mkdir(parents=True)
    PythonLib.Git.Git(repDir).initBare()

    # Clone bare repo
    workdir = Path(gitWorkDir, path.name)
    workdir.mkdir(parents=True)
    PythonLib.Git.Git(workdir).clone(repDir)

    return (repDir, workdir)


def createDirGitRepo(path: Path, files: list[Path], dirs: list[Path]) -> Path:

    (repDir, workdir) = initAndClone(path)

    # Add submodules
    for file in files:
        repo = path2repo.get(file)
        PythonLib.Git.Git(workdir).addSubModule(repo).addAll().commit("First commit").push()

    for directory in dirs:
        repo = path2repo.get(directory)
        PythonLib.Git.Git(workdir).addSubModule(repo).addAll().commit("First commit").push()

    return repDir


def createFileGitRepo(path: Path) -> PurePath:

    (repDir, workdir) = initAndClone(path)

    # Copy File into workDir and push
    shutil.copy(path, workdir)
    PythonLib.Git.Git(workdir).addAll().commit("First commit").push()

    return repDir


def treeWalker(startPath: PurePath) -> None:

    files = []
    directories = []

    for dirElement in os.listdir(startPath):
        path = Path(startPath, dirElement)
        if path.is_file():
            files.append(path)
        else:
            directories.append(path)

   # dive into tree
    for directory in directories:
        treeWalker(directory)

    # Create GitRepo for each file
    for file in files:
        repoLocation = createFileGitRepo(file)
        path2repo[file] = repoLocation

    # Directories and files done, create own directory as Git repo
    repoLocation = createDirGitRepo(startPath, files, directories)
    path2repo[startPath] = repoLocation


if __name__ == '__main__':
    treeWalker(startpath)
