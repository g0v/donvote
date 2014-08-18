// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('donvote');
x$.controller('discuss', function($scope, $http, stateIndicator){
  $scope.newDiscuss = function(){
    var url;
    url = typeof ownerapi != 'undefined' && ownerapi !== null ? ownerapi : '/api/discuss/';
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
    return $scope.data.tendency = it;
  };
  $scope.reset = function(){
    return $scope.data = {
      tendency: 2
    };
  };
  return $scope.reset();
});