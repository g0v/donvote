(function() {
{% include 'django_js_reverse/urls_js.tpl' %}
var {{ js_var_name }} = this.{{ js_var_name }};
angular.module("django.common")
.factory("urlpatterns",function() {
  return {{js_var_name}};
});
})();
