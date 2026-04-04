from xdrdef.nfs4_const import *
from .environment import check, create_confirm, close_file, lookup_obj
import nfs_ops
op = nfs_ops.NFS4ops()

def remove_obj(sess, path):
    """Remove the object at path (dir + name)."""
    dirfh = lookup_obj(sess, path[:-1])
    return sess.compound([op.putfh(dirfh), op.remove(path[-1])])

def testStaleRemove(t, env):
    """REMOVE of an open file should allow CLOSE

    FLAGS: remove all
    CODE: RM21
    """
    name = env.testname(t)
    owner = b"owner_%s" % name
    sess = env.c1.new_client_session(name)
    path = env.c1.homedir + [name]
    fh, stateid = create_confirm(sess, owner, path=path)
    res = remove_obj(sess, path)
    check(res)
    res = close_file(sess, fh, stateid)
    check(res, msg="CLOSE after REMOVE of open file returns ESTALE")
