# PermissionModelAnalysisofAndroidApps
Problem Statement: To analyze a number of Android Applications and verify whether the permissions they ask for and utilize are in agreement with what they claim to do. 

Approach: Scouring through Application Descriptions, Manifest File, and API Calls.

Steps Involved:
1. Manual Analysis of Applications: A set of applications from all categories were analyzed and their action words were mapped to a set of specific permissions. For example: In Whatsapp’s Description, “uses Internet” was mapped to the permission group “Internet”. 
2. Creation of Database: The data obtained in Step 1 was transformed into a SQL Database. The action words (Verbs and Nouns) were stemmed to their root form for an efficient comparison. 
3. Retrieving Permissions Using Database: Action words (Verbs and Nouns) found in Application Description were scoured for in the Database, and their corresponding Permission Groups were retrieved. 
4. Retrieving Permissions from Manifest: Androguard (a Python based tool), was used to extract the Permissions from the Manifest file. A comparison of the Permissions obtained from the Manifest File and the ones from the Database was derived. 
5. API to Permission Mapping: The Permission Groups that did not have a corresponding API calls were flagged. This meant that those permissions were declared in the Manifest file, however they were not used in the Source Code, thus raising suspicion.  
Thus, a Result Set for several applications analyzed using the above steps was derived.
