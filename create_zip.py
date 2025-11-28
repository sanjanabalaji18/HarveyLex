
import os
import zipfile

def should_exclude(path, exclude_list):
    for exclude_pattern in exclude_list:
        if exclude_pattern in path:
            return True
    return False

def zip_directory(path, zip_handle, exclude_list):
    for root, dirs, files in os.walk(path):
        # Prune directories to prevent walking into them
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclude_list)]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not should_exclude(file_path, exclude_list):
                arcname = os.path.relpath(file_path, path)
                zip_handle.write(file_path, arcname)

if __name__ == '__main__':
    project_dir = os.getcwd()
    output_zip_file = os.path.join(os.path.dirname(project_dir), 'harvey-lex.zip')
    
    # Define parts of paths to exclude. This is more robust.
    exclude_patterns = [
        '/node_modules/',
        '/venv/',
        '/__pycache__/',
        '/.pytest_cache/',
        '/dist/',
        '/.git/',
        '.log',
        '.pid',
        '.DS_Store',
        '.env',
        'harvey-lex.zip', # Exclude the zip file itself
        'create_zip.py'
    ]

    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zip_directory(project_dir, zipf, exclude_patterns)

    print(f"Project zipped successfully to {output_zip_file}")
