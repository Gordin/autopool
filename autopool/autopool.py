
# coding: utf-8

# In[ ]:

class Autopool(object):
    def __init__(self, pool, cleanup):
        # check if __del__ of this class will actually be called
        mro = self.__class__.__mro__
        for c in mro[1:-1]:
            if mro[0].__del__ == c.__del__ and mro[1] is not Autopool:
            #Class does not have own __del__ and our __del__ can't be called first!
                def __nop__():
                    pass
                self.__really_delete__ = True
                self.__del__ = __nop__
                # Make really sure this this actually gets deleted just in case...
                raise Exception("Please make sure Autopool.__del__ gets called by writing your own __del__ or put Autopool as first Inheritance")
        if not hasattr(pool, "append"):
            raise "Pool has no append function!"
        self.pool = pool
        if cleanup:
            self.cleanup = cleanup

    def __del__(self):
        if hasattr(self, "__really_delete__"):
            try:
                super(self.__class__, self).__del__()
            finally:
                return
        if hasattr(self, "cleanup"):
            self.cleanup(self)
        self.pool.append(self)

    def stop_pooling(self):
        self.__really_delete__ = True
