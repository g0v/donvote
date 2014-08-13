angular.module \ld.common, <[]>

  ..directive \state, <[$timeout]> ++ ($timeout) -> do
    require: \ngModel
    restrict: \E
    scope: state: \=ngModel
    templateUrl: \/directives/state
    link: (s,e,a,c) ->

  ..factory \stateIndicator, -> do
    init: -> do
      value: 0
      reset: -> @value = 0
      loading: -> @value = 1
      done: -> @value = 2
      fail: -> @value = 3

  ..directive \delayBk, -> do
    restrict: \A
    link: (scope, e, attrs, ctrl) ->
      url = attrs["delayBk"]
      $ \<img/> .attr \src url .load ->
        $(@)remove!
        e.css "background-image": "url(#url)"
        setTimeout (-> e.toggle-class \visible), 100
