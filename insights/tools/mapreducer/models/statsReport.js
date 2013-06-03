var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var StatsReport = new Schema({
    timestamp    : { type: Date, default: Date.now },
    processtime: Number,
    counts: { input: Number, emit: Number, reduce: Number, output: Number },
    timing: {
        mapTime: Number,
        emitLoop: Number,
        reduceTime: Number,
        mode: String,
        total: Number
    },
    tags        : [String],
    message     : String,
    details     : String
}, {collection: 'stats_reports'});
StatsReport.index({ timestamp: -1 });
StatsReport.plugin(require('mongoose-lifecycle'));

StatsReport.methods.findStats = function(callback) {
  return this.db.model('StatsReport').findById(this.check, callback);
};

StatsReport.statics.aggregateEventsByDay = function(events, callback) {
  // list checks concerned by all events
  var checkIds = [];
  events.forEach(function(event) {
    var check = event.check.toString();
    if (checkIds.indexOf(check) == -1) checkIds.push(check);
  });
  this.db.model('Stats').find({ _id: { $in: checkIds } }).select({ _id: 1, name: 1, url: 1 }).exec(function(err, checks) {
    // populate related check for each event
    if (err) return callback(err);
    var indexedChecks = {};
    checks.forEach(function(check) {
      indexedChecks[check._id] = check;
    });
    events.forEach(function(event, index) {
      event = event.toJSON(); // bypass mongoose's magic setters
      event.check = indexedChecks[event.check];
      delete event.__v;
      delete event._id;
      if (event.message == 'up') {
        delete event.details;
      }
      events[index] = event;
    });

    // aggregate events by day
    var currentDay;
    var aggregatedEvents = {};
    var currentAggregate = [];
    events.forEach(function(event) {
      var date = new Date(event.timestamp).toLocaleDateString();
      if (date != currentDay) {
        currentDay = date;
        currentAggregate = aggregatedEvents[date] = [];
      }
      currentAggregate.push(event);
    });
    callback(null, aggregatedEvents);
  });
};

StatsReport.statics.cleanup = function(maxAge, callback) {
  var oldestDateToKeep = new Date(Date.now() - (maxAge ||  3 * 31 * 24 * 60 * 60 * 1000));
  this.find({ timestamp: { $lt: oldestDateToKeep } }).remove(callback);
};

module.exports = mongoose.model('StatsReport', StatsReport);
