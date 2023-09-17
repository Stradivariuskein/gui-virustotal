import hashlib
from virus_total_apis import PublicApi
from os.path import getsize
from time import sleep

API_KEY = "285c15e5ffc7ea112a96f3069d787f98335a086e2b2defd2532d1886528a3ca3"

def size_more_32(path): # valida si un archivo es mayor a 32mb 
    size = getsize(path)
    if size >= 33554432:
        return True
    return False


def send_request_file(arch):
    api = PublicApi(API_KEY)


    #Abrimos el archivo
    

    with open(arch, "rb") as file:

        file_md5 = hashlib.md5(file.read()).hexdigest()
    response = api.get_file_report(file_md5)
    filtered_response = {}
    if response["response_code"] == 200:
        list_positives = []
        list_relevant_av = []
        list_others = []
        
        #print(f"{response['results']['positives']} / {response['results']['total']}")
        filtered_response["positive_relevant"] = False
        try:
            filtered_response["positives"] = response['results']['positives']
            filtered_response["total"] = response['results']['total']
        except Exception as e:
            if not size_more_32(arch):
                api.scan_file(arch)
                while True:
                    response = api.get_file_report(file_md5)
                    try:
                        response['results']['positives']
                        break
                    except KeyError:
                        sleep(7)
                filtered_response["positives"] = response['results']['positives']
                filtered_response["total"] = response['results']['total']
            else:
                raise "longFile: The file exceeds the maximum size (32MB) allowed for uploading."
            


        for anti_virus, value in response["results"]["scans"].items():
    
            if value["detected"] == True:
                list_positives.append(anti_virus)
            elif anti_virus == "Panda" or anti_virus == "Microsoft" or anti_virus == "Google" or anti_virus == "Kaspersky " or anti_virus == "AVG":
                list_relevant_av.append(anti_virus)
                if value["detected"] == True:
                    filtered_response["positive_relevant"] = True
            else:
                list_others.append(anti_virus)
        aux_dic = {}
        for key in list_positives:
            aux_dic[key] = response["results"]["scans"][key]

        filtered_response["positives_sacans"] = aux_dic
        aux_dic = {}
        for key in list_relevant_av:
            aux_dic[key] = response["results"]["scans"][key]
        
        filtered_response["relevant_scans"] = aux_dic
        aux_dic = {}

        for key in list_others:
            aux_dic[key] = response["results"]["scans"][key]

        filtered_response["others_scans"] = aux_dic




    
    
    '''print("------------------------------------------------------")
    print(f"{filtered_response['positive_relevant']} || {filtered_response['positives']} || {filtered_response['total']}")
    print("------------------------------------------------------")
    print(filtered_response["positives_sacans"])
    print("------------------------------------------------------")
    print(filtered_response["relevant_scans"])
    print("------------------------------------------------------")
    print(filtered_response["others_scans"])
    print("------------------------------------------------------")'''

    return filtered_response



#send_request_file("MaxPayne3.exe")