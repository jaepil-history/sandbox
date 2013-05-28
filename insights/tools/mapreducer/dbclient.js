var db_appspand_url = 'localhost:27017/appspand';  // "username:password@example.com/mydb"
var application_collection = 'application';
var account_collection = 'account';
var collections_appspand = [application_collection, account_collection];
exports.db_appspand = require('mongojs').connect(db_appspand_url, collections_appspand);

var db_insight_url = 'localhost:27017/test';
//var cpu_collection = '.event.cpu';
//var all_collection = '.event.all';
//var collections_insight = [cpu_collection, all_collection];
exports.db_insight = require("mongojs").connect(db_insight_url);//, collections_insight);

var db_processed_url = 'localhost:27017/processed';
//var integration_collection = '.integration';
//var collections_processed = [integration_collection];
exports.db_processed = require('mongojs').connect(db_processed_url);//, collections_processed);

//exports.dbclient = function() {
//    var dblist = [db_appspand, db_insight, db_processed];
//    return dblist
//};

//var mongoose   = require('mongoose');
//var semver     = require('semver');
//
//// config
//var config     = require('./config/config');
//
//// configure mongodb
//mongoose.connect(config.mongodb.connectionString || 'mongodb://' + config.mongodb.user + ':' + config.mongodb.password
//                             + '@' + config.mongodb.server + ':' + String(config.mongodb.port) + '/' + config.mongodb.database);
//
//var db = mongoose.connection;
//
//db.on('error', function (err) {
//  console.error('MongoDB error: ' + err.message);
//  console.error('Make sure a mongoDB api is running and accessible by this application');
//  process.exit(1);
//});
//
//db.on('open', function (err) {
//  db.db.admin().serverStatus(function(err, data) {
//    if (err) {
//      if (err.name === "MongoError" && (err.errmsg === 'need to login' || err.errmsg === 'unauthorized')) {
//        console.log('Forcing MongoDB authentication');
//        db.db.authenticate(config.mongodb.user, config.mongodb.password, function(err) {
//          if (!err) return;
//          console.error(err);
//          process.exit(1);
//        });
//        return;
//      } else {
//        console.error(err);
//        process.exit(1);
//      }
//    }
//    if (!semver.satisfies(data.version, '>=2.1.0')) {
//      console.error('Error: datapro requires MongoDB v2.1 minimum. The current MongoDB api uses only '+ data.version);
//      process.exit(1);
//    }
//  });
//});
//
//
//module.exports = mongoose;
