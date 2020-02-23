from androguard.core.bytecodes.apk import APK
from permission_script import permission_dictionary

def manifest_analysis(permissions_manifest):
	permission_class=[]
	for item in range (len(permissions_manifest)):
		if(permissions_manifest[item] in permission_dictionary.keys()):
			if permission_dictionary.get(permissions_manifest[item]) != "dangerous":
					permission_class.append(permission_dictionary.get(permissions_manifest[item]).upper())
			else:
					permission_class.append(permissions_manifest[item].upper())
	return permission_class