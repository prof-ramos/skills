#!/usr/bin/env python3
"""
Duck CLI Batch Upload Script
Wrapper for batch file operations with progress tracking and error handling

Usage:
    python batch_upload.py --remote sftp://user@host/path/ --files file1.txt file2.txt
    python batch_upload.py --remote s3://bucket/path/ --directory /local/dir
    python batch_upload.py --config batch_config.json
"""

import subprocess
import sys
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
import concurrent.futures
from typing import List, Dict, Tuple


class DuckBatchUploader:
    """Batch uploader using duck CLI with progress tracking and error handling"""
    
    def __init__(self, remote_url: str, duck_path: str = "duck"):
        self.remote_url = remote_url
        self.duck_path = duck_path
        self.results = []
        self.verify_duck()
    
    def verify_duck(self):
        """Verify duck CLI is installed"""
        try:
            subprocess.run([self.duck_path, "--version"], 
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: duck CLI not found. Install from https://duck.sh/")
            sys.exit(1)
    
    def upload_file(self, local_file: Path, 
                   options: Dict = None) -> Tuple[bool, str]:
        """
        Upload a single file
        
        Args:
            local_file: Path to local file
            options: Dict of additional duck options
            
        Returns:
            Tuple of (success, message)
        """
        if not local_file.exists():
            return False, f"File not found: {local_file}"
        
        # Build command
        cmd = [
            self.duck_path,
            "--upload",
            self.remote_url,
            str(local_file)
        ]
        
        # Add options
        if options:
            if options.get("verbose"):
                cmd.append("--verbose")
            if options.get("preserve"):
                cmd.append("--preserve")
            if options.get("retry"):
                cmd.extend(["--retry", str(options["retry"])])
            if options.get("permissions"):
                cmd.extend(["--permissions", options["permissions"]])
            if options.get("storage_class"):
                cmd.extend(["--storage-class", options["storage_class"]])
            if options.get("throttle"):
                cmd.extend(["--throttle", str(options["throttle"])])
        
        # Execute upload
        start_time = datetime.now()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=options.get("timeout", 300)
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if result.returncode == 0:
                file_size = local_file.stat().st_size
                speed = file_size / duration if duration > 0 else 0
                return True, f"Success ({duration:.1f}s, {speed/1024/1024:.2f} MB/s)"
            else:
                return False, f"Failed: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout exceeded"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def upload_directory(self, local_dir: Path, 
                        options: Dict = None,
                        pattern: str = "*",
                        recursive: bool = True) -> None:
        """
        Upload all files in a directory
        
        Args:
            local_dir: Path to local directory
            options: Dict of duck options
            pattern: File pattern to match
            recursive: Include subdirectories
        """
        if not local_dir.is_dir():
            print(f"ERROR: Not a directory: {local_dir}")
            return
        
        # Find files
        if recursive:
            files = list(local_dir.rglob(pattern))
        else:
            files = list(local_dir.glob(pattern))
        
        # Filter to files only
        files = [f for f in files if f.is_file()]
        
        print(f"Found {len(files)} files to upload")
        
        # Upload files
        self.upload_batch(files, options)
    
    def upload_batch(self, files: List[Path], 
                    options: Dict = None,
                    max_workers: int = 5) -> None:
        """
        Upload multiple files with parallel execution
        
        Args:
            files: List of file paths
            options: Dict of duck options
            max_workers: Number of parallel uploads
        """
        total = len(files)
        completed = 0
        failed = 0
        
        print(f"Starting batch upload of {total} files...")
        print(f"Remote destination: {self.remote_url}")
        print(f"Parallel workers: {max_workers}")
        print("-" * 60)
        
        # Parallel upload
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self.upload_file, f, options): f 
                for f in files
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                completed += 1
                
                try:
                    success, message = future.result()
                    status = "✓" if success else "✗"
                    
                    if not success:
                        failed += 1
                    
                    # Store result
                    self.results.append({
                        "file": str(file_path),
                        "success": success,
                        "message": message
                    })
                    
                    # Progress output
                    progress = (completed / total) * 100
                    print(f"[{progress:5.1f}%] {status} {file_path.name}: {message}")
                    
                except Exception as e:
                    failed += 1
                    error_msg = f"Exception: {str(e)}"
                    self.results.append({
                        "file": str(file_path),
                        "success": False,
                        "message": error_msg
                    })
                    print(f"[{(completed/total)*100:5.1f}%] ✗ {file_path.name}: {error_msg}")
        
        # Summary
        print("-" * 60)
        print(f"Completed: {completed}/{total}")
        print(f"Successful: {completed - failed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed uploads:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['file']}: {result['message']}")
    
    def save_results(self, output_file: str):
        """Save upload results to JSON file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "remote_url": self.remote_url,
            "total_files": len(self.results),
            "successful": sum(1 for r in self.results if r["success"]),
            "failed": sum(1 for r in self.results if not r["success"]),
            "results": self.results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")


def load_config(config_file: str) -> Dict:
    """Load configuration from JSON file"""
    with open(config_file) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Batch upload files using duck CLI"
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--files", nargs="+", help="List of files to upload")
    input_group.add_argument("--directory", help="Directory to upload")
    input_group.add_argument("--config", help="JSON config file")
    
    # Remote destination
    parser.add_argument("--remote", help="Remote URL (protocol://host/path)")
    
    # Upload options
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--preserve", action="store_true", help="Preserve timestamps")
    parser.add_argument("--retry", type=int, default=3, help="Retry attempts")
    parser.add_argument("--permissions", help="File permissions (e.g., 644)")
    parser.add_argument("--storage-class", help="S3 storage class")
    parser.add_argument("--throttle", type=int, help="Bandwidth limit (bytes/sec)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per file (sec)")
    
    # Execution options
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers")
    parser.add_argument("--pattern", default="*", help="File pattern for directory upload")
    parser.add_argument("--recursive", action="store_true", default=True, 
                       help="Recursive directory upload")
    
    # Output
    parser.add_argument("--output", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    # Load config file if provided
    if args.config:
        config = load_config(args.config)
        remote_url = config.get("remote_url")
        files = config.get("files", [])
        directory = config.get("directory")
        options = config.get("options", {})
        workers = config.get("workers", 5)
    else:
        if not args.remote:
            parser.error("--remote is required when not using --config")
        
        remote_url = args.remote
        files = args.files or []
        directory = args.directory
        options = {
            "verbose": args.verbose,
            "preserve": args.preserve,
            "retry": args.retry,
            "permissions": args.permissions,
            "storage_class": args.storage_class,
            "throttle": args.throttle,
            "timeout": args.timeout
        }
        workers = args.workers
    
    # Initialize uploader
    uploader = DuckBatchUploader(remote_url)
    
    # Upload files or directory
    if files:
        file_paths = [Path(f) for f in files]
        uploader.upload_batch(file_paths, options, workers)
    elif directory:
        uploader.upload_directory(
            Path(directory),
            options,
            args.pattern,
            args.recursive
        )
    
    # Save results if requested
    if args.output:
        uploader.save_results(args.output)
    
    # Exit with error code if any uploads failed
    failed = sum(1 for r in uploader.results if not r["success"])
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
