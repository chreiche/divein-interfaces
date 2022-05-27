var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

const basicAuth = require('express-basic-auth');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// TASK 1:
app.get('/lucky_number', (req, res) => {
  let value1 = Math.floor(Math.random() * 100);
  res.send('Your lucky number for the day is: ' + value1);
})

// TASK 2:
app.get('/greetings', (req, res, next) => {
  if(!req.query.name) {
    const err = new Error('Required query parameter name is missing');
    err.status = 400;
    next(err);
  }
  else{
    let name = req.query.name;
    res.send('Welcome ' + name);
  }
})

// TASK 3:
function isNumeric(str) {
  if (typeof str != "string") return false // we only process strings!  
  return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
         !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

app.get('/weekday_calculator', (req, res, next) => {
  if(!req.headers['n']) {
    const err = new Error('Required query parameter n is missing');
    err.status = 400;
    next(err);
  }
  else{
    var f;
    var n = parseInt(req.headers['n'])
    if(isNumeric(req.headers['n']) == false) {
      const err = new Error('Required query parameter n is invalid');
      err.status = 400;
      next(err);
    }
    var dict = {};
    dict[1] = "Monday";
    dict[2] = "Tuesday";
    dict[3] = "Wednesday";
    dict[4] = "Thursday";
    dict[5] = "Friday";
    dict[6] = "Saturday";
    dict[7] = "Sunday";
    var today = new Date();
    let p = today.getDay();
    if(p + n <= 7) {
      f = p + n;
    }
    else{
      f = p + n - 7;
    }
    res.send(n + ' days from now is a ' + dict[f]);
  }
})

//TASK 4:
function myAuthorizer(username, password) {
  const userMatches = basicAuth.safeCompare(username, 'DiveIn')
  const passwordMatches = basicAuth.safeCompare(password, '1234')
  return userMatches & passwordMatches
}

app.get('/login', (req, res) => {
  // check for basic auth header
  if (!req.headers.authorization) {
    return res.status(401).json({ message: 'Missing Authorization Header' });
  }
  else{
    // verify auth credentials
    const base64Credentials =  req.headers.authorization.split(' ')[1];
    const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii');
    const [username, password] = credentials.split(':');
    const user = myAuthorizer(username, password);
    if (!user) {
        return res.status(401).json({ message: 'Invalid Authentication Credentials' });
    }
    else{
      return res.send("Login successful!");
    }
  }
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

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
