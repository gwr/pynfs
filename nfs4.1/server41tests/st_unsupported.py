from .st_create_session import create_session
from xdrdef.nfs4_const import *
from xdrdef.nfs4_type import *
from .environment import check, fail, create_file
import nfs_ops
op = nfs_ops.NFS4ops()
import nfs4lib

def testAllocSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT1
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.allocate(stateid, 0, 1)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testCopySupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT2
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.copy(stateid, stateid, 0, 0, 1, 1, 1, [])])
    check(res, stat=NFS4ERR_NOTSUPP)

def testCopyNotifySupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT3
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.copy_notify(stateid, netloc4(NL4_NAME, b"hello.world"))])
    check(res, stat=NFS4ERR_NOTSUPP)

def testDeallocateSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT4
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.deallocate(stateid, 0, 1)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testIOAdviseSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT5
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.io_advise(stateid, 0, 0, 0)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testLayoutErrorSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT6
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.layouterror(0, 1, stateid, [])])
    check(res, stat=NFS4ERR_NOTSUPP)

def testLayoutStatsSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT7
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.layoutstats(0, 1, stateid, io_info4(1, 1), io_info4(1, 1), b"deviceid", layoutupdate4(1, b""))])
    check(res, stat=NFS4ERR_NOTSUPP)

def testOffloadCancelSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT8
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.offload_cancel(stateid)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testOffloadStatusSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT9
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.offload_status(stateid)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testReadPlusSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT10
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.read_plus(stateid, 0, 1)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testSeekSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT11
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.seek(stateid, 0, 0)])
    check(res, stat=NFS4ERR_NOTSUPP)

def testWriteSameSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT12
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.write_same(stateid, 0, app_data_block4(0, 1, 1, 1, 1, 1, b"test"))])
    check(res, stat=NFS4ERR_NOTSUPP)

def testCloneSupported(t, env):
    """send PUTROOTFH+OP, check for legal result

    FLAGS: neg
    CODE: SUPPORT13
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = create_file(sess, env.testname(t), access=OPEN4_SHARE_ACCESS_WRITE)
    fh = res.resarray[-1].object
    stateid = res.resarray[-2].stateid

    res = sess.compound([op.putfh(fh), op.clone(stateid, stateid, 0, 0, 1)])
    check(res, stat=NFS4ERR_NOTSUPP)

