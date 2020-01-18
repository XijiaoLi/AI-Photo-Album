$(document).ready(function() {
	// $("#TextSearchLayer").hide()
	$("#VoiceSearchLayer").hide()
	$("#UploadPhotoLayer").hide()
	$("#SearchReaultsLayer").hide()
	// $("#ThreeChoicesLayer").hide()


	// $("#TextSearchChoice").click(function() {
	// 	$("#ThreeChoicesLayer").hide()
	// 	$("#TextSearchLayer").show()
	// });

	$("#VoiceSearchChoice").click(function() {
		$("#ThreeChoicesLayer").hide()
		$("#VoiceSearchLayer").show()
	});

	$("#UploadPhotoChoice").click(function() {
		$("#ThreeChoicesLayer").hide()
		$("#UploadPhotoLayer").show()
	});


	$(".back_btn").click(function() {
		$(".choice").hide()
		$("#ThreeChoicesLayer").show()
	});

	var apigClient = apigClientFactory.newClient({
		apiKey: "sGPigkX5DJ8fHy6wlba10aqufVAQYoje9yBMdK6b"
	});

	$(".submit_key_btn").click(function() {
		var params = {
			"query": $('#q').val()
		};
		var additionalParams = {
			queryParams: {
			      query: $('#q').val()
			}
		};
		var body = {
			"query": $('#q').val()
		};

		$("#VoiceSearchLayer").hide()
		$("#SearchReaultsLayer").show()
		console.log(body)

		apigClient.searchGet(params, body, additionalParams).then(function (result) {

			console.log(result)
			var response_body = result.data;
			var results = response_body.results;
			console.log(results)
			$("ul").empty();
			results.forEach(function(result) {
				console.log(result)

				var img = "<li><img src=\"" + result.url + "\" width=\"1000\"></li>";
				$("ul").append(img);
			});
	
		}).catch(function (result) {

		});
	});


	$("#fileupload").change(function(){
	  	var file = $("#fileupload").prop('files')[0];
	  	console.log(file.size);
	  	console.log(file.type);
		// reader = new FileReader();
		// reader.onload = function(e) {
		// 	base64 = reader.result;
		// }
		// reader.readAsDataURL(file);
		// reader.readAsArrayBuffer(file);
 	});

	 // upload photo
	$("#submit_photo_btn").click(function() {
		var file = $("#fileupload").prop('files')[0];
	  	console.log(file.size);
	  	console.log(file.type);
		var xhr = new XMLHttpRequest(); 
		xhr.open("PUT", "https://bc0hpvs7zg.execute-api.us-east-1.amazonaws.com/beta/hw3-photos-upload/" + file.name);
		xhr.setRequestHeader("Content-Type", file.type);
		xhr.setRequestHeader("x-api-key", "sGPigkX5DJ8fHy6wlba10aqufVAQYoje9yBMdK6b");
		xhr.onload = function (event) { 
			alert("Congratulations! You have successfully uploaded your photo!");
		};
		xhr.send(file);

		// var s3 = new AWS.S3();
		// var params = {
		// 	Bucket: 'hw3-photos-upload',
		// 	Key: file.name,
		// 	ContentType: file.type,
		// 	Body: file,
		// 	ACL: 'public-read-write'
		// };
		// s3.putObject(params, function (err, res) {
		// 	if (err) {
		// 		console.log("Error uploading data: ", err);
		// 	} else {
		// 		console.log("Successfully uploaded data");
		// 		window.alert("Successfully uploaded image");
		// 	}
		// });

		// if (base64) {
		// 	console.log(base64);
		// 	var pos = base64.indexOf("base64,");
		// 	var base64Content = base64.substring(pos + 7);
		// 	var body = {
		// 		"file": base64Content
		// 	};
		// 	var params = {
		// 		"Content-Type": file.type,
		// 		"folder": 'hw3-photos-upload',
		// 		"item": file.name
		// 	};
		// 	//Call uploadPut to make a HTTP put request.
		// 	apigClient.folderItemPut(params, body).then(function(result){
		// 		//a success callback
		// 		console.log("put result -----------\n" + JSON.stringify(result));
		// 		alert("Congratulations! You have successfully uploaded your photo!");
		// 	}).catch( function(result){
		// 		//an error callback
		// 		alert("An error occurred, please try again!");
		// 		// showError(responseResult);
		// 		console.log("put request error ----------\n" + JSON.stringify(result));
		// 	});
		// } else {
		// 	alert("Sorry, please select a photo");
		// }
	});
});