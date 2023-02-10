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

app.get('/users', function(req, res, next) {
  res.render('users', { newProfile: 'no', title: 'Express' });
});

app.get('/newprofile', function(req, res, next) {
  res.render('newprofile', { title: 'Express' });
});

app.get('/algorithm', function(req, res, next) {
  res.render('algorithm', {myVar: 'idk', title: 'Express' });
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

function sendProfile(nickname, username, password){

  var bucketName = 'added-new-person';
  var keyName = nickname + 'userprofile.json';

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
  // new Promise((resolve, reject) => {
  //   new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: 'idk-what-it-wants', Key: keyName}, function (err, data) {
  //       if (err) {
  //           reject(err);
  //       } else {
  //           console.log("Successfully dowloaded data from  bucket");
  //           var object = JSON.parse(data.Body.toString());
  //           console.log(object.nickname);
  //           resolve(data);
  //       }
  //   });
  // });
}


module.exports = app;
