import re
import csv
import sys
import os
import pandas as pd
import requests

global columns
columns = {}
global prefixes
prefixes = {}

def inner_values(row,dic,triples_map_list):
    values = ""
    for inputs in dic["inputs"]:
        if "reference" == inputs[1]:
            values += str(row[inputs[0]])
        elif "reference function" == inputs[1]:
            temp_dics = {}
            for tp in triples_map_list:
                if tp.triples_map_id == inputs[0]:
                    temp_dic = create_dictionary(tp)
                    current_func = {"inputs":temp_dic["inputs"], 
                                    "function":temp_dic["executes"],
                                    "func_par":temp_dic,
                                    "termType":True}
                    values += inner_values(row,temp_dic,triples_map_list)
    return values

def inner_function_exists(inner_func, inner_functions):
    for inner_function in inner_functions:
        if inner_func["id"] in inner_function["id"]:
            return False
    return True

########################################################
################## EABlock Functions ###################
########################################################

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

def falcon_wikipedia_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=short'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities_wikidata']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities[0].replace('<','').replace('>','')
    else:
        return ""           

def falcon_dbpedia_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/api?mode=short'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities[0]
    else:
        return ""          

def falcon_UMLS_CUI_function():
    value = global_dic["value"]
    output = ""
    url = 'https://labs.tib.eu/sdm/biofalcon/api?mode=short'
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        if len(response['entities'][1])>0:
            return response['entities'][1][0]
        else:
            return ""
    else:
        return ""

def falcon_wikipedia_description_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=long'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities_wikidata']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities_wikidata']:
                entities.append(result[0])
    if len(entities) >= 1:
        return list(str(entities[i]).replace('<','').replace('>','') for i in range (0, len(entities)))
    else:
        return ""           

def falcon_dbpedia_description_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/api?mode=long'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+str(text)+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities
    else:
        return ""            

def falcon_UMLS_CUI_description_function(value):
    output = ""
    url = 'http://node3.research.tib.eu:5005/api_umls?mode=long&type=cui'
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        entity_list = response['entities']
        return list(entity_list[i][0][1] for i in range (0, len(entity_list)))
    else:
        return ""

########################################################
def prefix_extraction(original, uri):
    url = ""
    value = ""
    if prefixes:
        if "#" in uri:
            url, value = uri.split("#")[0]+"#", uri.split("#")[1]
        else:
            value = uri.split("/")[len(uri.split("/"))-1]
            char = ""
            temp = ""
            temp_string = uri
            while char != "/":
                temp = temp_string
                temp_string = temp_string[:-1]
                char = temp[len(temp)-1]
            url = temp
    else:
        f = open(original,"r")
        original_mapping = f.readlines()
        for prefix in original_mapping:
            if ("prefix" in prefix) or ("base" in prefix):
               elements = prefix.split(" ")
               prefixes[elements[2][1:-1]] = elements[1][:-1]
            else:
                break
        f.close()
        if "#" in uri:
            url, value = uri.split("#")[0]+"#", uri.split("#")[1]
        else:
            value = uri.split("/")[len(uri.split("/"))-1]
            char = ""
            temp = ""
            temp_string = uri
            while char != "/":
                temp = temp_string
                temp_string = temp_string[:-1]
                char = temp[len(temp)-1]
            url = temp
    return prefixes[url], url, value

def update_mapping(triple_maps, dic, output, original, join, data_source):
    mapping = ""
    for triples_map in triple_maps:

        if triples_map.function:
            pass
        else:
            if "#" in triples_map.triples_map_id:
                mapping += "<" + triples_map.triples_map_id.split("#")[1] + ">\n"
            else: 
                mapping += "<" + triples_map.triples_map_id + ">\n"

            mapping += "    a rr:TriplesMap;\n"
            if triples_map.triples_map_id in data_source:
                mapping += "    rml:logicalSource [ rml:source \"" + data_source[triples_map.triples_map_id] +"\";\n"
            else:
                mapping += "    rml:logicalSource [ rml:source \"" + triples_map.data_source +"\";\n"
            if str(triples_map.file_format).lower() == "csv" and triples_map.query == "None": 
                mapping += "                rml:referenceFormulation ql:CSV\n" 
            mapping += "                ];\n"

            
            mapping += "    rr:subjectMap [\n"
            if triples_map.subject_map.subject_mapping_type is "template":
                mapping += "        rr:template \"" + triples_map.subject_map.value + "\";\n"
            elif triples_map.subject_map.subject_mapping_type is "reference":
                mapping += "        rml:reference \"" + triples_map.subject_map.value + "\";\n"
                mapping += "        rr:termType rr:IRI\n"
            elif triples_map.subject_map.subject_mapping_type is "constant":
                mapping += "        rr:constant \"" + triples_map.subject_map.value + "\";\n"
                mapping += "        rr:termType rr:IRI\n"
            elif triples_map.subject_map.subject_mapping_type is "function":
                for tp in triple_maps:
                    if tp.triples_map_id == triples_map.subject_map.value:
                        temp_dic = create_dictionary(tp)
                        mapping += "        rml:reference \"" + temp_dic["executes"].split("/")[len(temp_dic["executes"].split("/"))-1] + "_"+ tp.triples_map_id + "\";\n"
                        mapping += "        rr:termType rr:IRI\n"
            if triples_map.subject_map.rdf_class is not None:
                prefix, url, value = prefix_extraction(original, triples_map.subject_map.rdf_class)
                mapping += "        rr:class " + prefix + ":" + value  + "\n"
            mapping += "    ];\n"

            for predicate_object in triples_map.predicate_object_maps_list:
                if predicate_object.predicate_map.mapping_type is not "None":
                    mapping += "    rr:predicateObjectMap [\n"
                    if "constant" in predicate_object.predicate_map.mapping_type :
                        prefix, url, value = prefix_extraction(original, predicate_object.predicate_map.value)
                        mapping += "        rr:predicate " + prefix + ":" + value + ";\n"
                    elif "constant shortcut" in predicate_object.predicate_map.mapping_type:
                        prefix, url, value = prefix_extraction(original, predicate_object.predicate_map.value)
                        mapping += "        rr:predicate " + prefix + ":" + value + ";\n"
                    elif "template" in predicate_object.predicate_map.mapping_type:
                        mapping += "        rr:predicateMap[\n"
                        mapping += "            rr:template \"" + predicate_object.predicate_map.value + "\"\n"  
                        mapping += "        ];\n"
                    elif "reference" in predicate_object.predicate_map.mapping_type:
                        mapping += "        rr:predicateMap[\n"
                        mapping += "            rml:reference \"" + predicate_object.predicate_map.value + "\"\n" 
                        mapping += "        ];\n"

                    mapping += "        rr:objectMap "
                    if "constant" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:constant \"" + predicate_object.object_map.value + "\"\n"
                        mapping += "        ]\n"
                    elif "template" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:template  \"" + predicate_object.object_map.value + "\"\n"
                        mapping += "        ]\n"
                    elif "reference" == predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rml:reference \"" + predicate_object.object_map.value + "\"\n"
                        mapping += "        ]\n"
                    elif "parent triples map function" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                        mapping += "        rr:joinCondition [\n"
                        mapping += "            rr:child <" + predicate_object.object_map.child + ">;\n"
                        mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                        mapping += "        ]\n"
                    elif "parent triples map parent function" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                        mapping += "        rr:joinCondition [\n"
                        mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                        mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                        mapping += "        ]\n"
                    elif "parent triples map child function" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                        mapping += "        rr:joinCondition [\n"
                        mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                        mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                        mapping += "        ]\n"
                    elif "parent triples map" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        if (predicate_object.object_map.child is not None) and (predicate_object.object_map.parent is not None):
                            mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">\n"
                            mapping = mapping[:-1]
                            mapping += ";\n"
                            mapping += "        rr:joinCondition [\n"
                            mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                            mapping += "            rr:parent \"" + predicate_object.object_map.parent + "\";\n"
                            mapping += "        ]\n"
                        else:
                            if triples_map.triples_map_id in data_source:
                                mapping = mapping[:-1]
                                for tm in triple_maps:
                                    if tm.triples_map_id == predicate_object.object_map.value:
                                        if tm.subject_map.subject_mapping_type == "constant":
                                            mapping += "\n            rr:constant \"" + tm.subject_map.value + "\";\n"
                                            mapping += "            rr:termType rr:IRI\n"
                                        elif tm.subject_map.subject_mapping_type == "function":
                                            for func in triple_maps:
                                                if tm.subject_map.value == func.triples_map_id:
                                                    temp_dic = create_dictionary(func)
                                                    mapping += "\n        rml:reference \"" + temp_dic["executes"].split("/")[len(temp_dic["executes"].split("/"))-1] + "_" + func.triples_map_id + "\";\n"
                                                    mapping += "        rr:termType rr:IRI\n"
                                        else:
                                            mapping += "\n"
                                            mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                                            if tm.subject_map.subject_mapping_type == "function":
                                                for func in triple_maps:
                                                    if tm.subject_map.value == func.triples_map_id:
                                                        temp = create_dictionary(func)
                                                        temp_dic = {"inputs":temp["inputs"], 
                                                                    "function":temp["executes"],
                                                                    "func_par":temp}
                                                        for attr in temp_dic["inputs"]:
                                                            if "reference function" not in attr[1] and "constant" not in attr[1]:
                                                                mapping += "        rr:joinCondition [\n"
                                                                mapping += "            rr:child \"" + attr[0] + "\";\n"
                                                                mapping += "            rr:parent \"" + attr[0] +"\";\n"
                                                                mapping += "            ];\n"
                                            else:    
                                                if "{" in tm.subject_map.value:
                                                    for string in tm.subject_map.value.split("{"):
                                                        if "}" in string:
                                                            subject_value = string.split("}")[0]
                                                            mapping += "        rr:joinCondition [\n" 
                                                            mapping += "            rr:child \"" + subject_value  + "\";\n"
                                                            mapping += "            rr:parent \"" + subject_value + "\";\n"
                                                            mapping += "        ];\n"
                                                else:
                                                    mapping += "        rr:joinCondition [\n" 
                                                    mapping += "            rr:child \"" + tm.subject_map.value  + "\";\n"
                                                    mapping += "            rr:parent \"" + tm.subject_map.value + "\";\n"
                                                    mapping += "        ];\n"
                        mapping += "        ]\n"
                    elif "constant shortcut" in predicate_object.object_map.mapping_type:
                        mapping += "[\n"
                        mapping += "        rr:constant \"" + predicate_object.object_map.value + "\"\n"
                        mapping += "        ]\n"
                    elif "reference function" in predicate_object.object_map.mapping_type:
                        if join:
                            mapping += "[\n"
                            if predicate_object.object_map.value in dic:
                                mapping += "        rr:parentTriplesMap <" + dic[predicate_object.object_map.value]["output_name"] + ">;\n"
                                for attr in dic[predicate_object.object_map.value]["inputs"]:
                                    if ("reference function" in attr[1]):
                                        for tp in triple_maps:
                                            if tp.triples_map_id == attr[0]:
                                                temp_dic = create_dictionary(tp)
                                                mapping += "        rr:joinCondition [\n"
                                                mapping += "            rr:child \"" + temp_dic["executes"].split("/")[len(temp_dic["executes"].split("/"))-1] + "\";\n"
                                                mapping += "            rr:parent \"" + temp_dic["executes"].split("/")[len(temp_dic["executes"].split("/"))-1] +"\";\n"
                                                mapping += "            ];\n"
                                                break
                                    elif (attr[1] is not "constant"):
                                        mapping += "        rr:joinCondition [\n"
                                        mapping += "            rr:child \"" + attr[0] + "\";\n"
                                        mapping += "            rr:parent \"" + attr[0] +"\";\n"
                                        mapping += "            ];\n"
                                mapping += "        ];\n"
                            else:
                                for tp in triple_maps:
                                    if tp.triples_map_id == predicate_object.object_map.value:
                                        temp_dic = create_dictionary(tp)
                                        mapping += "        rml:reference \"" + temp_dic["executes"].split("/")[len(temp_dic["executes"].split("/"))-1] + "_" + tp.triples_map_id + "\";\n"
                                        mapping += "        rr:termType rr:IRI\n"
                                        mapping += "        ];\n"
                        else:
                            mapping += "[\n"
                            mapping += "        rml:reference \"" + dic[predicate_object.object_map.value]["output_name"] + "\";\n"
                            mapping += "        rr:termType rr:IRI\n"
                            mapping += "        ];\n"
                    mapping += "    ];\n"
            if triples_map.function:
                pass
            else:
                mapping = mapping[:-2]
                mapping += ".\n\n"

    if join:
        for function in dic.keys():
            mapping += "<" + dic[function]["output_name"] + ">\n"
            mapping += "    a rr:TriplesMap;\n"
            mapping += "    rml:logicalSource [ rml:source \"" + dic[function]["output_file"] +"\";\n"
            if "csv" in dic[function]["output_file"]:
                mapping += "                rml:referenceFormulation ql:CSV\n" 
            mapping += "            ];\n"
            mapping += "    rr:subjectMap [\n"
            mapping += "        rml:reference \"" + dic[function]["output_name"] + "\";\n"
            mapping += "        rr:termType rr:IRI\n"
            mapping += "    ].\n\n"

    prefix_string = ""
    
    f = open(original,"r")
    original_mapping = f.readlines()
    for prefix in original_mapping:
        if ("prefix" in prefix) or ("base" in prefix):
           prefix_string += prefix
        else:
            break
    f.close()  

    prefix_string += "\n"
    prefix_string += mapping

    mapping_file = open(output + "/transfered_mapping.ttl","w")
    mapping_file.write(prefix_string)
    mapping_file.close()

def update_mapping_rdb(triple_maps, dic, output, original, join, data_source):
    mapping = ""
    for triples_map in triple_maps:

        if triples_map.function:
            pass
        else:
            if "#" in triples_map.triples_map_id:
                mapping += "<#" + triples_map.triples_map_id.split("#")[1] + ">\n"
            else: 
                mapping += "<#" + triples_map.triples_map_id + ">\n"

            mapping += "    a rr:TriplesMap;\n"
            if data_source:
                mapping += "    rml:logicalSource [ rml:source <DB_source>;\n"
                mapping += "                        rr:tableName \"" + data_source[triples_map.triples_map_id] + "\";\n"
            else:
                mapping += "    rml:logicalSource [ rml:source <DB_source>;\n"
                mapping += "                        rr:tableName \"" + triples_map.tablename + "\";\n"
            if triples_map.query != "None": 
                mapping += "                rml:query \"" + triples_map.query +"\"\n" 
            mapping += "                ];\n"

            
            mapping += "    rr:subjectMap [\n"
            if triples_map.subject_map.subject_mapping_type is "template":
                mapping += "        rr:template \"" + triples_map.subject_map.value + "\";\n"
            elif triples_map.subject_map.subject_mapping_type is "reference":
                mapping += "        rml:reference " + triples_map.subject_map.value + ";\n"
            elif triples_map.subject_map.subject_mapping_type is "constant":
                mapping += "        rr:constant " + triples_map.subject_map.value + ";\n"
            elif triples_map.subject_map.subject_mapping_type is "function":
                mapping = mapping[:-2]
                mapping += "<" + triples_map.subject_map.value + ">;\n"
            if triples_map.subject_map.rdf_class is not None:
                prefix, url, value = prefix_extraction(original, triples_map.subject_map.rdf_class)
                mapping += "        rr:class " + prefix + ":" + value  + "\n"
            mapping += "    ];\n"

            for predicate_object in triples_map.predicate_object_maps_list:
                
                mapping += "    rr:predicateObjectMap [\n"
                if "constant" in predicate_object.predicate_map.mapping_type :
                    prefix, url, value = prefix_extraction(original, predicate_object.predicate_map.value)
                    mapping += "        rr:predicate " + prefix + ":" + value + ";\n"
                elif "constant shortcut" in predicate_object.predicate_map.mapping_type:
                    prefix, url, value = prefix_extraction(original, predicate_object.predicate_map.value)
                    mapping += "        rr:predicate " + prefix + ":" + value + ";\n"
                elif "template" in predicate_object.predicate_map.mapping_type:
                    mapping += "        rr:predicateMap[\n"
                    mapping += "            rr:template \"" + predicate_object.predicate_map.value + "\"\n"  
                    mapping += "        ];\n"
                elif "reference" in predicate_object.predicate_map.mapping_type:
                    mapping += "        rr:predicateMap[\n"
                    mapping += "            rml:reference \"" + predicate_object.predicate_map.value + "\"\n" 
                    mapping += "        ];\n"

                mapping += "        rr:objectMap "
                if "constant" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:constant \"" + predicate_object.object_map.value + "\"\n"
                    mapping += "        ]\n"
                elif "template" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:template  \"" + predicate_object.object_map.value + "\"\n"
                    mapping += "        ]\n"
                elif "reference" == predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rml:reference \"" + predicate_object.object_map.value + "\"\n"
                    mapping += "        ]\n"
                elif "parent triples map function" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                    mapping += "        rr:joinCondition [\n"
                    mapping += "            rr:child <" + predicate_object.object_map.child + ">;\n"
                    mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                    mapping += "        ]\n"
                elif "parent triples map parent function" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                    mapping += "        rr:joinCondition [\n"
                    mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                    mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                    mapping += "        ]\n"
                elif "parent triples map child function" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">;\n"
                    mapping += "        rr:joinCondition [\n"
                    mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                    mapping += "            rr:parent <" + predicate_object.object_map.parent + ">;\n"
                    mapping += "        ]\n"
                elif "parent triples map" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:parentTriplesMap <" + predicate_object.object_map.value + ">\n"
                    if (predicate_object.object_map.child is not None) and (predicate_object.object_map.parent is not None):
                        mapping = mapping[:-1]
                        mapping += ";\n"
                        mapping += "        rr:joinCondition [\n"
                        mapping += "            rr:child \"" + predicate_object.object_map.child + "\";\n"
                        mapping += "            rr:parent \"" + predicate_object.object_map.parent + "\";\n"
                        mapping += "        ]\n"
                    mapping += "        ]\n"
                elif "constant shortcut" in predicate_object.object_map.mapping_type:
                    mapping += "[\n"
                    mapping += "        rr:constant \"" + predicate_object.object_map.value + "\"\n"
                    mapping += "        ]\n"
                elif "reference function" in predicate_object.object_map.mapping_type:
                    if join:
                        mapping += "[\n"
                        mapping += "        rr:parentTriplesMap <#" + dic[predicate_object.object_map.value]["output_name"] + ">;\n"
                        for attr in dic[predicate_object.object_map.value]["inputs"]:
                            if attr[1] is not "constant":
                                mapping += "        rr:joinCondition [\n"
                                mapping += "            rr:child \"" + attr[0] + "\";\n"
                                mapping += "            rr:parent \"" + attr[0] +"\";\n"
                                mapping += "            ];\n"
                        mapping += "        ];\n"
                    else:
                        mapping += "[\n"
                        mapping += "        rml:reference \"" + dic[predicate_object.object_map.value]["output_name"] + "\";\n"
                        mapping += "        ];\n"
                mapping += "    ];\n"
            if triples_map.function:
                pass
            else:
                mapping = mapping[:-2]
                mapping += ".\n\n"

    if join:
        for function in dic.keys():
            mapping += "<#" + dic[function]["output_name"] + ">\n"
            mapping += "    a rr:TriplesMap;\n"
            mapping += "    rml:logicalSource [ rml:source \"" + dic[function]["output_file"] +"\";\n"
            if "csv" in dic[function]["output_file"]:
                mapping += "                rml:referenceFormulation ql:CSV\n" 
            mapping += "            ];\n"
            mapping += "    rr:subjectMap [\n"
            if dic[function]["termType"]:
                mapping += "        rml:reference \"" + dic[function]["output_name"] + "\";\n"
                mapping += "        rr:termType rr:IRI\n"
            else:
                mapping += "        rml:reference \"" + dic[function]["output_name"] + "\"\n"
            mapping += "    ].\n\n"

    prefix_string = ""
    db_source = "<#DB_source> a d2rq:Database;\n"
    
    f = open(original,"r")
    original_mapping = f.readlines()
    for prefix in original_mapping:
        if "prefix;" in prefix or "d2rq:Database;" in prefix:
            pass
        elif ("prefix" in prefix) or ("base" in prefix):
           prefix_string += prefix
        elif "jdbcDSN" in prefix:
            db_source +=  prefix 
        elif "jdbcDriver" in prefix:
            db_source += prefix 
        elif "d2rq:username" in prefix:
            db_source += prefix 
        elif "d2rq:password" in prefix:
            db_source += prefix 
    f.close()  

    prefix_string += "\n"
    prefix_string += mapping

    prefix_string += db_source 
    
    mapping_file = open(output + "/transfered_mapping.ttl","w")
    mapping_file.write(prefix_string)
    mapping_file.close()

def execute_function(row,dic):
    if "tolower" in dic["function"]:
        return tolower(row[dic["func_par"]["value"]])
    elif "toupper" in dic["function"]:
        return toupper(row[dic["func_par"]["value"]])
    elif "totitle" in dic["function"]:
        return totitle(row[dic["func_par"]["value"]])
    elif "trim" in dic["function"]:
        return trim(row[dic["func_par"]["value"]])
    elif "chomp" in dic["function"]:
        return chomp(row[dic["func_par"]["value"]],dic["func_par"]["toremove"])
    elif "substring" in dic["function"]:
        if "index2" in dic["func_par"].keys():
            return substring(row[dic["func_par"]["value"]],dic["func_par"]["index1"],dic["func_par"]["index2"])
        else:
            return substring(row[dic["func_par"]["value"]],dic["func_par"]["index1"],None)
    elif "replaceValue" in dic["function"]:
        return replaceValue(row[dic["func_par"]["value"]],dic["func_par"]["value2"],dic["func_par"]["value3"])
    elif "match" in dic["function"]:
        return match(dic["func_par"]["regex"],row[dic["func_par"]["value"]])
    elif "variantIdentifier" in dic["function"]:
        return variantIdentifier(row[dic["func_par"]["column1"]],row[dic["func_par"]["column2"]],dic["func_par"]["prefix"])
    elif "condreplace" in dic["function"]:
        return condreplace(row[dic["func_par"]["value"]],dic["func_par"]["value1"],dic["func_par"]["value2"],dic["func_par"]["replvalue1"],dic["func_par"]["replvalue2"])
    elif "concat2" in dic["function"]:
        for inputs in dic["func_par"]["inputs"]:
            if dic["func_par"]["value1"] in inputs:
                if "constant" in inputs:
                    value1 = dic["func_par"]["value1"]
                else:
                    value1 = row[dic["func_par"]["value1"]]
            elif dic["func_par"]["value2"] in inputs:
                if "constant" in inputs:
                    value2 = dic["func_par"]["value2"]
                else:
                    value2 = row[dic["func_par"]["value2"]]
        if isinstance(value1,list) and isinstance(value2,list):
            output = []
            for v1 in value1:
                for v2 in value2:
                    output.append(concat2(v1,v2))
        elif isinstance(value1,list):
            output = []
            for v1 in value1:
                output.append(concat2(v1,value2))
        elif isinstance(value2,list):
            output = []
            for v2 in value2:
                output.append(concat2(value1,v2))
        else:
            output = concat2(value1,value2)
        return output
    elif "falcon_wikipedia_function" in dic["function"]:
        return falcon_wikipedia_function(row[dic["func_par"]["value"]])
    elif "falcon_dbpedia_function" in dic["function"]:
        return falcon_dbpedia_function(row[dic["func_par"]["value"]])    
    elif "falcon_UMLS_CUI_function" in dic["function"]:
        return falcon_UMLS_CUI_function(row[dic["func_par"]["value"]])
    elif "falcon_wikipedia_description_function" in dic["function"]:
        return falcon_wikipedia_description_function(row[dic["func_par"]["value"]])
    elif "falcon_dbpedia_description_function" in dic["function"]:
        return falcon_dbpedia_description_function(row[dic["func_par"]["value"]])    
    elif "falcon_UMLS_CUI_description_function" in dic["function"]:
        return falcon_UMLS_CUI_description_function(row[dic["func_par"]["value"]])            
    else:
        print("Invalid function")
        print("Aborting...")
        sys.exit(1)

def execute_function_mysql(row,header,dic):
    if "tolower" in dic["function"]:
        return tolower(row[header.index(dic["func_par"]["value"])])
    elif "toupper" in dic["function"]:
        return toupper(row[header.index(dic["func_par"]["value"])])
    elif "totitle" in dic["function"]:
        return totitle(row[header.index(dic["func_par"]["value"])])
    elif "trim" in dic["function"]:
        return trim(row[header.index(dic["func_par"]["value"])])
    elif "chomp" in dic["function"]:
        return chomp(row[header.index(dic["func_par"]["value"])],dic["func_par"]["toremove"])
    elif "substring" in dic["function"]:
        if "index2" in dic["func_par"].keys():
            return substring(row[header.index(dic["func_par"]["value"])],dic["func_par"]["index1"],dic["func_par"]["index2"])
        else:
            return substring(row[header.index(dic["func_par"]["value"])],dic["func_par"]["index1"],None)
    elif "replaceValue" in dic["function"]:
        return replaceValue(row[header.index(dic["func_par"]["value"])],dic["func_par"]["value2"],dic["func_par"]["value3"])
    elif "match" in dic["function"]:
        return match(dic["func_par"]["regex"],row[header.index(dic["func_par"]["value"])])
    elif "variantIdentifier" in dic["function"]:
        return variantIdentifier(row[header.index(dic["func_par"]["column1"])],row[header.index(dic["func_par"]["column2"])],dic["func_par"]["prefix"])
    elif "condreplace" in dic["function"]:
        return condreplace(row[header.index(dic["func_par"]["value"])],dic["func_par"]["value1"],dic["func_par"]["value2"],dic["func_par"]["replvalue1"],dic["func_par"]["replvalue2"])
    elif "falcon_call_wikidata" in dic["function"]:
        return falcon_call_wikidata(row[dic["func_par"]["value"]])
    elif "falcon_call_db" in dic["function"]:
        return falcon_call_db(row[dic["func_par"]["value"]]) 
    else:
        print("Invalid function")
        print("Aborting...")
        sys.exit(1)

def inner_function(row,dic,triples_map_list):

    functions = []
    keys = []
    for attr in dic["inputs"]:
        if ("reference function" in attr[1]):
            functions.append(attr[0])
        elif "constant" not in attr[1]:
            keys.append(attr[0])
    if functions:
        temp_dics = {}
        for function in functions:
            for tp in triples_map_list:
                if tp.triples_map_id == function:
                    temp_dic = create_dictionary(tp)
                    current_func = {"inputs":temp_dic["inputs"], 
                                    "function":temp_dic["executes"],
                                    "func_par":temp_dic,
                                    "termType":True}
                    temp_dics[function] = current_func
        temp_row = {}
        for dics in temp_dics:
            value = inner_function(row,temp_dics[dics],triples_map_list)
            temp_row[dics] = value
        for key in keys:
            temp_row[key] = row[key]
        return execute_function(temp_row,dic)
    else:
        return execute_function(row,dic)

def join_csv(source, dic, output):
    with open(dic["output_file"], "w") as temp_csv:
        writer = csv.writer(temp_csv, quoting=csv.QUOTE_ALL)

        keys = []
        for attr in dic["inputs"]:
            if attr[1] is not "constant":
                keys.append(attr[0])

        values = {}
        global columns
        
        if "variantIdentifier" in dic["function"]:

            if  dic["func_par"]["column1"]+dic["func_par"]["column2"] in columns:

                keys.append(dic["output_name"])
                writer.writerow(keys)

                for row in columns[dic["func_par"]["column1"]+dic["func_par"]["column2"]]:
                    if (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] not in values) and (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] is not None):
                        value = execute_function(row,dic)
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        line.append(value)
                        writer.writerow(line)
                        values[row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]]] = value

            else:
                reader = pd.read_csv(source, usecols=keys)
                reader = reader.where(pd.notnull(reader), None)
                reader = reader.to_dict(orient='records')
                keys.append(dic["output_name"])
                writer.writerow(keys)
                projection = []

                for row in reader:                   
                    if (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] not in values) and (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] is not None):
                        value = execute_function(row,dic)
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        line.append(value)
                        writer.writerow(line)
                        values[row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]]] = value
                        projection.append({dic["func_par"]["column1"]:row[dic["func_par"]["column1"]], dic["func_par"]["column2"]:row[dic["func_par"]["column2"]]})

                columns[dic["func_par"]["column1"]+dic["func_par"]["column2"]] = projection
        else:
            if dic["func_par"]["value"] in columns:

                keys.append(dic["output_name"])
                writer.writerow(keys)

                for row in columns[dic["func_par"]["value"]]:
                    if (row[dic["func_par"]["value"]] not in values) and (row[dic["func_par"]["value"]] is not None):
                        value = execute_function(row,dic)
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        if isinstance(value,list):
                            for v in value:
                                writer.writerow(line + [v])
                        else:
                            line.append(value)
                            writer.writerow(line)
                        values[row[dic["func_par"]["value"]]] = value

            else:

                reader = pd.read_csv(source, usecols=keys)
                reader = reader.where(pd.notnull(reader), None)
                reader = reader.to_dict(orient='records')
                keys.append(dic["output_name"])
                writer.writerow(keys)
                projection = []

                for row in reader:
                    if (row[dic["func_par"]["value"]] not in values) and (row[dic["func_par"]["value"]] is not None):
                        value = execute_function(row,dic)
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        if isinstance(value,list):
                            for v in value:
                                writer.writerow(line + [v])
                        else:
                            line.append(value)
                            writer.writerow(line)
                        values[row[dic["func_par"]["value"]]] = value
                        projection.append({dic["func_par"]["value"]:row[dic["func_par"]["value"]]})

                columns[dic["func_par"]["value"]] = projection

def join_csv_URI(source, dic, output):
    with open(dic["output_file"], "w") as temp_csv:
        writer = csv.writer(temp_csv, quoting=csv.QUOTE_ALL)

        keys = []
        for attr in dic["inputs"]:
            if attr[1] is not "constant":
                keys.append(attr[0])

        values = {}
        global columns
        
        if "variantIdentifier" in dic["function"]:

            if  dic["func_par"]["column1"]+dic["func_par"]["column2"] in columns:

                keys.append(dic["output_name"])
                writer.writerow(keys)

                for row in columns[dic["func_par"]["column1"]+dic["func_par"]["column2"]]:
                    if (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] not in values) and (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] is not None):
                        value = execute_function(row,dic) 
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        line.append(value)
                        writer.writerow(line)
                        values[row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]]] = value

            else:
                reader = pd.read_csv(source, usecols=keys)
                reader = reader.where(pd.notnull(reader), None)
                reader = reader.to_dict(orient='records')
                keys.append(dic["output_name"])
                writer.writerow(keys)
                projection = []

                for row in reader:                   
                    if (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] not in values) and (row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]] is not None):
                        value = execute_function(row,dic) 
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        line.append(value)
                        writer.writerow(line)
                        values[row[dic["func_par"]["column1"]]+row[dic["func_par"]["column2"]]] = value
                        projection.append({dic["func_par"]["column1"]:row[dic["func_par"]["column1"]], dic["func_par"]["column2"]:row[dic["func_par"]["column2"]]})

                columns[dic["func_par"]["column1"]+dic["func_par"]["column2"]] = projection
        else:
            if dic["func_par"]["value"] in columns:

                keys.append(dic["output_name"])
                writer.writerow(keys)

                for row in columns[dic["func_par"]["value"]]:
                    if (row[dic["func_par"]["value"]] not in values) and (row[dic["func_par"]["value"]] is not None):
                        value = execute_function(row,dic) 
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        if isinstance(value,list):
                            for v in value:
                                writer.writerow(line + [v])
                        else:
                            line.append(value)
                            writer.writerow(line)
                        values[row[dic["func_par"]["value"]]] = value

            else:

                reader = pd.read_csv(source, usecols=keys)
                reader = reader.where(pd.notnull(reader), None)
                reader = reader.to_dict(orient='records')
                keys.append(dic["output_name"])
                writer.writerow(keys)
                projection = []

                for row in reader:
                    if (row[dic["func_par"]["value"]] not in values) and (row[dic["func_par"]["value"]] is not None):
                        value = execute_function(row,dic)
                        line = []
                        for attr in dic["inputs"]:
                            if attr[1] is not "constant":
                                line.append(row[attr[0]])
                        if isinstance(value,list):
                            for v in value:
                                writer.writerow(line + [v])
                        else:
                            line.append(value)
                            writer.writerow(line)
                        values[row[dic["func_par"]["value"]]] = value
                        projection.append({dic["func_par"]["value"]:row[dic["func_par"]["value"]]})

                columns[dic["func_par"]["value"]] = projection


def create_dictionary(triple_map):
    dic = {}
    inputs = []
    for tp in triple_map.predicate_object_maps_list:
        if "#" in tp.predicate_map.value:
            key = tp.predicate_map.value.split("#")[1]
            tp_type = tp.predicate_map.mapping_type
        elif "/" in tp.predicate_map.value:
            key = tp.predicate_map.value.split("/")[len(tp.predicate_map.value.split("/"))-1]
            tp_type = tp.predicate_map.mapping_type
        if "constant" in tp.object_map.mapping_type:
            value = tp.object_map.value
            tp_type = tp.object_map.mapping_type
        elif "#" in tp.object_map.value:
            value = tp.object_map.value.split("#")[1]
            tp_type = tp.object_map.mapping_type
        elif "/" in tp.object_map.value:
            value = tp.object_map.value.split("/")[len(tp.object_map.value.split("/"))-1]
            tp_type = tp.object_map.mapping_type
        else:
            value = tp.object_map.value
            tp_type = tp.object_map.mapping_type

        dic.update({key : value})
        if (key != "executes") and ([value,tp_type] not in inputs):
            inputs.append([value,tp_type])

    dic["inputs"] = inputs
    return dic

def join_mysql(data, header, dic, db):
    values = {}
    cursor = db.cursor(buffered=True)
    create = "CREATE TABLE " + dic["output_file"] + " ( "
    if "variantIdentifier" in dic["function"]:
        create += "`" + dic["func_par"]["column1"] + "` varchar(300),\n"
        create += "`" + dic["func_par"]["column2"] + "` varchar(300),\n"
    else:
        create += "`" + dic["func_par"]["value"] + "` varchar(300),\n"
    create += "`" + dic["output_name"] + "` varchar(300));"
    cursor.execute(create)
    if "variantIdentifier" in dic["function"]:
        for row in data:
            if (row[header.index(dic["func_par"]["column1"])]+row[header.index(dic["func_par"]["column2"])] not in values) and (row[header.index(dic["func_par"]["column1"])]+row[header.index(dic["func_par"]["column2"])] is not None):
                value = execute_function_mysql(row,header,dic)
                line = "INSERT INTO " + dic["output_file"] + "\n"  
                line += "VALUES ("
                for attr in dic["inputs"]:
                    if attr[1] is not "constant":
                        line += "'" + row[header.index(attr[0])] + "', "
                line += "'" + value + "');"
                cursor.execute(line)
                values[row[header.index(dic["func_par"]["column1"])]+row[header.index(dic["func_par"]["column2"])]] = value
    else:
        for row in data:
            if (row[header.index(dic["func_par"]["value"])] not in values) and (row[header.index(dic["func_par"]["value"])] is not None):
                value = execute_function_mysql(row,header,dic)
                line = "INSERT INTO " + dic["output_file"] + "\n"  
                line += "VALUES ("
                for attr in dic["inputs"]:
                    if attr[1] is not "constant":
                        line += "'" + row[header.index(attr[0])] + "', "
                line += "'" + value + "');"
                cursor.execute(line)
                values[row[header.index(dic["func_par"]["value"])]] = value


def translate_sql(triples_map):

    query_list = []
    
    
    proyections = []

        
    if "{" in triples_map.subject_map.value:
        subject = triples_map.subject_map.value
        count = count_characters(subject)
        if (count == 1) and (subject.split("{")[1].split("}")[0] not in proyections):
            subject = subject.split("{")[1].split("}")[0]
            if "[" in subject:
                subject = subject.split("[")[0]
            proyections.append(subject)
        elif count > 1:
            subject_list = subject.split("{")
            for s in subject_list:
                if "}" in s:
                    subject = s.split("}")[0]
                    if "[" in subject:
                        subject = subject.split("[")
                    if subject not in proyections:
                        proyections.append(subject)

    for po in triples_map.predicate_object_maps_list:
        if "{" in po.object_map.value:
            count = count_characters(po.object_map.value)
            if 0 < count <= 1 :
                predicate = po.object_map.value.split("{")[1].split("}")[0]
                if "[" in predicate:
                    predicate = predicate.split("[")[0]
                if predicate not in proyections:
                    proyections.append(predicate)

            elif 1 < count:
                predicate = po.object_map.value.split("{")
                for po_e in predicate:
                    if "}" in po_e:
                        pre = po_e.split("}")[0]
                        if "[" in pre:
                            pre = pre.split("[")
                        if pre not in proyections:
                            proyections.append(pre)
        elif "#" in po.object_map.value:
            pass
        elif "/" in po.object_map.value:
            pass
        else:
            predicate = po.object_map.value 
            if "[" in predicate:
                predicate = predicate.split("[")[0]
            if predicate not in proyections:
                    proyections.append(predicate)
        if po.object_map.child != None:
            if po.object_map.child not in proyections:
                    proyections.append(po.object_map.child)

    temp_query = "SELECT DISTINCT "
    for p in proyections:
        if p is not "None":
            if p == proyections[len(proyections)-1]:
                temp_query += "`" + p + "`"
            else:
                temp_query += "`" + p + "`, " 
        else:
            temp_query = temp_query[:-2] 
    if triples_map.tablename != "None":
        temp_query = temp_query + " FROM " + triples_map.tablename + ";"
    else:
        temp_query = temp_query + " FROM " + triples_map.data_source + ";"
    query_list.append(temp_query)

    return triples_map.iterator, query_list

def count_characters(string):
    count = 0
    for s in string:
        if s == "{":
            count += 1
    return count
