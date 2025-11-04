# 📁 File Organiser
A lightweight Python utility which organises files based on file type.

## Features
- Automatically sorts files into subfolders by type (images, documents, etc.)
- Supports a dry run to preview file movement
- Generates a history log of all actions
- Can undo last file organisation session
- Cleans up empty folders
- Fully CLI-based, no GUI or dependencies

## Usage
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/file-organiser.git
   cd file-organiser
   ```
2. Run the script:
   ```bash
   python3 file_organiser.py
   ```
3. Select an option from the menu.

## Example Output
```
Enter folder path: /home/jim/Documents
 * Locating /home/jim/Documents
 * Logging actions.
 * Files have been organised.
```
History logs are automatically saved to `file_organiser_history.txt`.

## Requirements
- Python 3.8 or higher
- No external libraries (only os, time, datetime, shutil)

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE).

## Author
**Jim** / [mcdoods](https://github.com/mcdoods)
