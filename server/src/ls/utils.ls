angular.module \donvote
  ..directive \accordion ($compile, $timeout) ->
    return
      restrict: \E
      replace: true
      transclude: true
      template: "<div style='overflow:hidden;height:0;' ng-transclude></div>"
      scope: expand: '=ngExpand'
      link: (s,e,a) ->
        cog = [['auto' '0' 'visible' '1'], ['0' 'auto' 'hidden' '0.5']]
        console.log a['ngExpand'], e.height!
        s.$watch 'expand', (v) -> if typeof(v)!="undefined" =>
          c = if v => cog.0 else cog.1
          e.height c.0
          r = e.height!
          e.height c.1
          console.log a['ngExpand'], c.0, r, c.2
          e.css overflow: c.2
          e.animate opacity: c.3, height: r, -> 
            e.css height: c.0, opacity: c.3, overflow: c.2

  ..directive \timedelta ($compile) ->
    return
      restrict: \E
      replace: true
      transclude: true
      template:
        "<div class='timedelta'>" +
        "<input class='form-control day' type='text'>" +
        "<span>天</span> " +
        "<input class='form-control hour' type='text'>" +
        "<span>時</span> " +
        "<input class='form-control minute' type='text'>" +
        "<span>分</span> "+
        "</div>"
      scope: model: '=ngModel', disabled: '=ngDisabled'
      link: (s,e,a) ->
        [d,h,m] = <[day hour minute]>map -> e.find(".#it")
        update-model = ->
          s.model = (d.val! * 86400 + h.val! * 3600 + m.val! * 60) * 1000
        if a[\ngModel] => 
          [d,h,m]map -> it.on \change -> update-model!
          s.$watch 'disabled' -> [d,h,m].map -> it.prop \disabled, s.disabled or false
          s.$watch 'model' (v) -> if v =>
            v /= 1000
            d.val parseInt(v / 86400)
            h.val parseInt((v % 86400)/3600)
            m.val parseInt((v %3600)/60)
