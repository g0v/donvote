angular.module \donvote
  ..factory \sel2, (urlpatterns) ->
    ret = do
      user: do
        placeholder: \選擇成員
        minimumInputLength: 2
        multiple: true
        ajax: do
          url: urlpatterns.api_user_list!
          dataType: \json
          quietMillis: 100
          data: (term, page) -> do
            username: term,
            page_limit: 5,
            page: page
          results: (data, page) ->
            data.results = data.results.map(-> {id: it.id, text: it.username})
            {results: data.results, more: page * 5 < data.count}
      group: do
        placeholder: \選擇群組
        minimumInputLength: 2
        multiple: true
        ajax: do
          url: urlpatterns.api_group_list!
          dataType: \json
          quietMillis: 100
          data: (term, page) -> do
            name: term,
            page_limit: 5,
            page: page
          results: (data, page) ->
            data.results = data.results.map(-> {id: it.id, text: it.name})
            {results: data.results, more: page * 5 < data.count}

  ..controller \group.edit, <[$scope $http resInit urlpatterns sel2]> ++ ($scope, $http, resInit, urlpatterns, sel2) ->
    console.log sel2
    $(\#user-chooser)select2 sel2.user
    $(\#group-chooser)select2 sel2.group
    # TODO use ui-select or sth like that for better data binding
    $(\#user-chooser).on \change -> $scope.group.user = $(\#user-chooser)val!split \,
    $(\#group-chooser).on \change -> $scope.group.group = $(\#group-chooser)val!split \,
    $scope.group = {}
    $scope.create = ->
      $http do
        url: urlpatterns.api_create_group()
        method: \POST
        data: JSON.stringify($scope.group)
      .success (e) -> console.log e
      .error (e) -> console.error e
 
