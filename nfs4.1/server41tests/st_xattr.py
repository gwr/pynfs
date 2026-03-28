from .st_create_session import create_session
from xdrdef.nfs4_const import *

from .environment import check, fail, create_file, open_file, close_file
from .environment import open_create_file_op, do_getattrdict
from xdrdef.nfs4_type import open_owner4, openflag4, createhow4, open_claim4
from xdrdef.nfs4_type import creatverfattr, fattr4, stateid4, locker4, lock_owner4
from xdrdef.nfs4_type import open_to_lock_owner4
import nfs_ops
op = nfs_ops.NFS4ops()
import threading
from testmod import UnsupportedException

current_stateid = stateid4(1, b'\0' * 12)


def _require_xattr_support(sess):
    """Skip the calling test if the server does not support xattr.

    Per RFC 8276 s8.2.1, a client may reasonably assume that a server
    that does not advertise FATTR4_XATTR_SUPPORT in supported_attrs, or
    that returns False for it, does not provide xattr support.  Raises
    UnsupportedException so the test runner marks the test UNSUPPORTED
    rather than FAILED.
    """
    res = sess.compound([op.putrootfh(),
                         op.getattr(1 << FATTR4_SUPPORTED_ATTRS |
                                    1 << FATTR4_XATTR_SUPPORT)])
    check(res)
    attrs = res.resarray[-1].obj_attributes
    bitmask = attrs.get(FATTR4_SUPPORTED_ATTRS, 0)
    if not (bitmask & (1 << FATTR4_XATTR_SUPPORT)):
        raise UnsupportedException(
            "Server does not advertise FATTR4_XATTR_SUPPORT in supported_attrs")
    if not attrs.get(FATTR4_XATTR_SUPPORT, False):
        raise UnsupportedException(
            "Server reports xattr_support=False")

def testGetXattrAttribute(t, env):
    """FATTR4_XATTR_SUPPORT must be advertised and return True when xattr supported.

    FLAGS: xattr all
    CODE: XATT1
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    res = sess.compound([op.putrootfh(),
                         op.getattr(1 << FATTR4_SUPPORTED_ATTRS |
                                    1 << FATTR4_XATTR_SUPPORT)])
    check(res)

    if FATTR4_SUPPORTED_ATTRS not in res.resarray[-1].obj_attributes:
        fail("Requested bitmap of supported attributes not provided")

    bitmask = res.resarray[-1].obj_attributes[FATTR4_SUPPORTED_ATTRS]
    if not (bitmask & (1 << FATTR4_XATTR_SUPPORT)):
        raise UnsupportedException(
            "FATTR4_XATTR_SUPPORT not in supported_attrs; server does not support xattr")

    if not res.resarray[-1].obj_attributes.get(FATTR4_XATTR_SUPPORT, False):
        fail("Server advertises FATTR4_XATTR_SUPPORT but does not return True")


def testGetMissingAttr(t, env):
    """Server MUST return NFS4ERR_NOXATTR if value is missing.

    FLAGS: xattr all
    CODE: XATT2
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    res = sess.compound([op.putfh(fh), op.getxattr("user.attr1".encode("UTF-8"))])
    check(res, NFS4ERR_NOXATTR)

def testCreateNewAttr(t, env):
    """Server MUST return NFS4_ON on create.

    FLAGS: xattr all
    CODE: XATT3
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value = "value1".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key, value)])
    check(res)

    res = sess.compound([op.putfh(fh), op.getxattr(key)])
    check(res)
    if value != res.resarray[-1].gxr_value:
        fail("Returned value doesn't")

def testCreateNewIfMissingAttr(t, env):
    """Server MUST update existing attribute with SETXATTR4_EITHER.

    FLAGS: xattr all
    CODE: XATT4
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value = "value1".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_EITHER, key, value)])
    check(res)

    res = sess.compound([op.putfh(fh), op.getxattr(key)])
    check(res)
    if value != res.resarray[-1].gxr_value:
        fail("Returned value doesn't match with expected one.")

def testUpdateOfMissingAttr(t, env):
    """Server MUST return NFS4ERR_NOXATTR on update of missing attribute.

    FLAGS: xattr all
    CODE: XATT5
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value = "value1".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_REPLACE, key, value)])
    check(res, NFS4ERR_NOXATTR)

def testExclusiveCreateAttr(t, env):
    """Server MUST return NFS4ERR_EXIST on create of existing attribute.

    FLAGS: xattr all
    CODE: XATT6
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value = "value1".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key, value)])
    check(res)

    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key, value)])
    check(res, NFS4ERR_EXIST)

def testUpdateExistingAttr(t, env):
    """Server MUST return NFS4_ON on update of existing attribute.

    FLAGS: xattr all
    CODE: XATT7
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value1 = "value1".encode("UTF-8")
    value2 = "value2".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key, value1)])
    check(res)

    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_REPLACE, key, value2)])
    check(res)

    res = sess.compound([op.putfh(fh), op.getxattr(key)])
    check(res)
    if value2 != res.resarray[-1].gxr_value:
        fail("Returned value doesn't match with expected one.")

def testRemoveNonExistingAttr(t, env):
    """Server MUST return NFS4ERR_NOXATTR on remove of non existing attribute.

    FLAGS: xattr all
    CODE: XATT8
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")

    res = sess.compound([op.putfh(fh), op.removexattr(key)])
    check(res, NFS4ERR_NOXATTR)

def testRemoveExistingAttr(t, env):
    """Server MUST return NFS4_ON on remove of existing attribute.

    FLAGS: xattr all
    CODE: XATT9
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object
    key = "user.attr1".encode("UTF-8")
    value = "value1".encode("UTF-8")
    res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key, value)])
    check(res)

    res = sess.compound([op.putfh(fh), op.removexattr(key)])
    check(res)

def testListNoAttrs(t, env):
    """Server MUST return NFS4_ON an empty list if no attributes defined.

    FLAGS: xattr all
    CODE: XATT10
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object

    res = sess.compound([op.putfh(fh), op.listxattrs(0, 8192)])
    check(res)

    if not res.resarray[-1].lxr_eof:
        fail("EOF flag is not set")

    if len(res.resarray[-1].lxr_names) > 0:
        fail("Unexpected attributes returned")

def testListAttrs(t, env):
    """Server MUST return NFS4_ON and list of defined attributes.

    FLAGS: xattr all
    CODE: XATT11
    VERS: 2-
    """
    sess = env.c1.new_client_session(env.testname(t))
    _require_xattr_support(sess)
    open_op = open_create_file_op(sess, env.testname(t), open_create=OPEN4_CREATE)
    res = sess.compound(open_op + [op.close(0, current_stateid)])
    check(res, NFS4_OK)

    fh = res.resarray[-2].object

    keys = ["user.attr1", "user.attr2", "user.attr3", "user.attr4", "user.attr5", "user.attr6"]

    for key in keys:
        value = "value".encode("UTF-8")
        res = sess.compound([op.putfh(fh), op.setxattr(SETXATTR4_CREATE, key.encode("UTF-8"), value)])
        check(res)

    res = sess.compound([op.putfh(fh), op.listxattrs(0, 8192)])
    check(res)

    xattrs = [key.decode("UTF-8") for key in res.resarray[-1].lxr_names]
    if len(xattrs) != len(keys):
        fail("Invalid number of entries returuned <expected> %d, <actual> %d" % (len(keys), len(xattrs)))

    for key in keys:
        if key not in xattrs:
            fail("Unexpected attribute received %s" % key)
