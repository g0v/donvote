angular.module \donvote
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
        console.log(e.find \.day)
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
