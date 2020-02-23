from androguard.core.api_specific_resources import load_permission_mappings
from androguard.core.bytecodes.apk import APK
from androguard.misc import AnalyzeAPK

def static_code_analysis(apk_name):
	a,d,dx =AnalyzeAPK("C:/Users/KK/Desktop/Final Year Project/APK/"+apk_name)
	methods=[]
	methods1=[]

	#All methods that an application uses- Internal and External
	for c in dx.get_classes():
		methods1=(list(map(lambda x: x.name, c.get_methods())))
		methods+=methods1
	methods=set(methods)

	#Mapping: {API:List of Permissions}
	mapping = load_permission_mappings(a.get_min_sdk_version()) 
	
	print(a.get_min_sdk_version())
	#A dictionary : {External API: list of permissions}
	external_apis_permissions={}

	for key, value in mapping.items():
		for m in methods:
			if m==key.split('-')[1]:
				external_apis_permissions.update({key:value})

	#If permission_dangerous not in external_apis_permissions
	permissions_from_mapping=[]
	for key, value in external_apis_permissions.items():
		for x in value:
			permissions_from_mapping.append(x)
			permissions_from_mapping=list(set(permissions_from_mapping))

	return permissions_from_mapping
