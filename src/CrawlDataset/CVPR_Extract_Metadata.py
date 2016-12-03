'''
Created on Oct 15, 2015

@author: Dalei
'''
import os, sys, json

def extract_metadata(dataset_folder_name = '../Dataset/', metadata_name = 'metadata.json'):
    # extract metadata
    metadata = {}
    with open(dataset_folder_name + metadata_name, 'w') as f:
        for sub_folder_name in os.listdir(dataset_folder_name):
            if os.path.isdir(dataset_folder_name + sub_folder_name):
                metadata_folder = dataset_folder_name + sub_folder_name + '/Metadata/'
                metadata_files_list = os.listdir(metadata_folder)
                
                metadata_dict = {}
                for metadata_file in metadata_files_list:
                    with open(metadata_folder + metadata_file) as metadata_f:
                        metadata_dict[metadata_file[:7]] = json.loads(json.load(metadata_f))[0]['gatewayResponse']['records']['record'][0]
                    metadata_f.close()
                metadata[sub_folder_name] = metadata_dict
        
        json.dump(metadata, f)

    f.close()
    
    
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        extract_metadata()
    elif len(sys.argv) <= 2:
        extract_metadata(sys.argv[1])
    else:
        extract_metadata(sys.argv[1], sys.argv[2])