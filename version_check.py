import requests
import zipfile
import os
import ast
import sys
import pickle
#import tqdm

name_cookies="csars.cookies"

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    download_url(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def download_url(r, save_path, chunk_size=1024):
    dl=0
    total_size_in_bytes= 26373 * 1024
    bar_length = 30  # should be less than 100
    try:
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                dl+= len(chunk)
                percent = int(100.0* dl/total_size_in_bytes)
                sys.stdout.write('\r')
                sys.stdout.write("Downloading: [{:{}}] {:>3}%   {}KB / {}KB"
                                  .format('='*int(percent/(100.0/bar_length)),
                                          bar_length, int(percent), int(dl/1024), total_size_in_bytes/1024))
                fd.write(chunk)
                sys.stdout.flush()
    except:
        r.close()

def db_check():
    try:
        s = requests.Session()
        try:
            with open(name_cookies,"rb") as f:
                s.cookies.update(pickle.load(f))
                f.close()
                    
        except Exception:
            print("Cookies not found")
            try:
                with open(name_cookies, 'wb') as f:
                    pickle.dump(s.cookies, f)
                    f.close()
            except Exception as e:
                print(e)
                print("\n\nEnable to store cookies.")
            
        respond = s.get("http://masterprojectsheep.000webhostapp.com/getVersion.php")        
        if respond.text == "Up-to-Date":
            return True
        else:
            v = ast.literal_eval(respond.text)
            return v
    
    except requests.exceptions.RequestException:
        input("Cannot connect to database...\nPlease check your internet connection and try it later.\n\nPress ENTER to exit.")
        raise SystemExit()

def version_check(current_version):
    print("Checking version...")
    v = db_check()
    if isinstance(v, dict) or v==True:
        if current_version < v["version"]:
            print("Your version is",current_version,"\nDownlading lastest version (v",v["version"],")")
            download_file_from_google_drive(v["file_id"], v["file_name"])   
            path = os.path.dirname(os.path.abspath(__file__))
            upper = path[:path.rfind("\\")]
            file = path[path.rfind("\\"):]
            print("\nExtracting to ", upper)
            try:
                with zipfile.ZipFile(v["file_name"], 'r') as zip_ref:
                    zFile = zip_ref.namelist()[0][:-1]
                    zip_ref.extractall(upper)
            
            except Exception as e:
                print("Error")
                with open("vc_log.txt","w") as f:
                    f.write(e)
                    f.close()
            input("\n\nNew version of CSARS is in the same location with the old one.\nPlease relaunch the system.\n\nPress Enter to exit.")
            return False
        else:
            print("Recommendation System is Up-to-Date")
            return True
    else:
        print("Something wrong when downloading the new version CSARS..")
        print("\nYou can go to masterprojectsheep.000webhostapp.com/download.html for downlaod")
        input("\n\nPress Enter to exit.")
        return False