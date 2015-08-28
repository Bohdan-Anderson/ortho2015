from apiclient import discovery,errors
import oauth2client,os,httplib2,io
from oauth2client import client,tools
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload,MediaIoBaseUpload
from django.conf import settings
# from apiclient import errors


def insert_permission(service, file_id, value, perm_type, role):
	new_permission = {
		'value': value,
		'type': perm_type,
		'role': role
	}
	try:
		return service.permissions().insert(fileId=file_id, body=new_permission).execute()
	except errors.HttpError, error:
		print 'An error occurred: %s' % error
	return None

def getService():
	client_email = settings.CLIENT_EMAIL
	with open("%s/my.p12"%settings.BASE_DIR) as f:
		private_key = f.read()

	credentials = SignedJwtAssertionCredentials(client_email, private_key,'https://www.googleapis.com/auth/drive')
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v2', http=http)

	return service

def insert_file(service, title, description, parent_id, mime_type, filename):
	media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
	body = {
		'title': title,
		'description': description,
		'mimeType': mime_type
	}
	# Set the parent folder.
	if parent_id:
		body['parents'] = [{'id': parent_id}]

	try:
		file = service.files().insert(body=body,media_body=media_body).execute()
		return file
	except errors.HttpError, error:
		print 'An error occured: %s' % error
	return None



def insert_text(service, title, description, parent_id, mime_type, fileContent):
	body = {
		'title': "%s.txt"%title,
		'description': description,
		'mimeType': "text/plain"
	}
	media_body = MediaIoBaseUpload(fileContent, mimetype=mime_type)

	if parent_id:
		body['parents'] = [{'id': parent_id}]

	try:
		file = service.files().insert(body=body,media_body=media_body).execute()
		return file
	except errors.HttpError, error:
		print 'An error occured: %s' % error
	return None

# upLoadToGD(service,slug,dateString,self.cv,"%s's CV"%self.fullName,"application/pdf","cv")

# def upLoadToGD(service,name,dateString,field,description,fileType,descriptor):

# 	location = os.path.join(settings.MEDIA_ROOT,name)
# 	location = os.path.join(location,str(field))
# 	field = str(field)
# 	if(field and os.path.isfile(location)):
# 		# print location
# 		newFile = insert_file(service,"%s-%s-%s"%(dateString,name,descriptor),description,None,fileType,location)
# 		# print newFile
# 		try:
# 			insert_permission(service,newFile["id"],settings.SHARE_WITH_THIS_USER,"user","writer")
# 		except Exception, e:
# 			print e
# 	else:
# 		print "%s file failed to upload"%str(field)

# service, self.cv,self.fullName,"cv","application/pdf"
def upLoadToGD(service,uploadedName,folder,toBeName,fileType):
	location = os.path.join(settings.MEDIA_ROOT,str(uploadedName))
	print "\n\n========="
	print uploadedName
	print location
	print os.path.isfile(location)
	if(uploadedName and os.path.isfile(location)):
		newFile = insert_file(service, toBeName ,"",folder,fileType,location)
		return newFile["id"]
		try:
			insert_permission(service,newFile["id"],settings.SHARE_WITH_THIS_USER,"user","writer")
		except Exception, e:
			print e
	else:
		print "%s file failed to upload"%str(uploadedName)
		return None

def createFolder(service, newName):
	body = {
		'title': newName,
		'mimeType': "application/vnd.google-apps.folder",
	}
	body['parents'] = [{'id': settings.SHARE_FOLDER}]

	newFolder = service.files().insert(body=body).execute()
	try:
		insert_permission(service,newFolder["id"],settings.SHARE_WITH_THIS_USER,"user","writer")
	except Exception, e:
		print e
	return newFolder

def formData(service,name,dateString,data,folder):
	out = "Full Name:\t%s\nEmail:\t\t%s\nPhone:\t\t%s"%(data.fullName,data.email,data.phone)
	print out
	newFile = insert_text(service,"%s-%s-details"%(dateString,name),"%s's data"%data.fullName,folder,"application/octet-stream",io.BytesIO(out.encode('utf-8')))
	try:
		insert_permission(service,newFile["id"],settings.SHARE_WITH_THIS_USER,"user","writer")
	except Exception, e:
		print e
	return newFile["id"]


def delete_file(service, file_id):
	try:
		service.files().delete(fileId=file_id).execute()
	except errors.HttpError, error:
		print 'An error occurred: %s' % error

def delete_all_files(service):
	result = []
	page_token = None
	while True:
		try:
			param = {}
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()


			# delete_file(service,)
			result.extend(files['items'])
			page_token = files.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			break
	for f in result:
		delete_file(service,f["id"])
	return result
