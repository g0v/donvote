// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('donvote');
x$.controller('karma', function($scope, $http, stateIndicator){
  $scope.newKarma = function(){
    var url;
    url = typeof ownerapi != 'undefined' && ownerapi !== null ? ownerapi : '/api/discuss/';
    url = '/api/discuss/3/karma/';
    console.log(url);
    $scope.state.loading();
    return $http({
      url: url,
      method: 'POST',
      data: JSON.stringify($scope.data)
    }).success(function(d){
      return $scope.state.done();
    }).error(function(e){
      console.error(e);
      return $scope.state.fail();
    });
  };
  $scope.state = stateIndicator.init();
  $scope.tend = function(it){
    return $scope.data.value = it;
  };
  $scope.reset = function(){
    return $scope.data = {
      value: 2
    };
  };
  return $scope.reset();
});