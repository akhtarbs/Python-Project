# Akhtar Code
# Python Script to Remove Empty Folder in a Directory

import os

def remove_empty_folders(directory_path):    
    # Explore all directory 
    for root, dirs, files in os.walk(directory_path, topdown=False):
        
        # Get folder name
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            try:
                if not os.listdir(folder_path):
                    # Remove the empty folder
                    os.rmdir(folder_path)
            except OSError:
                pass  # Ignore files and non-empty directories
            else:
                print("Removed the empty directory : "+folder_path)   
                                                                                                             
    return print("Done")


# Call the function to remove empty fodler
remove_empty_folders("C:\\Users\\Music")


