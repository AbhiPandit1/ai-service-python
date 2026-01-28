_buffers = {}

def add_chunk(interview_id, chunk):

    if interview_id not in _buffers:
        _buffers[interview_id] = []

    _buffers[interview_id].append(chunk)

    return "".join(_buffers[interview_id])


def finish_answer(interview_id):

    final = "".join(_buffers.get(interview_id, []))

    _buffers[interview_id] = []

    return final
