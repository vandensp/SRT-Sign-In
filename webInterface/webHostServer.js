var http = require("http");    //#A
var fs = require('fs');
var index
var port = 1444;

// anonymous function - function which handles requests to server
// request - incoming request message
// response - response message to be sent to client
http.createServer(function(request,response){    //#B
    var x;
    var headers = request.headers;
    var trailers = request.trailers;
    var url = request.url;
    var argurl = url.toString().split('?')[1]
    var params = argurl.split('&');
    var args = {};
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
    argurl = argurl.substring(argurl.indexOf('&') + 1);
    console.log('arg url: ');
    console.log(argurl);
    console.log('Params: ');
    // separate out parameters from url
    for (x in params) {
        var y = params[x].split('=');
        if (y[0] === 'path') {
            path = y[1].replace('%2F', '/');
            console.log('\t{' + y[0] + ': \"' + path + '\"}');
        }
        else {
            args[y[0]] = y[1];
            console.log('\t{' + y[0] + ': \"' + args[y[0]] + '\"}');
        }
    }
    if (argurl === 'client'){
        index= fs.readFileSync('signInClient.html')
    }
    else if (argurl === 'srt'){
        index = fs.readFileSync('signInSRT.html')
    }
    else{
        index= fs.readFileSync('signInClient.html')
    }
    response.writeHead(200,    //#C
          {'Content-Type': 'text/html',    //#D
           'Access-Control-Allow-Origin': '*'});    //#E
    //getSRTs();
   
    response.end(index);    //#G
    console.log('Response sent to client\n');
  
  }).listen(port,'');    //#H
  console.log('Server listening on http://localhost:' + port);