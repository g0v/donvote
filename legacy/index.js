// Generated by LiveScript 1.2.0
angular.module('simple', ['ui.bootstrap.datetimepicker', 'main']);
ctrl.blah = function($scope){
  $scope.max = 1;
  return $scope.$watch('$parent.cs', function(it){
    var k, v;
    $scope.max = Math.max.apply(null, (function(){
      var ref$, results$ = [];
      for (k in ref$ = it.d) {
        v = ref$[k];
        results$.push(parseInt(v.c));
      }
      return results$;
    }()));
    if ($scope.max <= 0) {
      return $scope.max = 1;
    }
  });
};
ctrl.simpletab = function($scope){
  $scope.tab = 2;
  return $scope.active = function(a, b){
    if (a === b) {
      return 'active';
    } else {
      return "";
    }
  };
};
ctrl.simplebase = function($scope, $location, $interval, DataService){
  var k, v, s, updateProgress;
  angular.element('body').scope().tab = 2;
  angular.element('#current-proposal').scope().cur = ((function(){
    var ref$, results$ = [];
    for (k in ref$ = DataService.proposal.ref) {
      v = ref$[k];
      results$.push([k, v]);
    }
    return results$;
  }())[0] || [])[1] || {};
  $scope.proposal = {
    ref: DataService.proposal.ref,
    s: function(){
      return angular.element('#current-proposal').scope();
    }
  };
  $scope.color = d3.scale.category20();
  $scope.updatePropCur = function(p){
    var x$, s, y$;
    x$ = s = $scope.proposal.s();
    x$.propCur = p;
    x$.cs = s.choiceState(s.propCur);
    y$ = $scope;
    y$.propCur = p;
    y$.id = p.id;
    y$.tab = 3;
    return $location.search({
      proposal: p.id
    });
  };
  s = $scope.proposal.s();
  $scope.$watch('proposal.ref', function(){
    var that, x$, s;
    $scope.proposal.ref = DataService.proposal.ref;
    if (that = $scope.proposal.ref[$location.search()['proposal']]) {
      $scope.updatePropCur(that);
    }
    x$ = s = $scope.proposal.s();
    if (s.propCur) {
      x$.propCur = $scope.proposal.ref[s.propCur.id];
    }
    x$.cs = s.choiceState(s.propCur);
    return x$;
  }, true);
  updateProgress = function(){
    var remains;
    if ($scope.propCur) {
      $scope.propCur.progress = $scope.proposal.s().getProgress($scope.propCur);
      remains = parseInt((($scope.propCur.end || 0) - new Date().getTime()) / 1000);
      $scope.propCur.remains = (remains > 86400 ? parseInt(remains / 86400) + " 天 " : "") + (remains > 3600 ? parseInt((remains % 86400) / 3600) + " 時 " : "") + (remains > 60 ? parseInt((remains % 3600) / 60) + " 分 " : "") + (parseInt(remains % 60) + " 秒");
      if (remains <= 0) {
        return $scope.propCur.remains = null;
      }
    }
  };
  $scope.$watch('propCur', updateProgress);
  return $interval(updateProgress, 1000);
};