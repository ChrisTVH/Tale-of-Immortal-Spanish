#!/usr/bin/env python3
"""
Build the mod release.

Cleans and compiles the ModMain project in Release configuration, then
verifies that the generated MOD_pzAi9g.dll assembly exists. Additional
arguments are forwarded to ``dotnet build``.
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
PROJECT_FILE = REPO_ROOT / "ModProject" / "ModCode" / "ModMain" / "ModMain.csproj"
OUTPUT_FILE = (
    REPO_ROOT
    / "ModProject"
    / "ModCode"
    / "ModMain"
    / "bin"
    / "Release"
    / "MOD_pzAi9g.dll"
)


def run_dotnet(arguments):
    try:
        return subprocess.run(["dotnet", *arguments], cwd=REPO_ROOT, check=False)
    except FileNotFoundError:
        print("dotnet CLI not found", flush=True)
        sys.exit(1)


def build_mod(dotnet_args):
    print("=== Building mod release... ===", flush=True)

    clean_result = run_dotnet(
        [
            "clean",
            str(PROJECT_FILE),
            "--configuration",
            "Release",
            "--verbosity",
            "quiet",
        ]
    )
    if clean_result.returncode != 0:
        print("Mod clean failed", flush=True)
        sys.exit(1)

    build_result = run_dotnet(
        [
            "build",
            str(PROJECT_FILE),
            "--configuration",
            "Release",
            "--no-incremental",
            *dotnet_args,
        ]
    )
    if build_result.returncode != 0:
        print("Mod build failed", flush=True)
        sys.exit(1)

    if not OUTPUT_FILE.exists():
        print(f"Mod assembly not found at {OUTPUT_FILE}", flush=True)
        sys.exit(1)

    print(f"Built {OUTPUT_FILE}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Build the mod release")
    parser.add_argument(
        "dotnet_args",
        nargs="*",
        help="Additional arguments passed to dotnet build",
    )
    args, unknown_args = parser.parse_known_args()
    build_mod([*args.dotnet_args, *unknown_args])
    print("=== Build complete ===", flush=True)


if __name__ == "__main__":
    main()
