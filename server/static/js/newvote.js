// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('donvote');
x$.controller('newvote', function($scope, $timeout, $http){
  var quickTimeUpdate, quickPlanUpdate;
  $scope.plan = {
    name: "",
    desc: ""
  };
  $scope.vote = {
    name: "",
    desc: "",
    startCountDown: 3600000,
    duration: 86400000,
    endCountDown: 3600000,
    planCount: 2,
    qualifiedRate: 25,
    karmaRate: 10,
    karmaCount: 10,
    agreeRate: 20,
    answerRate: 80,
    voteRate: 75,
    maxChoiceCount: 2,
    rankMethod: 1,
    endByDuration: false,
    disclosedBallot: false,
    nullTicketRate: 40,
    validVoteRate: 66,
    obtainRate: 30
  };
  $scope.quick = {};
  $scope.custom = {
    time: false,
    plan: false,
    perm: false,
    adv: false,
    disclosedBallot: 0,
    endDateType: 1
  };
  $scope.$watch('custom.disclosedBallot', function(v){
    return $scope.vote.disclosedBallot = v ? true : false;
  });
  $scope.$watch('vote.disclosedBallot', function(v){
    return $scope.custom.disclosedBallot = v ? 1 : 0;
  });
  quickTimeUpdate = function(v){
    if (v) {
      if (v[1]) {
        return import$($scope.vote, {
          startDate: new Date().getTime(),
          startMethod: {
            2: true
          },
          endMethod: {
            1: true
          }
        });
      } else if (v[2]) {
        return import$($scope.vote, {
          startMethod: {
            1: true
          },
          endMethod: {
            1: true
          }
        });
      } else if (v[3]) {
        return import$($scope.vote, {
          startDate: new Date().getTime(),
          startMethod: {
            2: true
          },
          endMethod: {
            2: true
          },
          endByDuration: true,
          duration: [1, 0, 0]
        });
      }
    }
  };
  quickPlanUpdate = function(v){
    if (v) {
      if (v[1]) {
        $scope.vote.voteMethod = {
          1: true
        };
        return $scope.vote.plan = [
          {
            name: '贊同'
          }, {
            name: '反對'
          }
        ];
      } else if (v[2]) {
        $scope.vote.plan = [
          {
            name: '贊同'
          }, {
            name: '反對'
          }, {
            name: '無感'
          }
        ];
        return $scope.vote.voteMethod = {
          1: true
        };
      } else {
        return $scope.vote.voteMethod = {
          4: true
        };
      }
    }
  };
  $scope.$watch('quick.time', quickTimeUpdate);
  $scope.$watch('custom.time', function(it){
    if (!it) {
      return quickTimeUpdate($scope.quick.time);
    }
  });
  $scope.$watch('quick.plan', quickPlanUpdate);
  $scope.$watch('custom.plan', function(it){
    if (!it) {
      return quickPlanUpdate($scope.quick.plan);
    }
  });
  $scope.newplan = function(p){
    var ref$;
    if (p.name) {
      return $scope.vote.plan.push((ref$ = {}, ref$.name = p.name, ref$.desc = p.desc, ref$));
    }
  };
  $scope.removeplan = function(p){
    return $scope.vote.plan = $scope.vote.plan.filter(function(it){
      return it.name !== p.name;
    });
  };
  $scope.newvote = function(v){
    return console.log(v);
  };
  return $timeout(function(){
    return $http({
      url: '/api/vote/1',
      method: 'GET'
    }).success(function(d){
      console.log(d);
      $scope.custom.time = true;
      $scope.custom.plan = true;
      return $scope.vote = d;
    });
  }, 1000);
});
function import$(obj, src){
  var own = {}.hasOwnProperty;
  for (var key in src) if (own.call(src, key)) obj[key] = src[key];
  return obj;
}