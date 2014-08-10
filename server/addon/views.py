def SubView(o_class):
  o_get_queryset = o_class.get_queryset
  o_pre_delete = o_class.pre_delete
  o_post_save = o_class.pre_save

  root_class = None
  target_field = ""

  # need to check if obj exists
  def get_queryset(self):
    obj = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(obj): return obj[0].__getattribute__(self.target_field).all()
    else: return []
  def pre_delete(self, obj):
    obj = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(obj): obj[0].__getattribute__(self.target_field).remove(obj)
    super(o_class, self).pre_delete(obj)
  def post_save(self, obj, created=False):
    v = self.root_class.objects.filter(pk=self.kwargs[self.target_field+"_owner_pk"])
    if len(v): v[0].__getattribute__(self.target_field).add(obj)
    super(o_class, self).post_save(obj)

  o_class.get_queryset = get_queryset
  o_class.pre_delete = pre_delete
  o_class.post_save = post_save
  return o_class

