'use strict';

var https = require('https');

const functions = require('firebase-functions');

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {

    var chat = "This is a sample response";

    response.setHeader('Content-Type', 'application/json');

    
    response.send(JSON.stringify({ "speech": chat, "displayText": chat }));

});