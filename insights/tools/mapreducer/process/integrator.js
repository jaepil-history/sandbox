/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 11
 * Time: 오후 9:11
 * To change this template use File | Settings | File Templates.
 */

var mongoose = require('mongoose');

// db 연결
mongoose.connect('mongodb://localhost/appspand');
var db = mongoose.connection;
console.log('Connected to DB appspand');


