// Example of simple server which displays info about incoming requests and sends simple response
var http = require("http");    //#A
var port = 1441;    // can use any port # you prefer (above 1024) - client must use same port #
var currentSRTs = ["Tori Robinson","Nathan Hurtig"];
var queue = [];
var occupancy = 0;
//var ip = '137.112.196.168';
var fs = require('fs')

// anonymous function - function which handles requests to server
// request - incoming request message
// response - response message to be sent to client
http.createServer(function(request,response){    //#B
  var x;
  var headers = request.headers;
  var trailers = request.trailers;
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
  logs=require('../logs/SRT_sample_queue.json')
  occupancy=Object.keys(logs).length;
  queue = [];
  for (student in logs) {
    if (!queue.includes(logs[student].name)){
      queue.push(logs[student].name);
    }
  }
  fs.watchFile(require.resolve('../logs/SRT_sample_queue.json'), function () {
    console.log("New Sign In, reloading...");
    delete require.cache[require.resolve('../logs/SRT_sample_queue.json')]
    logs=require('../logs/SRT_sample_queue.json')
    occupancy=Object.keys(logs).length;
    //queue = [];
    for (student in logs) {
      if (!queue.includes(logs[student].name)){
      queue.push(logs[student].name);
    }
  }
});

  response.writeHead(200,    //#C
        {'Content-Type': 'application/json',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
  response.write('{"currentSRTs" : "' + currentSRTs + '", "occupancy" : "' + occupancy +
  '", "queue" : "' + queue +'"}');    //#F
  response.end();    //#G
  console.log('Response sent to client\n');

}).listen(port);    //#H
console.log('Server listening on '+ "local" + ':' + port);

//#A Create an http object, which requires the http module 
//#B Create a server and define the function which will handle incoming requests
//#C Setting the status code to 200 (OK)
//#D Setting the header to announce we return JSON representations 
//#E Setting the header to allow origin '*' (all origins) for CORS support
//#F Write the JSON object to body of message
//#G Causes to return the response to the client
//#H Start server and begin accepting requests on port 