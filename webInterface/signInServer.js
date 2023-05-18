// Example of simple server which displays info about incoming requests and sends simple response
var http = require("http");    //#A
var port = 1441;    // can use any port # you prefer (above 1024) - client must use same port #
var currentSRTs = ["Tori Robinson","Nathan Hurtig"];
var queue = [];
var occupancy = 0;
// var ip = '137.112.220.167';
var fs = require('fs')

// anonymous function - function which handles requests to server
// request - incoming request message
// response - response message to be sent to client
http.createServer(function(request,response){    //#B
  var x;
  var headers = request.headers;
  var trailers = request.trailers;
  var url = request.url;
  console.log('New incoming client request for ' + request.url);
  console.log('Request method: ' + request.method);
  console.log('Headers: ');
  for (x in headers) {
    console.log('\t{' + x + ': \"' + headers[x] + '\"}');
  }
  console.log('Trailers: ');
  for (x in trailers) {
    console.log('\t{' + x + ': \"' + trailers[x] + '\"}');
  }

  console.log('full url: ');
  console.log(url.toString());
  queue=require('../logs/SRT_sample_queue.json')
  response.writeHead(200,    //#C
        {'Content-Type': 'application/json',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
     //#F
  occupancy=Object.keys(queue).length;
    if (url === '/currentSRTs'){
      response.write('{"currentSRTs" : "' + currentSRTs +'"}'); 
    }
    else if (url === '/occupancy'){
      response.write('{""occupancy" : "' + occupancy +'"}'); 
    }
    else if (url === '/queue'){
      response.write(JSON.stringify(queue));  
    }
    else{
      response.write('{"currentSRTs" : "' + currentSRTs +'"}'); 
    }
  
  response.end();    //#G
  console.log('Response sent to client\n');

}).listen(port);    //#H
console.log('Server listening on localhost:' + port);

//#A Create an http object, which requires the http module 
//#B Create a server and define the function which will handle incoming requests
//#C Setting the status code to 200 (OK)
//#D Setting the header to announce we return JSON representations 
//#E Setting the header to allow origin '*' (all origins) for CORS support
//#F Write the JSON object to body of message
//#G Causes to return the response to the client
//#H Start server and begin accepting requests on port 