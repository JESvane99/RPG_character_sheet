from pathlib import Path
import os

# Path to the database file
db_path = Path(__file__).parent / 'instance' / 'CharSheet_test.db'

# If the database file exists, delete it
if db_path.exists():
    db_path.unlink()
    print('Database file deleted.')
else:
    print('Database file not found.')
    
# Path to database backup file
backup_path = Path(__file__).parent / 'db_backup'

backup_files = list(backup_path.glob('*.db'))

# If there are backup files, restore the most recent one
if backup_files:
    backup_files.sort(key=lambda x: x.name, reverse=True)
    backup_file = backup_files[0]
    print(f'Restoring database from {backup_file.name}...')
    db_reset = os.popen(f'copy {backup_file} {db_path}').read()
    print(f'{db_reset}')
    
