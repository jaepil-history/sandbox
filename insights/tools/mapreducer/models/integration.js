/*
 * cpu
 */
//    s: The UID of the user.
//    b: The year of the user's birth, in YYYY/MM/DD format.
//    g: The gender of the user. Accepted parameter values are: m (Male), f (Female),
//        and u (Unknown, if no gender is specified).
//    lc: The country code of the country in which the user is located. The country code must be in
//        upper case format and conform to the ISO 3166-1 alpha-2 standard. If not sent, it will be
//        based on the parameter included in the pgr message.
//    f: The number of friends a user has.
//    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
//        It must be base64-encoded.
//    ts: The timestamp in the Epoch time format.
//        Include this parameter to prevent the user's browser from caching the REST API call if sent
//        using JavaScript.
//    """
//
//    user_uid = LongType(minimized_field_name="uuid", required=True)
//    birthday = StringType(minimized_field_name="b", min_length=10, max_length=10)
//    gender = StringType(minimized_field_name="g", min_length=1, max_length=1)
//    country = StringType(minimized_field_name="lc")
//    friends_count = IntType(minimized_field_name="f")
//    data = StringType()
//    timestamp = IntType(minimized_field_name="ts")

/*
 * apa
 */
//    s: The UID of the user adding the application.
//    u: A 16-digit unique hexadecimal string to track an invite, notification email, or stream post;
//        generated if the user installed the application as a result of clicking on an invite,
//        notification, email, or post. Valid characters are a-f, A-F, 0-9. This parameter must match
//        the u parameter in the associated ins/inr, pst/psr, or nes/nei API calls that the install
//        originated from.
//    su: An 8-digit unique hexadecimal string. If a click is from an advertisement, link, or partner
//        site, use this parameter instead of the u parameter. Valid characters are a-f, A-F, 0-9.
//        This parameter must match the su parameter in the associated ucc API call.
//    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
//        It must be base64-encoded.
//    ts: The timestamp in the Epoch time format.
//        Include this parameter to prevent the user's browser from caching the REST API call if sent
//        using JavaScript.
//    """
//
//    user_uid = LongType(minimized_field_name="uuid", required=True)
//    tracking_uid = StringType(minimized_field_name="tuid",
//                              regex="[0-9A-Fa-f]+", min_length=8, max_length=16)
//    data = StringType()
//    timestamp = IntType(minimized_field_name="ts")

/*
 * pgr
 */
//    s: The UID of the user.
//    u: The page address to be recorded can be set manually using this parameter. If this message is
//        posted to the server directly from the end user's browser, it is not necessary to set this
//        parameter, as the page address can be derived from the information in the HTTP header.
//        The value of this parameter, if present, should be URL-encoded.
//    ip: The IP address of the user requesting the page. If this message is sent to the Appspand API
//        server directly from your server, you must set this parameter.
//    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
//        It must be base64-encoded.
//    ts: The timestamp in the Epoch time format.
//        Include this parameter to prevent the user's browser from caching the REST API call if sent
//        using JavaScript.
//    """
//
//    user_uid = LongType(minimized_field_name="uuid", required=True)
//    url = StringType(minimized_field_name="url", min_length=1, max_length=128)
//    ip = StringType(min_length=1, max_length=32)
//    data = StringType()
//    timestamp = IntType(minimized_field_name="ts", required=True)

var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var Integration = new Schema({
    _mt: String,
    _dt: Date,
    user_uid: Number,
    birthday: String,
    gender: String,
    country: String,
    friends_count: Number,
    data: String,
    timestamp: Number,
    age: { type: Number, min: 8, max: 75 },
    tracking_uid: String,
    url: String,
    ip: String
}, {collection: 'integration'}); // 마지막은 collection name. 없으면 model_name = collection_name

// mapping UserInfo model to userSchema
var Integration = mongoose.model('Integration', Integration);

//Integration.index({ timestamp: -1 });
//Integration.plugin(require('mongoose-lifecycle'));

// db 연결
var test_db = mongoose.createConnection('mongodb://localhost:27017/test');
var appspand_db = mongoose.createConnection('mongodb://localhost:27017/appspand');

test_db.on('open', function() {
    console.log("test db connected...");
});

appspand_db.on('open', function() {
    console.log("appspand db connected...");
});

console.log(test_db.model('resultjs').find());
console.log(appspand_db.collections);


//module.exports = mongoose.model('Integration', Integration);
