#!/usr/bin/env python3
"""
File Generator - Exponential Growth
Creates files in exponentially increasing quantities and sizes.
WARNING: This will fill up disk space quickly. Use only in isolated VMs.
"""

import os
import time
from pathlib import Path

# Configuration
INITIAL_FILES = 5
INITIAL_FILE_SIZE = 1024  # 1 KB
OUTPUT_DIR = "generated_files"
DELAY_SECONDS = 2  # Delay between batches to observe progress

def create_file(filepath, size_bytes):
    """Create a file with random data of specified size."""
    with open(filepath, 'wb') as f:
        # Write in chunks to handle large files
        chunk_size = min(size_bytes, 1024 * 1024)  # 1 MB chunks
        remaining = size_bytes
        
        while remaining > 0:
            write_size = min(chunk_size, remaining)
            f.write(os.urandom(write_size))
            remaining -= write_size

def format_size(bytes_size):
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def main():
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    print("=" * 60)
    print("FILE GENERATOR - EXPONENTIAL GROWTH")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Initial files: {INITIAL_FILES}")
    print(f"Initial size: {format_size(INITIAL_FILE_SIZE)}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Initial batch
    num_files = INITIAL_FILES
    file_size = INITIAL_FILE_SIZE
    batch = 0
    total_files = 0
    
    try:
        while True:
            batch += 1
            print(f"Batch {batch}: Creating {num_files} files of {format_size(file_size)} each...")
            
            start_time = time.time()
            
            for i in range(num_files):
                filename = f"batch_{batch:04d}_file_{i:06d}.dat"
                filepath = os.path.join(OUTPUT_DIR, filename)
                create_file(filepath, file_size)
            
            elapsed = time.time() - start_time
            total_files += num_files
            total_size = total_files * file_size
            
            print(f"  ✓ Created {num_files} files in {elapsed:.2f}s")
            print(f"  Total files: {total_files:,} | Total size: {format_size(total_size)}")
            print()
            
            # Double for next iteration
            num_files *= 2
            file_size *= 2
            
            # Brief delay to observe progress
            time.sleep(DELAY_SECONDS)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Stopped by user")
        print(f"Final stats: {total_files:,} files created")
        print("=" * 60)
    except Exception as e:
        print(f"\nError occurred: {e}")
        print(f"Completed {batch} batches with {total_files:,} files")

if __name__ == "__main__":
    main()
