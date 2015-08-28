app = {
	init: function() {
		app.csrftoken = app.getCookie('csrftoken');
		app.toForm.init();
		app.liveFormCheck.init();
	},
	getCookie: function(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	},
	csrfSafeMethod: function(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	},
	toForm: {
		init: function() {
			$("#yes_na").click(app.toForm.yes)
			$("#no_na").click(app.toForm.no)
		},
		yes: function(event) {
			$("#first_selection").addClass("hidden");
			$("#study_in_canada").removeClass("hidden");
			app.submit.init();
		},
		no: function(event) {
			$("#first_selection").addClass("hidden");
			$("#no_study_in_canada").removeClass("hidden");
		}
	},
	submit: {
		fileNames: [
			"cv",
			"portrait",
			"reference_1",
			"reference_2",
			"reference_3",
			"letter_of_intent"
		],
		init: function() {
			$('#main-form').submit(app.submit.main.main);
			for (var i = app.submit.fileNames.length - 1; i >= 0; i--) {
				$("#theFile_" + app.submit.fileNames[i]).change(app.submit.submitNewFile.main);
			};
			$("#submit_everything").click(app.submit.makeItSo);
		},
		makeItSo: function() {
			$('#main-form').submit();
		},
		main: {
			main: function(event) {
				event.preventDefault();
				if (app.submit.main.testFrontEnd()) {
					return false;
				}

				$(this).ajaxSubmit({
					method: "post",
					beforeSend: app.submit.main.beforeSend,
					complete: app.submit.main.complete,
					error: app.submit.main.error
				});

				return false;
			},
			beforeSend: function(xhr, settings) {
				$("html").addClass("loading_form");
				if (!app.csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", app.csrftoken);
				}
			},
			error: function(jqXHR, textStatus, errorThrown, sent, ohter2) {
				$("html").removeClass("loading_form");
				var responce = $.parseJSON(jqXHR.responseText);
				app.submit.main.clearAllError();
				for (var key in responce) {
					if (responce.hasOwnProperty(key)) {
						app.submit.main.renderError(key, responce[key]);
					}
				}
				// $.each(responce, app.submit.main.renderError);
			},
			renderError: function(name, obj) {
				var target = $("#" + name + "-form")
				if (target.length) {
					target.addClass("error_onsend")
					target.find(".error_field").text(obj[0].message)
				}
			},
			complete: function(xhr, textStatus, sent) {
				$("html").removeClass("loading_form").addClass("loaded_form");
				$("#study_in_canada").html("");
			},
			clearAllError: function() {
				$(".error_field").each(function(i, val) {
					val.innerHTML = ""
					$(val.parentNode).removeClass("error_onsend");
				});
			},
			testFrontEnd: function() {
				app.submit.main.clearAllError();
				var fileNames = app.submit.fileNames.concat(['fullName',
						'email',
						'phone'
					]),
					error = false;
				for (var i = fileNames.length - 1; i >= 0; i--) {
					if (!$("#main-form #id_" + fileNames[i]).val()) {
						app.submit.main.renderError(fileNames[i], [{
							"message": "This field is required"
						}]);
						error = true;
					}
				}
				return error
			}

		},
		submitNewFile: {
			main: function(event) {
				var target = this.id.split("_");
				target.shift()
				target = target.join("_");
				$(this.parentNode).ajaxSubmit({
					target: target,
					method: "post",
					mimeType: "multipart/form-data",
					beforeSend: app.submit.submitNewFile.beforeSend,
					uploadProgress: app.submit.submitNewFile.uploadProgress,
					success: app.submit.submitNewFile.success,
					complete: app.submit.submitNewFile.complete,
					error: app.submit.submitNewFile.error
				});
			},
			beforeSend: function(xhr, settings) {
				console.log("0%");
				$("#" + this.target + "-form").addClass("file_loading");
				if (!app.csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", app.csrftoken);
				}
			},
			uploadProgress: function(event, position, total, percentComplete) {
				console.log(percentComplete + "%")
			},
			error: function(jqXHR, textStatus, errorThrown, sent, ohter2) {
				console.log(jqXHR)
				var responce = $.parseJSON(jqXHR.responseText);
				console.log(responce)
				// app.submit.main.clearAllError();
				var text = ""
				for (var key in responce) {
					if (responce.hasOwnProperty(key)) {
						text += responce[key][0].message
					}
				}
				$("#" + sent[0].id).removeClass("file_loading file_loaded").addClass("error_onsend");
				if (sent[0].id == "theFile_portrait") {
					text += " This field only accepts .jpg file type. Please submit a .jpg file type.";
				} else {
					text += " This field only accepts .pdf file type. Please submit a .pdf file type.";
				}
				$("#" + sent[0].id + " .error_field").html(text);
			},
			complete: function(xhr, textStatus, sent) {
				if (xhr.status == 400) {
					return false
				}
				var rootId = sent[0].id.split("-")[0]
				$("#id_" + rootId).val(xhr.responseText);
				var target = $("#" + sent[0].id);
				$(target).addClass("loading");
				target.removeClass("error_onsend file_loading").addClass("file_loaded");
				target.find(".error_field").html("");
				target.find(".pknumber").val(xhr.responseText);
			}
		}
	},
	liveFormCheck: {
		init: function() {

			var charLimit = 500;

			$("#id_statement").keyup(function() {
				console.log(this.value.length);
				$("#cnt").html(charLimit - this.value.length);

				if (this.value.length > charLimit) {
					$("#cnt").css("color", "#f00");
				};
			});
		}
	}

}