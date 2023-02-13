var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');
var app = express();
var AWS = require("aws-sdk");

AWS.config.getCredentials(function(err) {
  if (err) console.log(err.stack);
  // credentials not loaded
  else {
    console.log("Access key:", AWS.config.credentials.accessKeyId);
  }
});

var profileslist = [];

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended:true}));

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res, next) {
  res.render('homepage', { title: 'Express' });
});

app.get('/contact', function(req, res, next) {
  res.render('contact', { title: 'Express' });
});

app.get('/users', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  res.render('users', { algorithmlist: algorithmlist, newProfile: 'no', title: 'Express' });
});

app.get('/newprofile', function(req, res, next) {
  res.render('newprofile', { title: 'Express' });
});

app.get('/algorithm', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  res.render('algorithm', {algorithmlist: algorithmlist, title: 'Express' });
});

app.post('/newprofile', function(req, res, next) {
  sendProfile(req.body.nickname, req.body.username, req.body.password);
  res.render('users', {newProfile: 'yes', title: 'Express' });
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  console.log(err)
  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

function getProfListBucket(){
  var bucketNameProfList = 'profiles-list'
  var profilesListKeyName = 'profilenames.json'
  var listed = [];

  new Promise((resolve, reject) => {
    new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: bucketNameProfList, Key: profilesListKeyName}, function (err, data) {
        if (err) {

        } else {
            console.log("Successfully dowloaded data from bucket");
            var object = JSON.parse(data.Body.toString());
            var profiles = object.profiles;
            profiles.forEach(p=>{
              listed.push(p);
            })
        }
    });
  });
  return new Promise(resolve=>{
    setTimeout(()=>{
      resolve(listed);
    }, 2000);
  })
}

async function getProfiles(){
  var listtosend = [];

  var results = await getProfListBucket();

  results.forEach(key => {
    var newkey = key + 'userprofile.json'; 
    console.log(newkey);
    new Promise((resolve, reject) => {
      new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: 'added-new-person', Key: newkey}, function (err, data) {
          if (err) {
              reject(err);
          } else {
              console.log("Successfully dowloaded data from bucket");
              var object = JSON.parse(data.Body.toString());
              listtosend.push([object.nickname]);
              resolve(data);
          }
      });
    });
  });
  return new Promise(resolve=>{
    setTimeout(()=>{
      resolve(listtosend);
    }, 2000);
  })
}

function sendProfile(nickname, username, password){
  var bucketNameProfList = 'profiles-list'
  var profilesListKeyName = 'profilenames.json'
  var bucketName = 'added-new-person';
  var keyName = nickname + 'userprofile.json';
  var profilesAll = [];

  new Promise((resolve, reject) => {
    new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: bucketNameProfList, Key: profilesListKeyName}, function (err, data) {
        if (err) {

        } else {
            console.log("Successfully dowloaded data from bucket");
            var object = JSON.parse(data.Body.toString());
            var profiles = object.profiles;
            profiles.forEach(p=>{
              profilesAll.push(p);
            })
        }
    });
  });
  profilesAll.push(nickname);

  var bucketPromise = new AWS.S3({apiVersion: '2006-03-01'}).createBucket({Bucket: bucketName}).promise();
  bucketPromise.then(
    function(data) {
      var objectParams = {
        Bucket: bucketName, 
        Key: keyName, 
        Body: JSON.stringify({
          'nickname': nickname, 
          'username': username,
          'password': password
        })};
      var uploadPromise = new AWS.S3({apiVersion: '2006-03-01'}).putObject(objectParams).promise();
      uploadPromise.then(
        function(data) {
          console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
        });
  }).catch(
    function(err) {
      console.error(err, err.stack);
  });

  var bucketPromise = new AWS.S3({apiVersion: '2006-03-01'}).createBucket({Bucket: bucketNameProfList}).promise();
  bucketPromise.then(
    function(data) {
      var objectParams = {
        Bucket: bucketNameProfList, 
        Key: profilesListKeyName, 
        Body: JSON.stringify({
          'profiles': profilesAll
        })};
      var uploadPromise = new AWS.S3({apiVersion: '2006-03-01'}).putObject(objectParams).promise();
      uploadPromise.then(
        function(data) {
          console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
        });
  }).catch(
    function(err) {
      console.error(err, err.stack);
  });
}


module.exports = app;
