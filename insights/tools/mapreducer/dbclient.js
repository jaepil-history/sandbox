var mongoose   = require('mongoose');
var semver     = require('semver');

// config
var config     = require('./config/config');

// configure mongodb
mongoose.connect(config.mongodb.connectionString || 'mongodb://' + config.mongodb.user + ':' + config.mongodb.password
                             + '@' + config.mongodb.server + ':' + String(config.mongodb.port) + '/' + config.mongodb.database);

var db = mongoose.connection;

db.on('error', function (err) {
  console.error('MongoDB error: ' + err.message);
  console.error('Make sure a mongoDB api is running and accessible by this application');
  process.exit(1);
});

db.on('open', function (err) {
  db.db.admin().serverStatus(function(err, data) {
    if (err) {
      if (err.name === "MongoError" && (err.errmsg === 'need to login' || err.errmsg === 'unauthorized')) {
        console.log('Forcing MongoDB authentication');
        db.db.authenticate(config.mongodb.user, config.mongodb.password, function(err) {
          if (!err) return;
          console.error(err);
          process.exit(1);
        });
        return;
      } else {
        console.error(err);
        process.exit(1);
      }
    }
    if (!semver.satisfies(data.version, '>=2.1.0')) {
      console.error('Error: datapro requires MongoDB v2.1 minimum. The current MongoDB api uses only '+ data.version);
      process.exit(1);
    }
  });
});


module.exports = mongoose;
