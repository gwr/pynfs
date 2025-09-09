from .st_create_session import create_session
from xdrdef.nfs4_const import *
from xdrdef.nfs4_type import *
from .environment import check, fail, create_file, use_obj
import nfs_ops
op = nfs_ops.NFS4ops()
import nfs4lib

def testBug(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: bsr
    CODE: NEWBUG1
    """

    sess = env.c1.new_client_session(env.testname(t))
    res = sess.compound(use_obj(env.opts.usedir) + [op.getfh()])
    check(res)
    fh = res.resarray[-1].object

    res = sess.compound([op.putfh(fh), op.lookup(b'ebs'), op.getfh()])
    check(res)
