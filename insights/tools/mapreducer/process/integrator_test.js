<<<<<<< HEAD
var async = require('async');
var Integrator = require('./integrator');
var analyzer   = require('../lib/analyzer');

var a = analyzer.createAnalyzer({joinInterval: 600000});
a.start();


//var apps;
//
//async.waterfall([
//    function(callback) {
//        Integrator.getAppsList(db_appspand, application_collection);
//        console.log('which? ' + apps);
//        console.log('processed?');
//        //callback(null, apps);
//    },
//    function(apps, callback) {
//        console.log('apps length : ' + apps.length);
//        var cluster_name;
//        var db_name;
//        var appId;
//        console.log('who? ' + apps);
//        for (var i in apps) {
//            console.log(apps[i]);
//            cluster_name = apps[i].cluster.name;
//            console.log(cluster_name);
//            db_name = apps[i].cluster.db_name;
//            console.log(db_name);
//            appId = apps[i]._id.toString();
//            console.log(appId);
//            Integrator.joinAllandCPU(cluster_name, db_name, appId, callback);
//            //callback(null, '2');
//        }
//    }
//],
//// optional callback
//function(err, results) {
//    // results is ...
//});

//// an example using an object instead of an array
//async.series({
//    one: function(callback) {
//        setTimeout(function() {
//            console.log('1');
//            callback(null, 1);
//        }, 200);
//    },
//    two: function(callback) {
//        setTimeout(function() {
//            console.log('2');
//            callback(null, 2);
//        }, 100);
//    }
//},
//function(err, results) {
//    // results is now equal to: {one: 1, two: 2}
=======
var async = require('async');
var Integrator = require('./integrator');
var analyzer   = require('../lib/analyzer');

var a = analyzer.createAnalyzer({joinInterval: 600000});
a.start();


//var apps;
//
//async.waterfall([
//    function(callback) {
//        Integrator.getAppsList(db_appspand, application_collection);
//        console.log('which? ' + apps);
//        console.log('processed?');
//        //callback(null, apps);
//    },
//    function(apps, callback) {
//        console.log('apps length : ' + apps.length);
//        var cluster_name;
//        var db_name;
//        var appId;
//        console.log('who? ' + apps);
//        for (var i in apps) {
//            console.log(apps[i]);
//            cluster_name = apps[i].cluster.name;
//            console.log(cluster_name);
//            db_name = apps[i].cluster.db_name;
//            console.log(db_name);
//            appId = apps[i]._id.toString();
//            console.log(appId);
//            Integrator.joinAllandCPU(cluster_name, db_name, appId, callback);
//            //callback(null, '2');
//        }
//    }
//],
//// optional callback
//function(err, results) {
//    // results is ...
//});

//// an example using an object instead of an array
//async.series({
//    one: function(callback) {
//        setTimeout(function() {
//            console.log('1');
//            callback(null, 1);
//        }, 200);
//    },
//    two: function(callback) {
//        setTimeout(function() {
//            console.log('2');
//            callback(null, 2);
//        }, 100);
//    }
//},
//function(err, results) {
//    // results is now equal to: {one: 1, two: 2}
>>>>>>> e1fa4f7d9c8eb0592f3156be59486cb533826530
//});