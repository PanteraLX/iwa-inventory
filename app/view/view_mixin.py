class ViewMixin():
    ''' Mixin class for all custom views '''

    def extract_pk(self, kwargs):
        ''' Extracts the primary key from the kwargs dictionary'''
        if kwargs and kwargs['pk']:
            return kwargs['pk']
        return None

    def extract_query_value(self, request, key):
        ''' Extracts the value of a key from the request dictionary'''
        if request and request.GET and request.GET[key]:
            return request.GET[key]
        return None

    def extract_object(self, pk):
        ''' Extracts the object from the model based on the primary key'''
        if pk:
            return self.model.objects.get(id=pk)
        return None