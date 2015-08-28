from django.forms import ModelForm
from django import forms
from form.models import *


class ExtFileField(forms.FileField):
	def __init__(self, *args, **kwargs):
		ext_whitelist = kwargs.pop("ext_whitelist")
		self.ext_whitelist = [i.lower() for i in ext_whitelist]

		super(ExtFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		print self
		data = super(ExtFileField, self).clean(*args, **kwargs)
		if data:
			filename = data.name
			# print self
			ext = os.path.splitext(filename)
			ext = ext[1]
			ext = ext.lower()
			if ext not in self.ext_whitelist:
				raise forms.ValidationError("Filetype '%s' is not allowed for this field." % ext)
			elif (data._size > settings.MAX_UPLOAD_SIZE):
				raise forms.ValidationError("File is too large %s"%data._size)

		elif not data and self.required:
			raise forms.ValidationError("Required file not found for %s" % self.label)
		return data
		
class UploadForm(ModelForm):
	def __init__(self, *args, **kwargs):		
		self.base_fields['theFile']=ExtFileField(ext_whitelist=(".pdf",".jpg",".jpeg",))
		super(UploadForm, self).__init__(*args, **kwargs)

	class Meta:
		model = UploadedFile
		fields = ['theFile',]


class ApplicationForm(ModelForm):
	class Meta:
		model = Application
		fields = ['fellowship','fullName','email','phone',"cv","portrait","reference_1","reference_2","reference_3","letter_of_intent"]

# class ApplicationForm(ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(ApplicationForm, self).__init__(*args, **kwargs)

# 	class Meta:
# 		model = Application
# 		fields = ['fullName','email','phone','statement',"cv","portrait","reference_1","reference_2","reference_3"]



