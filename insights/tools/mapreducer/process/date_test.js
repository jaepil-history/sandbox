/**
 * Created with PyCharm.
 * User: byouloh
 * Date: 13. 5. 7
 * Time: 오후 6:19
 * To change this template use File | Settings | File Templates.
 */

var birth = '2011/03/31';
var today = new Date();

console.log(today);
console.log(today.getFullYear());
console.log(birth.split('/', 1));

var age = today.getFullYear() - birth.split('/', 1);
console.log(age);