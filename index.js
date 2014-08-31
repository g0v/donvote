// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('main', ['firebase']);
x$.controller('main', ['$scope', '$firebase', 'render'].concat(function($scope, $firebase, render){
  var prepareMetix, prepareDraw, resize;
  import$($scope, {
    user: null,
    mlogin: {
      email: "",
      password: "",
      error: {}
    }
  });
  $scope.auth = new FirebaseSimpleLogin(new Firebase("https://donmockup.firebaseio.com/"), function(e, u){
    return $scope.$apply(function(){
      console.log("user login:", u);
      if (e) {
        return console.log("get user fail: ", e);
      }
      return $scope.user = u;
    });
  });
  $scope.logout = function(){
    if ($scope.user) {
      $scope.auth.logout();
      return $scope.email = "", $scope.password = "", $scope.user = null, $scope;
    }
  };
  $scope.login = function(){
    if (!$scope.user) {
      return $scope.auth.createUser($scope.mlogin.email, $scope.mlogin.password, function(e, u){
        if (e && e.code === 'EMAIL_TAKEN') {
          return $scope.auth.login('password', {
            email: $scope.mlogin.email,
            password: $scope.mlogin.password
          });
        } else if (e) {
          return console.log("create user error: ", e);
        } else {
          return $scope.$apply(function(){
            return $scope.user = u;
          });
        }
      });
    }
  };
  $scope.mvote = {
    id: null,
    obj: null,
    data: null,
    allballot: {},
    plans: [],
    ballot: [],
    planCount: function(plan){
      return this.allballot[plan.id] || 0;
    },
    planById: function(id){
      var ret;
      ret = this.plans.filter(function(it){
        return it.id === id;
      });
      if (ret.length) {
        return ret[0].name;
      }
    },
    setReadOnly: function(v){
      return this.readonly = v;
    },
    toggle: function(plan){
      var planid, ret, this$ = this;
      if (!this.id || this.readonly) {
        return;
      }
      if (!$scope.user) {
        return;
      }
      planid = this.plans.map(function(it){
        return it.id;
      });
      this.metix.forEach(function(it){
        if (!in$(it.$value, planid)) {
          return this$.metix.$remove(it);
        }
      });
      ret = this.metix.filter(function(it){
        return it.$value === plan.id;
      });
      if (ret.length > 0) {
        return ret.map(function(it){
          return this$.metix.$remove(it);
        });
      } else if (this.metix.length < (this.obj.maxvote || 1)) {
        return this.metix.$add(plan.id);
      }
    },
    add: function(){
      var db, payload, ref$;
      db = $firebase(new Firebase("https://donmockup.firebaseio.com/vote"));
      payload = (ref$ = {}, ref$.name = this.name, ref$.desc = this.desc, ref$.maxvote = this.maxvote, ref$.plans = this.plans, ref$.readonly = this.readonly, ref$);
      return db.$add(payload);
    },
    load: function(id){
      var obj, alltix, this$ = this;
      this.id = id;
      obj = $firebase(new Firebase("https://donmockup.firebaseio.com/vote/" + id)).$asObject();
      obj.$loaded().then(function(){
        var ref$;
        this$.obj = obj;
        return this$.name = (ref$ = this$.obj).name, this$.desc = ref$.desc, this$.maxvote = ref$.maxvote, this$.plans = ref$.plans, this$.readonly = ref$.readonly, this$;
      });
      alltix = $firebase(new Firebase("https://donmockup.firebaseio.com/vote/" + id + "/tix")).$asObject();
      return alltix.$loaded().then(function(){
        var update;
        this$.alltix = alltix;
        update = function(){
          this$.allballot = {};
          return this$.alltix.forEach(function(ballot){
            var k, v, results$ = [];
            for (k in ballot) {
              v = ballot[k];
              if (!this$.allballot[v]) {
                this$.allballot[v] = 0;
              }
              results$.push(this$.allballot[v]++);
            }
            return results$;
          });
        };
        update();
        return this$.alltix.$watch(update);
      });
    },
    save: function(){
      var ref$;
      $('#vote-modal').modal('hide');
      if (this.obj) {
        ref$ = this.obj;
        ref$.name = this.name;
        ref$.desc = this.desc;
        ref$.maxvote = this.maxvote;
        ref$.plans = this.plans;
        ref$.readonly = this.readonly;
        return this.obj.$save();
      }
      if (!this.name) {
        return;
      }
      if (!this.obj) {
        return this.add();
      }
    },
    delplan: function(plan){
      return this.plans.splice(this.plans.indexOf(plan), 1);
    },
    newplan: function(){
      return this.plans.push({
        name: this.newplanname,
        id: new Date().getTime()
      });
    }
  };
  $scope.mvote.load('-JVeaoPJwNWyZH9I8VRT');
  prepareMetix = function(){
    var metix;
    if (!($scope.mvote.id && $scope.user && $scope.user.uid)) {
      return;
    }
    metix = $firebase(new Firebase("https://donmockup.firebaseio.com/vote/" + $scope.mvote.id + "/tix/" + $scope.user.uid)).$asArray();
    return metix.$loaded().then(function(){
      var update;
      $scope.mvote.metix = metix;
      update = function(){
        return $scope.mvote.ballot = $scope.mvote.metix.map(function(it){
          return it.$value;
        });
      };
      update();
      return $scope.mvote.metix.$watch(update);
    });
  };
  $scope.svg = document.getElementById('svg');
  $scope.$watch('user', function(){
    return prepareMetix();
  });
  $scope.$watch('mvote.id', function(){
    return prepareMetix();
  });
  prepareDraw = function(){
    var payload;
    console.log($scope.mvote.plans);
    payload = $scope.mvote.plans.map(function(it){
      var ref$;
      return ref$ = {
        value: $scope.mvote.allballot[it.id] || 0
      }, ref$.name = it.name, ref$.id = it.id, ref$;
    });
    return render.draw(payload, $scope.svg);
  };
  $scope.$watch('mvote.allballot', prepareDraw, true);
  $scope.$watch('mvote.plans', prepareDraw, true);
  resize = function(){
    var ref$, h, w;
    ref$ = [$(window).height(), $(window).width()], h = ref$[0], w = ref$[1];
    $(svg).width(w - 40);
    return $(svg).height(h - 200);
  };
  $(window).resize(resize);
  return resize();
}));
function import$(obj, src){
  var own = {}.hasOwnProperty;
  for (var key in src) if (own.call(src, key)) obj[key] = src[key];
  return obj;
}
function in$(x, xs){
  var i = -1, l = xs.length >>> 0;
  while (++i < l) if (x === xs[i]) return true;
  return false;
}