/**
 * Module dependencies.
 */

var http       = require('http');
var express    = require('express');
var socketIo   = require('socket.io');
var fs         = require('fs');
//var StatsReport = require('./models/statsReport');
//var dataProc   = require('./lib/dataProcessor');
var analyzer   = require('./lib/analyzer');
//var config     = require('config');

var app = module.exports = express();
var server = http.createServer(app);

// config
var config     = require('./config/config');

// database
var dbclient   = require('./dbclient');

// data processor
//var p;
//if (config.autoStartDataPro) {
//    p = dataProc.createDataProc(config.processor);
//    p.start();
//}

var a = analyzer.createAnalyzer({joinInterval: 600000});
a.start();

// Configuration
app.configure(function(){
    app.use(app.router);
    // the following middlewares are only necessary for the mounted 'datapro' api,
    // but express needs it on the parent api (?) and it therefore pollutes the api
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(express.cookieParser());
    app.use(express.session({ secret: 'qdfegsgkjhflkquhfskqdjfhskjdfh' }));
});

app.configure('development', function() {
    //if (config.verbose) dbclient.set('debug', true);
    app.use(express.static(__dirname + '/public'));
    app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

app.configure('production', function() {
    app.use(express.static(__dirname + '/public', { maxAge: oneYear }));
    app.use(express.errorHandler());
});

// Routes
app.get('/', function (req, res) {
    res.redirect('/index.html');
});


// Sockets
var io = socketIo.listen(server);

io.configure('production', function() {
    io.enable('browser client etag');
    io.set('log level', 1);
});

io.configure('development', function() {
    if (!config.verbose) io.set('log level', 1);
});

//StatsReport.on('afterInsert', function(event) {
//    io.sockets.emit('StatsReport', event.toJSON());
//});

io.sockets.on('connection', function(socket) {
    socket.on('set check', function(check) {
        socket.set('check', check);
    });
});

// start server
var port = process.env.PORT || config.server.port;
server.listen(port);
console.log("Express api listening on port %d in %s mode", port, app.settings.env);
