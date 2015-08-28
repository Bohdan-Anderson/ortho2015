from django.db import models
from django.conf import settings
import os, datetime
from django.template.defaultfilters import slugify
from form.GDriveConnect import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage


class UploadedFile(models.Model):
	def location(self,title):
		title = title.rsplit(".",1)
		fileName = "%s.%s"%(slugify(title[0]),title[1])
		self.extention = ".%s"%title[1]
		return fileName
		return "location.pdf"
	
	theFile = models.FileField(upload_to="",blank=True)#location,blank=True)	
	extention = models.CharField(max_length=30,blank=True)

	def __unicode__(self):
		return "%s"%(str(self.theFile))
	

class Application(models.Model):
	slug = models.SlugField(blank=True)
	fileName = models.SlugField(blank=True)
	uploaded = models.DateTimeField(auto_now=True)

	fullName = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	phone = models.CharField(max_length=500)

	# statement = models.TextField(max_length=1000)

	cv =  models.ForeignKey(UploadedFile,related_name="cv")
	portrait = models.ForeignKey(UploadedFile,related_name="portrait")
	reference_1 = models.ForeignKey(UploadedFile,related_name="reference_1")
	reference_2 = models.ForeignKey(UploadedFile,related_name="reference_2")
	reference_3 = models.ForeignKey(UploadedFile,related_name="reference_3")
	letter_of_intent = models.ForeignKey(UploadedFile,related_name="letter_of_intent")

	def __unicode__(self):
		return "%s %s"%(self.fullName,self.uploaded)
	
	def save(self,*args, **kwargs):
		service = getService()
		slug = slugify(self.fullName)
		dateString = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")

		
		folder = createFolder(service, "%s-%s"%(slug, dateString))["id"]
		formData(service,slug,dateString,self,folder)
		upLoadToGD(service, self.cv, folder, "cv.pdf", "application/pdf")
		upLoadToGD(service, self.portrait, folder, "portrait.jpg", "image/jpeg")
		upLoadToGD(service, self.reference_1, folder, "reference1.pdf", "application/pdf")
		upLoadToGD(service, self.reference_2, folder, "reference2.pdf", "application/pdf")
		upLoadToGD(service, self.reference_3, folder, "reference3.pdf", "application/pdf")
		upLoadToGD(service, self.letter_of_intent, folder, "letter_of_intent.pdf", "application/pdf")


		title = "%s submitted"%self.fullName
		message = """
				Hello!
				%s has submitted their completed fellowship application. 
				View their application at: https://drive.google.com/drive/u/0/folders/%s
				OR 
				view all available applications at: https://drive.google.com/drive/u/0/folders/0BxArj8ptnN7AXzJ5WEdrZUZQLVU
				+ + + 
				For technical issues, please contact: collaborate@alsocollective.com
			"""%(self.fullName,folder)
		messageHTML = """
				Hello!<br><br> 
				%s has submitted their completed fellowship application.<br><br>
				View their application at: <a href='https://drive.google.com/drive/u/0/folders/%s'> https://drive.google.com/drive/u/0/folders/%s </a><br><br>
				OR<br><br>
				view all available applications at: <a href='https://drive.google.com/drive/u/0/folders/0BxArj8ptnN7AXzJ5WEdrZUZQLVU'> https://drive.google.com/drive/u/0/folders/0BxArj8ptnN7AXzJ5WEdrZUZQLVU </a><br><br>
				+ + + <br><br>
				For technical issues, please contact: <a href='mailto:collaborate@alsocollective.com'>collaborate@alsocollective.com</a><br><br>
			"""%(self.fullName,folder,folder)
		send_mail(title,message,"orthosickkids@gmail.com" ,[settings.SHARE_WITH_THIS_USER], fail_silently=False, html_message=messageHTML)
		
		super(Application, self).save(*args, **kwargs)









