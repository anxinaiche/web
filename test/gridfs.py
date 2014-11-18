from tornado import gen
import motor

db = motor.MotorClient().test

@gen.coroutine
def write_file():
    fs = motor.MotorGridFS(db)

    # file_id is the ObjectId of the resulting file.
    file_id = yield fs.put('Contents')

    # put() can take a file or a file-like object, too.
    from cStringIO import StringIO
    file_like = StringIO('Lengthy contents')
    file_id = yield fs.put(file_like)

    # Specify the _id.
    specified_id = yield fs.put('Contents', _id=42)
    assert 42 == specified_id