// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('ld.common', []);
x$.directive('state', ['$timeout'].concat(function($timeout){
  return {
    require: 'ngModel',
    restrict: 'E',
    scope: {
      state: '=ngModel'
    },
    templateUrl: '/directives/state',
    link: function(s, e, a, c){}
  };
}));
x$.factory('stateIndicator', function(){
  return {
    init: function(){
      return {
        value: 0,
        reset: function(){
          return this.value = 0;
        },
        loading: function(){
          return this.value = 1;
        },
        done: function(){
          return this.value = 2;
        },
        fail: function(){
          return this.value = 3;
        }
      };
    }
  };
});
x$.directive('delayBk', function(){
  return {
    restrict: 'A',
    link: function(scope, e, attrs, ctrl){
      var url;
      url = attrs["delayBk"];
      return $('<img/>').attr('src', url).load(function(){
        $(this).remove();
        e.css({
          "background-image": "url(" + url + ")"
        });
        return setTimeout(function(){
          return e.toggleClass('visible');
        }, 100);
      });
    }
  };
});