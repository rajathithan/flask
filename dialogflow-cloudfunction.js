'use strict';
 
var https = require ('https');
const functions = require('firebase-functions');
const DialogFlowApp = require('actions-on-google').DialogFlowApp;

console.log('set me');
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  console.log('Inside Main function');
  console.log('Request Headers: ' + JSON.stringify(request.headers));
  console.log('Request Body: ' + JSON.stringify(request.body));
  
  let action = request.body.queryResult.action;
  //const agent = new WebhookClient({ request, response });
  var chat = "This is a sample response";
  console.log(action);
  response.setHeader('Content-Type','application/json');
  
    if ((action!= 'input.getOrderNo') && (action!= 'input.getGiftcardBalance')){
        console.log('Unknown input...exiting');
        response.send(buildChatResponse("I'm sorry, I don't know this"));
        return;
    }

    const parameters = request.body.queryResult.parameters;

    if (action== 'input.getOrderNo'){
        console.log('Successfully entered getOrderNo');
        var orderNo = parameters.number;
        getOrderNo (orderNo, response);    
    }

    if (action== 'input.getGiftcardBalance'){
        console.log('Successfully entered getGiftcardBalance');
        var gcNo = parameters.number;
        getGiftcardBalance (gcNo, response);
    }

});

function getOrderNo (orderNo, CloudFnResponse) {

	console.log('In Function Get Stock Price');

	console.log("orderNo: " + orderNo);
	
	
	var pathString = '/retail-order-status/' + orderNo;

	console.log ('path string:' + pathString);

	var request = https.get({
		host: "rajathithanrajasekar-eval-prod.apigee.net",
		path: pathString
		}, function (response) {
		var json = "";
		response.on('data', function(chunk) {
			console.log("Received JSON response: " + chunk);
			json += chunk;

			
		});

		response.on('end', function(){
			var jsonData = JSON.parse(json);
          
		           
			var orderStatus = jsonData.status;

			console.log ("The order status for order number -"+ orderNo +" is:" + orderStatus);

			var chat = "your order number " + orderNo + " is currently in " + orderStatus + " status";

			CloudFnResponse.send(buildChatResponse(chat));

		});

});

}

function getGiftcardBalance (gcNo, CloudFnResponse) {

	console.log('In Function Get Giftcard Balance');

	console.log("Giftcard No: " + gcNo);
	
	
	var pathString = '/retailclient-giftcards-balance/' + gcNo;

	console.log ('path string:' + pathString);

	var request = https.get({
		host: "rajathithanrajasekar-eval-prod.apigee.net",
		path: pathString
		}, function (response) {
		var json = "";
		response.on('data', function(chunk) {
			console.log("Received JSON response: " + chunk);
			json += chunk;

			
		});

		response.on('end', function(){
			var jsonData = JSON.parse(json);
          
		           
			var gcBalance = jsonData.amount;

			console.log ("The balance amount on gift card no. -"+ gcNo +" is:" + gcBalance);

			var chat = "your balance amount on gift card number " + gcNo + " is " + gcBalance + " dollars";

			CloudFnResponse.send(buildChatResponse(chat));

		});

});

}

function buildChatResponse(chat) {
	return JSON.stringify({"fulfillmentText": chat});
}