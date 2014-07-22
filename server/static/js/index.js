// Generated by LiveScript 1.2.0
var err, ok, x$;
err = function(it){
  return console.error("[ERROR]", it);
};
ok = function(it){
  return console.log("[OK]", it);
};
x$ = angular.module('donvote', ['ui.choices', 'ui.bootstrap.datetimepicker']);
x$.config(function($httpProvider){
  return $httpProvider.defaults.headers.common["X-CSRFToken"] = $.cookie('csrftoken');
});
x$.controller('main', function($scope, $http){
  console.log('ok');
  $scope.user = {};
  $scope.save = function(){
    console.log('saving');
    return $http({
      url: "/user/" + $scope.id,
      method: 'PUT',
      data: {
        group: $scope.user.group
      }
    }).success(ok).error(err);
  };
  $scope.init = function(){
    if (!$scope.id) {
      return;
    }
    return $http({
      url: "/user/" + $scope.id + "/",
      method: 'GET'
    }).success(function(d){
      console.log("user loaded: ", d);
      return $scope.user = d;
    }).error(err);
  };
  $scope.group = {
    list: [],
    dict: {},
    selected: 0,
    init: function(){
      var this$ = this;
      return $http({
        url: '/group/',
        method: 'GET'
      }).success(function(d){
        $scope.group.list = d;
        return d.map(function(it){
          return this$.dict[it.id] = it;
        });
      });
    },
    remove: function(id){
      console.log("removing " + id);
      $scope.user.group = $scope.user.group.filter(function(it){
        return it !== id;
      });
      return $scope.save();
    },
    'new': function(){
      var this$ = this;
      console.log('ok', $scope.groupform.name.$invalid);
      if ($scope.groupform.name.$invalid) {
        return;
      }
      return $http({
        url: '/group/',
        method: 'POST',
        data: {
          name: $scope.group.name,
          desc: $scope.group.desc
        }
      }).success(function(it){
        this$.list.push(it);
        return this$.dict[it.id] = it;
      }).error(err);
    },
    add: function(){
      var id;
      id = (this.selected || {}).id;
      console.log($scope.user.group, id);
      if (!id || in$(id, $scope.user.group)) {
        return;
      }
      console.log(id);
      $scope.user.group.push(id);
      $scope.save();
      return this.selected = 0;
    }
  };
  $scope.group.init();
  return $scope.$watch('id', function(){
    return $scope.init();
  });
});
function in$(x, xs){
  var i = -1, l = xs.length >>> 0;
  while (++i < l) if (x === xs[i]) return true;
  return false;
}